#!/usr/bin/env python3
import json
import os
import sys
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


SCRIPT_DIR = Path(__file__).resolve().parent
PLUGIN_ROOT = SCRIPT_DIR.parent
PLUGIN_ENV = PLUGIN_ROOT / ".env"

VIDEO_REGION_BASES = {
    "beijing": "https://dashscope.aliyuncs.com/api/v1",
    "singapore": "https://dashscope-intl.aliyuncs.com/api/v1",
}

IMAGE_URLS = {
    "beijing": "https://dashscope.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation",
    "singapore": "https://dashscope-intl.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation",
}


def load_plugin_env() -> None:
    if not PLUGIN_ENV.exists():
        return
    for line in PLUGIN_ENV.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            key, value = line.split("=", 1)
            os.environ.setdefault(key.strip(), value.strip())


load_plugin_env()


def require_api_key() -> str:
    api_key = os.environ.get("DASHSCOPE_API_KEY", "").strip()
    if not api_key:
        print("ERROR: DASHSCOPE_API_KEY not set. Put it in the shell or plugin-local .env.", file=sys.stderr)
        raise SystemExit(1)
    return api_key


def http_json(url: str, api_key: str, payload: dict, *, extra_headers: dict | None = None) -> dict:
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    if extra_headers:
        headers.update(extra_headers)
    request = Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers=headers,
        method="POST",
    )
    try:
        with urlopen(request) as response:
            return json.loads(response.read().decode("utf-8"))
    except HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"HTTP {exc.code} calling {url}: {body}") from exc
    except URLError as exc:
        raise RuntimeError(f"Network error calling {url}: {exc}") from exc


def http_get_json(url: str, api_key: str) -> dict:
    request = Request(url, headers={"Authorization": f"Bearer {api_key}"}, method="GET")
    try:
        with urlopen(request) as response:
            return json.loads(response.read().decode("utf-8"))
    except HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"HTTP {exc.code} calling {url}: {body}") from exc
    except URLError as exc:
        raise RuntimeError(f"Network error calling {url}: {exc}") from exc


def download_file(url: str, destination: Path) -> Path:
    destination.parent.mkdir(parents=True, exist_ok=True)
    request = Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urlopen(request) as response:
        destination.write_bytes(response.read())
    return destination
