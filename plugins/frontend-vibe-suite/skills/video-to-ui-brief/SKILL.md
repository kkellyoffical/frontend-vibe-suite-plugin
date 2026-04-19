---
name: video-to-ui-brief
description: Translate a generated UI showcase video into structured frontend language using a Qwen Omni model over the DashScope OpenAI-compatible API.
metadata: {"openclaw":{"requires":{"env":["DASHSCOPE_API_KEY"]},"primaryEnv":"DASHSCOPE_API_KEY","skillKey":"video-to-ui-brief"}}
---

# Video To UI Brief

Use this skill after a Wan2.7 showcase video exists and you want a machine-readable frontend brief from that visual artifact.

## Inputs

- a public `video_url`
- optional context about product type, stack, and what to focus on

## Script

Run:

```bash
python3 plugins/frontend-vibe-suite/scripts/video_to_ui_brief.py \
  --video-url https://example.com/design-preview.mp4 \
  --prompt-pack path/to/frontend-prompt-pack.json \
  --focus "dashboard layout, navigation, KPI cards, chart styling, motion language" \
  --output path/to/video-ui-brief.json
```

## Environment

Required:

- `DASHSCOPE_API_KEY`

Optional:

- `DASHSCOPE_BASE_URL`
- `QWEN_OMNI_MODEL`

## What the translator should extract

- page regions and hierarchy
- layout system
- likely design tokens
- interaction patterns
- motion language
- implementation hints
- open questions or ambiguities

## Output Contract

The output JSON should be usable as the design source for:

- `frontend-skill`
- `ui-ux-pro-max`
- manual implementation tickets

If the video is too vague or too cinematic to support that, say so and loop back to brief refinement rather than pretending the translation is reliable.
