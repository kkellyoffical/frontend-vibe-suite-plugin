# Frontend Vibe Suite

`frontend-vibe-suite` adds a multimodal design loop to frontend development:

1. clarify the visual direction with a style interview
2. render prompts for Wan2.7
3. generate concept frames or a short UI video
4. translate the video back into frontend language with Qwen Omni
5. generate a strict build handoff for downstream coding

## Included

### Skills

- `frontend-vibe-suite`
- `frontend-style-interview`
- `video-to-ui-brief`
- `frontend-build-handoff`

### Scripts

- `scripts/render_prompt_pack.py`
- `scripts/run_visual_loop.py`
- `scripts/video_to_ui_brief.py`
- `scripts/build_handoff.py`

### Example files

- `examples/frontend-style-brief.example.json`
- `examples/frontend-prompt-pack.example.json`
- `examples/video-ui-brief.example.json`
- `examples/build-handoff.example.json`
- `examples/build-handoff.example.md`

## Expected Workflow

### 1. Build the style brief

Run the interview workflow until product, surface, mood, density, anti-goals, and implementation constraints are specific enough to drive image and video generation.

### 2. Render the prompt pack

```bash
python3 plugins/frontend-vibe-suite/scripts/render_prompt_pack.py \
  --brief path/to/frontend-style-brief.json \
  --output path/to/frontend-prompt-pack.json
```

### 3. Run the visual loop

Use your existing `wan27-image` and `wan27-video` skills directly, or use the wrapper:

```bash
python3 plugins/frontend-vibe-suite/scripts/run_visual_loop.py \
  --prompt-pack path/to/frontend-prompt-pack.json \
  --manifest-output path/to/visual-run.json \
  --image-output path/to/concept/frame.png \
  --video-output path/to/concept/showcase.mp4
```

Default mode is `t2v`. In `i2v`, the wrapped Wan skill currently expects public URLs such as `--first-frame-url`.

### 4. Translate the video

```bash
python3 plugins/frontend-vibe-suite/scripts/video_to_ui_brief.py \
  --video-url https://example.com/design-preview.mp4 \
  --prompt-pack path/to/frontend-prompt-pack.json \
  --output path/to/video-ui-brief.json
```

### 5. Generate the coding handoff

```bash
python3 plugins/frontend-vibe-suite/scripts/build_handoff.py \
  --style-brief path/to/frontend-style-brief.json \
  --translated-brief path/to/video-ui-brief.json \
  --prompt-pack path/to/frontend-prompt-pack.json \
  --output-json path/to/build-handoff.json \
  --output-md path/to/build-handoff.md
```

Continue implementation with `frontend-skill`, `ui-ux-pro-max`, and `visual-verdict`.

## Configuration

Required:

- `DASHSCOPE_API_KEY`

Optional:

- `DASHSCOPE_BASE_URL`
- `QWEN_OMNI_MODEL`

Template:

- `.env.example`

## Scope in `0.0.1`

- style brief generation
- prompt-pack generation
- wrapper for existing Wan skills
- Qwen Omni translation over the DashScope OpenAI-compatible API
- implementation handoff generation

Not included yet:

- local media upload hosting
- direct code patch generation from the translated brief
- Figma or design tool sync
