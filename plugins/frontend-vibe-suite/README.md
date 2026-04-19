# Frontend Vibe Suite

`frontend-vibe-suite` adds a multimodal design loop to frontend development:

1. clarify the visual direction with a style interview
2. render prompts for Wan2.7
3. generate concept frames or a short UI video
4. translate the video back into frontend language with Qwen Omni
5. route the stack to the right component family or Web Components system
6. generate a strict build handoff for downstream coding

## Included

### Skills

- `frontend-vibe-suite`
- `frontend-style-interview`
- `frontend-library-router`
- `video-to-ui-brief`
- `frontend-build-handoff`

### Scripts

- `scripts/choose_library.py`
- `scripts/select_prompt_template.py`
- `scripts/render_prompt_pack.py`
- `scripts/run_visual_loop.py`
- `scripts/video_to_ui_brief.py`
- `scripts/build_handoff.py`

### Example files

- `examples/frontend-style-brief.example.json`
- `examples/frontend-style-brief.vue.example.json`
- `examples/frontend-style-brief.web-components.example.json`
- `examples/library-route.react.example.json`
- `examples/library-route.vue.example.json`
- `examples/library-route.web-components.example.json`
- `examples/scenario-profile.react.example.json`
- `examples/scenario-profile.vue.example.json`
- `examples/scenario-profile.web-components.example.json`
- `examples/frontend-prompt-pack.example.json`
- `examples/video-ui-brief.example.json`
- `examples/build-handoff.example.json`
- `examples/build-handoff.example.md`

## Library Routing

This plugin keeps the stack choice explicit instead of defaulting everything to one UI kit.

- React headless: `React Aria`, `Radix UI`, `Headless UI`
- React source-first: `shadcn/ui`
- React suites: `MUI`, `Ant Design`, `Chakra UI`, `Mantine`, `PrimeReact`
- Vue suites: `PrimeVue`, `Quasar`, `Element Plus`, `Naive UI`, `Vuetify`
- Angular: `PrimeNG`, `Ionic`
- Svelte primitives: `Bits UI`, `Melt UI`
- cross-framework behavior: `Zag.js`, `Ark UI`
- portable Web Components: `Lit`, `Shoelace`, `Stencil`, `FAST`, `Fluent UI Web Components`, `Spectrum Web Components`, `Carbon Web Components`, `Vaadin`, `Material Web`
- Tailwind-only layer: `DaisyUI`

See [docs/component-library-routing.md](./docs/component-library-routing.md) for the full matrix and routing rules.

## Expected Workflow

### 1. Build the style brief

Run the interview workflow until product, surface, mood, density, anti-goals, target stack, and implementation constraints are specific enough to drive image and video generation. If the stack is still broad, resolve it with `frontend-library-router` before rendering prompts.

### 2. Resolve the scenario and library route

```bash
python3 plugins/frontend-vibe-suite/scripts/select_prompt_template.py \
  --brief path/to/frontend-style-brief.json \
  --output path/to/scenario-profile.json
```

```bash
python3 plugins/frontend-vibe-suite/scripts/choose_library.py \
  --brief path/to/frontend-style-brief.json \
  --output path/to/library-route.json
```

### 3. Render the prompt pack

```bash
python3 plugins/frontend-vibe-suite/scripts/render_prompt_pack.py \
  --brief path/to/frontend-style-brief.json \
  --output path/to/frontend-prompt-pack.json
```

The machine-readable catalogs behind this flow live at `data/component-libraries.json` and `data/prompt-scenarios.json`.

### 4. Run the visual loop

Use your existing `wan27-image` and `wan27-video` skills directly, or use the wrapper:

```bash
python3 plugins/frontend-vibe-suite/scripts/run_visual_loop.py \
  --prompt-pack path/to/frontend-prompt-pack.json \
  --manifest-output path/to/visual-run.json \
  --image-output path/to/concept/frame.png \
  --video-output path/to/concept/showcase.mp4
```

Default mode is `t2v`. In `i2v`, the wrapped Wan skill currently expects public URLs such as `--first-frame-url`.

### 5. Translate the video

```bash
python3 plugins/frontend-vibe-suite/scripts/video_to_ui_brief.py \
  --video-url https://example.com/design-preview.mp4 \
  --prompt-pack path/to/frontend-prompt-pack.json \
  --output path/to/video-ui-brief.json
```

### 6. Generate the coding handoff

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

## Scope in `0.0.2`

- style brief generation
- scenario-aware prompt generation across at least 20 UI situations
- machine-readable scenario selection
- machine-readable component-library selection
- prompt-pack generation
- wrapper for existing Wan skills
- Qwen Omni translation over the DashScope OpenAI-compatible API
- implementation handoff generation

Not included yet:

- local media upload hosting
- direct code patch generation from the translated brief
- Figma or design tool sync
