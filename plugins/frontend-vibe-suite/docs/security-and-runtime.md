# Security and Runtime Contract

This plugin should be easy to inspect before installation.

The goals of this document are:

1. make required secrets explicit
2. make network behavior explicit
3. make subprocess usage explicit
4. make dependency expectations explicit

Canonical machine-readable metadata lives in [`../data/runtime-contract.json`](../data/runtime-contract.json).

## Required Environment Variables

- `DASHSCOPE_API_KEY`
  - required for `scripts/video_to_ui_brief.py`, `scripts/generate_wan_image.py`, and `scripts/generate_wan_video.py`
  - used to authenticate calls to DashScope for both Qwen Omni translation and plugin-local Wan generation

## Optional Environment Variables

- `DASHSCOPE_BASE_URL`
  - optional override for the DashScope OpenAI-compatible base URL
- `QWEN_OMNI_MODEL`
  - optional override for the default Qwen Omni model

## Python Dependencies

Current repository Python scripts use the standard library only.

- no `pip install` step is required
- no `requirements.txt` packages are required beyond Python itself
- no postinstall behavior is expected

## Network Behavior

### Direct network calls from repo scripts

- `scripts/video_to_ui_brief.py`
  - calls the DashScope OpenAI-compatible endpoint
  - default base URL: `https://dashscope-intl.aliyuncs.com/compatible-mode/v1`
- `scripts/generate_wan_image.py`
  - calls the DashScope image generation endpoint
- `scripts/generate_wan_video.py`
  - calls the DashScope async video generation endpoint

### User-provided URLs

The workflow can transmit user-provided public media URLs when:

- a public `video_url` is passed to `video_to_ui_brief.py`
- public media URLs are passed to the plugin-local Wan `i2v` flow

## Subprocess Behavior

Only one repo script launches subprocesses:

- `scripts/run_visual_loop.py`
  - invokes plugin-local Wan helper scripts from `scripts/generate_wan_image.py` and `scripts/generate_wan_video.py`

This repo does not:

- install packages at runtime
- shell out to `pip`
- download code for execution
- modify system configuration

## File System Behavior

The scripts read:

- style briefs
- prompt packs
- translated UI briefs
- the plugin-local `.env` file only

The scripts write:

- prompt-pack JSON
- scenario and library route JSON
- translated brief JSON
- build handoff JSON and Markdown
- visual-run manifest JSON

## Bundle Hygiene

This repo should not publish:

- `.pyc` files
- `__pycache__/` directories
- undeclared runtime dependencies

If any of those appear, treat it as a release bug and fail preflight.
