#!/usr/bin/env python3
import argparse
import json
import subprocess
import sys
from pathlib import Path


IMAGE_SCRIPT = Path.home() / ".codex/skills/wan27-image/scripts/generate.py"
VIDEO_SCRIPT = Path.home() / ".codex/skills/wan27-video/scripts/generate.py"


def load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def extract_result(stdout: str) -> dict:
    marker = "---RESULT---"
    if marker not in stdout:
        return {"raw_stdout": stdout}
    raw = stdout.split(marker, 1)[1].strip()
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return {"raw_result": raw, "raw_stdout": stdout}


def run_command(command: list[str]) -> dict:
    result = subprocess.run(command, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(
            "Command failed.\n"
            f"Command: {' '.join(command)}\n"
            f"Stdout:\n{result.stdout}\n"
            f"Stderr:\n{result.stderr}"
        )
    return {
        "command": command,
        "stdout": result.stdout,
        "stderr": result.stderr,
        "parsed": extract_result(result.stdout),
    }


def build_image_command(prompt_pack: dict, args: argparse.Namespace) -> list[str]:
    command = [
        sys.executable,
        str(IMAGE_SCRIPT),
        prompt_pack["wan_image_prompt"],
        str(args.image_output),
        args.image_model,
        args.image_size,
        str(args.image_count),
    ]
    return command


def build_video_command(prompt_pack: dict, args: argparse.Namespace) -> list[str]:
    command = [
        sys.executable,
        str(VIDEO_SCRIPT),
        args.video_mode,
        "--prompt",
        prompt_pack["wan_video_prompt"],
        "--region",
        args.video_region,
        "--resolution",
        args.video_resolution,
        "--duration",
        str(args.video_duration),
        "--output",
        str(args.video_output),
    ]

    if args.video_mode in {"t2v", "r2v", "edit"} and args.video_ratio:
        command.extend(["--ratio", args.video_ratio])

    if args.video_mode == "i2v":
        if not args.first_frame_url:
            raise ValueError("i2v mode requires --first-frame-url")
        command.extend(["--media", f"first_frame={args.first_frame_url}"])
        if args.last_frame_url:
            command.extend(["--media", f"last_frame={args.last_frame_url}"])
        if args.driving_audio_url:
            command.extend(["--media", f"driving_audio={args.driving_audio_url}"])

    return command


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Run the visual generation phase of frontend-vibe-suite using existing Wan skills."
    )
    parser.add_argument("--prompt-pack", required=True, help="Path to frontend prompt-pack JSON.")
    parser.add_argument("--manifest-output", required=True, help="Path to write the run manifest JSON.")
    parser.add_argument("--image-output", default="artifacts/concept.png", help="Local output path for the image.")
    parser.add_argument("--video-output", default="artifacts/concept.mp4", help="Local output path for the video.")
    parser.add_argument("--image-model", default="wan2.7-image-pro")
    parser.add_argument("--image-size", default="2K")
    parser.add_argument("--image-count", type=int, default=1)
    parser.add_argument("--video-mode", choices=["t2v", "i2v"], default="t2v")
    parser.add_argument("--video-region", choices=["beijing", "singapore"], default="beijing")
    parser.add_argument("--video-resolution", default="720P")
    parser.add_argument("--video-ratio", default="16:9")
    parser.add_argument("--video-duration", type=int, default=5)
    parser.add_argument("--first-frame-url", default="")
    parser.add_argument("--last-frame-url", default="")
    parser.add_argument("--driving-audio-url", default="")
    parser.add_argument("--skip-image", action="store_true")
    parser.add_argument("--skip-video", action="store_true")
    args = parser.parse_args()

    if not IMAGE_SCRIPT.exists():
        raise SystemExit(f"Missing Wan image script: {IMAGE_SCRIPT}")
    if not VIDEO_SCRIPT.exists():
        raise SystemExit(f"Missing Wan video script: {VIDEO_SCRIPT}")

    prompt_pack = load_json(Path(args.prompt_pack))
    manifest = {
        "prompt_pack": str(Path(args.prompt_pack).resolve()),
        "image": None,
        "video": None,
    }

    if not args.skip_image:
        manifest["image"] = run_command(build_image_command(prompt_pack, args))

    if not args.skip_video:
        manifest["video"] = run_command(build_video_command(prompt_pack, args))

    output_path = Path(args.manifest_output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as handle:
        json.dump(manifest, handle, ensure_ascii=False, indent=2)
        handle.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
