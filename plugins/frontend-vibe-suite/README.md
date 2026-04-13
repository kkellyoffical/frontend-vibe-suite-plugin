# Frontend Vibe Suite

`frontend-vibe-suite` is a local Codex plugin for a multimodal frontend workflow:

1. interview for style, product, and interaction intent
2. turn that brief into Wan2.7 image and video prompts
3. generate a short design showcase video
4. translate the video back into a structured UI brief with Qwen Omni
5. hand the brief to implementation skills such as `frontend-skill`, `ui-ux-pro-max`, and `visual-verdict`

## Why this exists

Normal frontend codegen often jumps straight from a thin requirement to JSX and CSS.
This plugin adds a visual prototype loop in the middle so the implementation is driven
by an explicit design brief plus a machine-readable video interpretation.

## Bundled Skills

- `frontend-vibe-suite`: top-level orchestration workflow
- `frontend-style-interview`: multi-angle style and requirement interview
- `video-to-ui-brief`: translate a design video into natural language and structured JSON
- `frontend-build-handoff`: merge the style brief and translated video brief into an implementation-ready handoff

## Scripts

- `scripts/render_prompt_pack.py`
  - turns a design brief JSON into prompt packs for Wan image/video generation, omni analysis, and build handoff
- `scripts/run_visual_loop.py`
  - reads a prompt pack and invokes the existing `wan27-image` and `wan27-video` skills to generate concept assets
- `scripts/video_to_ui_brief.py`
  - calls the DashScope OpenAI-compatible chat endpoint with a Qwen Omni model and asks for a structured UI brief from a video URL
- `scripts/build_handoff.py`
  - merges the original style brief and the translated video brief into a coding handoff in JSON and Markdown

## Expected Workflow

1. Run the `frontend-style-interview` skill until the style brief is specific enough.
2. Save the brief as JSON and render a prompt pack:

```bash
python3 plugins/frontend-vibe-suite/scripts/render_prompt_pack.py \
  --brief path/to/frontend-style-brief.json \
  --output path/to/frontend-prompt-pack.json
```

A sample input brief lives at `plugins/frontend-vibe-suite/examples/frontend-style-brief.example.json`.

3. Use the generated prompts with your existing `wan27-image` and `wan27-video` skills.
   Or run the wrapper:

```bash
python3 plugins/frontend-vibe-suite/scripts/run_visual_loop.py \
  --prompt-pack path/to/frontend-prompt-pack.json \
  --manifest-output path/to/visual-run.json \
  --image-output path/to/concept/frame.png \
  --video-output path/to/concept/showcase.mp4
```

By default the wrapper uses `t2v`. If you switch to `i2v`, the current Wan video skill still expects public media URLs such as `--first-frame-url`, not local file paths.

4. Feed the resulting video URL into the translator:

```bash
python3 plugins/frontend-vibe-suite/scripts/video_to_ui_brief.py \
  --video-url https://example.com/design-preview.mp4 \
  --prompt-pack path/to/frontend-prompt-pack.json \
  --output path/to/video-ui-brief.json
```

5. Build the coding handoff:

```bash
python3 plugins/frontend-vibe-suite/scripts/build_handoff.py \
  --style-brief path/to/frontend-style-brief.json \
  --translated-brief path/to/video-ui-brief.json \
  --prompt-pack path/to/frontend-prompt-pack.json \
  --output-json path/to/build-handoff.json \
  --output-md path/to/build-handoff.md
```

6. Continue implementation with your normal frontend coding skills using the handoff as the source of truth.

## Configuration

Set `DASHSCOPE_API_KEY` before calling the translator script.

Optional:

- `DASHSCOPE_BASE_URL`: defaults to `https://dashscope-intl.aliyuncs.com/compatible-mode/v1`
- `QWEN_OMNI_MODEL`: defaults to `qwen3-omni-flash`

## Current Scope

- single-product design direction
- style brief generation
- Wan prompt pack generation
- wrapper for Wan generation via existing local skills
- Qwen Omni video interpretation
- implementation handoff generation for downstream coding

It does not yet automate:

- local video upload hosting
- Figma export or sync
- automatic code patching from the translated brief
