#!/usr/bin/env python3
import argparse
import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent
ENV_CANDIDATES = [
    SCRIPT_DIR.parent / ".env",
    Path.home() / ".codex/skills/wan27-video/.env",
    Path.home() / ".codex/skills/wan27-image/.env",
]
DEFAULT_BASE_URL = "https://dashscope-intl.aliyuncs.com/compatible-mode/v1"
DEFAULT_MODEL = "qwen3-omni-flash"


def load_env_file(path: Path) -> None:
    if not path.exists():
        return
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            key, value = line.split("=", 1)
            os.environ.setdefault(key.strip(), value.strip())


for env_file in ENV_CANDIDATES:
    load_env_file(env_file)


def build_messages(video_url: str, focus: str, prompt_override: str) -> list[dict]:
    system_prompt = (
        "You are a senior frontend architect and design translator. "
        "You watch UI concept videos and convert them into implementation-ready frontend briefs. "
        "Return JSON only."
    )
    user_prompt = prompt_override or (
        "Analyze this design video and return a JSON object with these keys: "
        "summary, page_regions, visual_tokens, typography, color, spacing, components, "
        "interactions, motion, implementation_hints, ambiguities. "
        "Keep the output concrete and frontend-oriented.\n"
        f"Focus: {focus or 'overall layout, tokens, components, and motion language'}"
    )
    return [
        {"role": "system", "content": system_prompt},
        {
            "role": "user",
            "content": [
                {"type": "text", "text": user_prompt},
                {"type": "video_url", "video_url": {"url": video_url}},
            ],
        },
    ]


def call_dashscope(
    api_key: str,
    base_url: str,
    model: str,
    video_url: str,
    focus: str,
    prompt_override: str,
) -> str:
    payload = {
        "model": model,
        "messages": build_messages(video_url, focus, prompt_override),
        "temperature": 0.2,
    }
    request = urllib.request.Request(
        f"{base_url.rstrip('/')}/chat/completions",
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=180) as response:
            data = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"DashScope HTTP {exc.code}: {body}") from exc
    except urllib.error.URLError as exc:
        raise RuntimeError(f"DashScope request failed: {exc}") from exc

    choices = data.get("choices") or []
    if not choices:
        raise RuntimeError(f"Unexpected response shape: {json.dumps(data, ensure_ascii=False)}")
    message = choices[0].get("message") or {}
    content = message.get("content")
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        text_parts = []
        for part in content:
            if part.get("type") == "text":
                text_parts.append(part.get("text", ""))
        if text_parts:
            return "\n".join(text_parts)
    raise RuntimeError(f"Could not extract text content from response: {json.dumps(data, ensure_ascii=False)}")


def parse_model_output(raw_text: str) -> dict:
    stripped = raw_text.strip()
    if stripped.startswith("```"):
        lines = [line for line in stripped.splitlines() if not line.startswith("```")]
        stripped = "\n".join(lines).strip()
    try:
        return json.loads(stripped)
    except json.JSONDecodeError:
        return {"raw_output": raw_text}


def load_prompt_override(prompt_pack_path: str) -> str:
    if not prompt_pack_path:
        return ""
    with Path(prompt_pack_path).open("r", encoding="utf-8") as handle:
        prompt_pack = json.load(handle)
    return prompt_pack.get("omni_translation_prompt", "")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Translate a design showcase video into a structured frontend brief with Qwen Omni."
    )
    parser.add_argument("--video-url", required=True, help="Public URL for the design video.")
    parser.add_argument("--focus", default="", help="Optional analysis focus area.")
    parser.add_argument("--prompt-pack", default="", help="Optional prompt-pack JSON for omni_translation_prompt.")
    parser.add_argument(
        "--model",
        default=os.environ.get("QWEN_OMNI_MODEL", DEFAULT_MODEL),
        help="DashScope Qwen Omni model name. Default: qwen3-omni-flash",
    )
    parser.add_argument(
        "--base-url",
        default=os.environ.get("DASHSCOPE_BASE_URL", DEFAULT_BASE_URL),
        help="DashScope OpenAI-compatible base URL.",
    )
    parser.add_argument("--output", required=True, help="Path to write the translated JSON brief.")
    args = parser.parse_args()

    api_key = os.environ.get("DASHSCOPE_API_KEY")
    if not api_key:
        print("Missing DASHSCOPE_API_KEY", file=sys.stderr)
        return 1

    prompt_override = load_prompt_override(args.prompt_pack)

    raw_text = call_dashscope(
        api_key=api_key,
        base_url=args.base_url,
        model=args.model,
        video_url=args.video_url,
        focus=args.focus,
        prompt_override=prompt_override,
    )
    parsed = parse_model_output(raw_text)
    result = {
        "model": args.model,
        "video_url": args.video_url,
        "focus": args.focus,
        "prompt_pack": args.prompt_pack,
        "brief": parsed,
        "raw_output": raw_text,
    }

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as handle:
        json.dump(result, handle, ensure_ascii=False, indent=2)
        handle.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
