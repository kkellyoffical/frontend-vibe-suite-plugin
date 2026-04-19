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
  - required for `scripts/video_to_ui_brief.py`
  - used to authenticate calls to the DashScope OpenAI-compatible API for Qwen Omni video understanding

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

### Indirect network calls

- `scripts/run_visual_loop.py`
  - calls local Wan helper scripts
  - those local Wan scripts can contact DashScope according to their own implementation

### User-provided URLs

The workflow can transmit user-provided public media URLs when:

- a public `video_url` is passed to `video_to_ui_brief.py`
- public media URLs are passed through the wrapped Wan video flow

## Subprocess Behavior

Only one repo script launches subprocesses:

- `scripts/run_visual_loop.py`
  - invokes local Wan helper scripts from `~/.codex/skills/wan27-image` and `~/.codex/skills/wan27-video`

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
- `.env` files under the plugin and local Wan skill directories

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
