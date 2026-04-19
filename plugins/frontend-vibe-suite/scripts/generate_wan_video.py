#!/usr/bin/env python3
import argparse
import json
import time
from pathlib import Path

from dashscope_common import VIDEO_REGION_BASES, download_file, http_get_json, http_json, require_api_key


def maybe_put(target: dict, key: str, value) -> None:
    if value is not None and value != "":
        target[key] = value


def create_task(base_url: str, api_key: str, payload: dict) -> dict:
    return http_json(
        f"{base_url}/services/aigc/video-generation/video-synthesis",
        api_key,
        payload,
        extra_headers={"X-DashScope-Async": "enable"},
    )


def fetch_task(base_url: str, api_key: str, task_id: str) -> dict:
    return http_get_json(f"{base_url}/tasks/{task_id}", api_key)


def wait_for_task(base_url: str, api_key: str, task_id: str, poll_interval: int, timeout: int) -> dict:
    deadline = time.time() + timeout
    while time.time() < deadline:
        result = fetch_task(base_url, api_key, task_id)
        status = result.get("output", {}).get("task_status")
        if status in {"SUCCEEDED", "FAILED", "CANCELED", "UNKNOWN"}:
            return result
        time.sleep(poll_interval)
    raise TimeoutError(f"Timed out waiting for task {task_id}")


def build_t2v_payload(args: argparse.Namespace) -> dict:
    input_obj = {"prompt": args.prompt}
    params: dict = {}
    maybe_put(params, "resolution", args.resolution)
    maybe_put(params, "ratio", args.ratio)
    maybe_put(params, "duration", args.duration)
    return {"model": "wan2.7-t2v", "input": input_obj, "parameters": params}


def build_i2v_payload(args: argparse.Namespace) -> dict:
    if not args.first_frame_url:
        raise ValueError("i2v mode requires --first-frame-url")
    media = [{"type": "first_frame", "url": args.first_frame_url}]
    if args.last_frame_url:
        media.append({"type": "last_frame", "url": args.last_frame_url})
    if args.driving_audio_url:
        media.append({"type": "driving_audio", "url": args.driving_audio_url})
    input_obj = {"media": media}
    maybe_put(input_obj, "prompt", args.prompt)
    params: dict = {}
    maybe_put(params, "resolution", args.resolution)
    maybe_put(params, "duration", args.duration)
    return {"model": "wan2.7-i2v", "input": input_obj, "parameters": params}


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate Wan2.7 videos from the plugin-local wrapper.")
    parser.add_argument("mode", choices=["t2v", "i2v"])
    parser.add_argument("--prompt", default="")
    parser.add_argument("--region", choices=sorted(VIDEO_REGION_BASES), default="beijing")
    parser.add_argument("--resolution", default="720P")
    parser.add_argument("--ratio", default="16:9")
    parser.add_argument("--duration", type=int, default=5)
    parser.add_argument("--output", required=True)
    parser.add_argument("--poll-interval", type=int, default=15)
    parser.add_argument("--timeout", type=int, default=1800)
    parser.add_argument("--first-frame-url", default="")
    parser.add_argument("--last-frame-url", default="")
    parser.add_argument("--driving-audio-url", default="")
    args = parser.parse_args()

    api_key = require_api_key()
    base_url = VIDEO_REGION_BASES[args.region]
    payload = build_t2v_payload(args) if args.mode == "t2v" else build_i2v_payload(args)
    created = create_task(base_url, api_key, payload)
    task_id = created.get("output", {}).get("task_id")
    if not task_id:
        raise SystemExit(f"Wan video task creation failed: {json.dumps(created, ensure_ascii=False)}")

    result = wait_for_task(base_url, api_key, task_id, args.poll_interval, args.timeout)
    output = result.get("output", {})
    if output.get("task_status") != "SUCCEEDED":
        raise SystemExit(f"Wan video generation failed: {json.dumps(result, ensure_ascii=False)}")
    video_url = output.get("video_url")
    if not video_url:
        raise SystemExit(f"Wan video succeeded without video_url: {json.dumps(result, ensure_ascii=False)}")

    destination = Path(args.output)
    download_file(video_url, destination)
    print("---RESULT---")
    print(json.dumps({"task_id": task_id, "saved": str(destination), "model": payload["model"]}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
