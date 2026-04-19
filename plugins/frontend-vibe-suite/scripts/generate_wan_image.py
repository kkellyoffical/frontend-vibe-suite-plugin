#!/usr/bin/env python3
import argparse
import json
from pathlib import Path

from dashscope_common import IMAGE_URLS, download_file, http_json, require_api_key


def output_path_for_choice(output_path: str | None, choice_index: int, total_choices: int) -> Path:
    if output_path and total_choices > 1:
        base = Path(output_path)
        return base.parent / f"{base.stem}_{choice_index}{base.suffix}"
    if output_path:
        return Path(output_path)
    return Path(f"artifacts/wan2.7_{choice_index}.png")


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate Wan2.7 images from the plugin-local wrapper.")
    parser.add_argument("prompt")
    parser.add_argument("output_path", nargs="?")
    parser.add_argument("model", nargs="?", default="wan2.7-image-pro")
    parser.add_argument("size", nargs="?", default="2K")
    parser.add_argument("count", nargs="?", type=int, default=1)
    parser.add_argument("--region", choices=sorted(IMAGE_URLS), default="beijing")
    args = parser.parse_args()

    payload = {
        "model": args.model,
        "input": {
            "messages": [
                {
                    "role": "user",
                    "content": [{"text": args.prompt}],
                }
            ]
        },
        "parameters": {
            "size": args.size,
            "n": args.count,
        },
    }

    result = http_json(IMAGE_URLS[args.region], require_api_key(), payload)
    choices = result.get("output", {}).get("choices", [])
    if not choices:
        raise SystemExit(f"Wan image generation returned no choices: {json.dumps(result, ensure_ascii=False)}")

    saved = []
    for index, choice in enumerate(choices):
        content = choice.get("message", {}).get("content", [{}])
        image_url = content[0].get("image") if content else None
        if not image_url:
            continue
        destination = output_path_for_choice(args.output_path, index, len(choices))
        download_file(image_url, destination)
        saved.append(str(destination))

    print("---RESULT---")
    print(json.dumps({"saved": saved, "model": args.model, "size": args.size}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
