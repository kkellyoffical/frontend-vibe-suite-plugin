<p align="center">
  <img src="./assets/frontend-vibe-suite-hero.svg" alt="Frontend Vibe Suite hero" width="100%" />
</p>

<p align="center">
  <strong>Multimodal frontend workflow for Codex</strong><br />
  Interview the style. Generate the concept. Translate the video. Build from a grounded UI brief.
</p>

<p align="center">
  <img src="https://img.shields.io/badge/release-0.0.1-1f6feb" alt="release 0.0.1" />
  <img src="https://img.shields.io/badge/plugin-Codex-0b1020" alt="Codex plugin" />
  <img src="https://img.shields.io/badge/models-Wan2.7%20%2B%20Qwen%20Omni-54c7ec" alt="Wan and Qwen Omni" />
  <img src="https://img.shields.io/badge/license-MIT-34d399" alt="MIT license" />
</p>

# Frontend Vibe Suite Plugin

`frontend-vibe-suite-plugin` packages a local Codex plugin that inserts a visual prototype loop into frontend vibecoding:

1. run a style interview
2. generate Wan2.7 concept prompts
3. create a short UI showcase video
4. translate that video with Qwen Omni
5. hand a structured brief into normal coding workflows

## Why this exists

Most frontend codegen jumps from a thin request straight into JSX and CSS. This repo adds a visual middle layer so implementation is anchored by:

- a clarified style brief
- a generated visual artifact
- a translated UI brief
- an implementation handoff

That changes the workflow from "guess and build" to "design, read back, then build."

## What ships in `0.0.1`

- `frontend-style-interview` for multi-round style discovery
- `render_prompt_pack.py` for Wan and Omni prompt generation
- `run_visual_loop.py` for wrapping existing local Wan image and video skills
- `video_to_ui_brief.py` for Qwen Omni video-to-UI translation
- `build_handoff.py` for implementation-ready JSON and Markdown handoff files
- example briefs and example generated artifacts
- local marketplace metadata for Codex plugin loading

## Quick Start

From the repository root:

```bash
python3 plugins/frontend-vibe-suite/scripts/render_prompt_pack.py \
  --brief plugins/frontend-vibe-suite/examples/frontend-style-brief.example.json \
  --output plugins/frontend-vibe-suite/examples/frontend-prompt-pack.example.json
```

```bash
python3 plugins/frontend-vibe-suite/scripts/build_handoff.py \
  --style-brief plugins/frontend-vibe-suite/examples/frontend-style-brief.example.json \
  --translated-brief plugins/frontend-vibe-suite/examples/video-ui-brief.example.json \
  --prompt-pack plugins/frontend-vibe-suite/examples/frontend-prompt-pack.example.json \
  --output-json plugins/frontend-vibe-suite/examples/build-handoff.example.json \
  --output-md plugins/frontend-vibe-suite/examples/build-handoff.example.md
```

## Workflow

```text
Style interview
  -> Prompt pack
  -> Wan image/video generation
  -> Qwen Omni translation
  -> Build handoff
  -> Frontend implementation
```

## Repository Layout

```text
.
├── .agents/plugins/marketplace.json
├── assets/
│   └── frontend-vibe-suite-hero.svg
├── plugins/
│   └── frontend-vibe-suite/
│       ├── .codex-plugin/plugin.json
│       ├── skills/
│       ├── scripts/
│       ├── examples/
│       └── README.md
├── CHANGELOG.md
├── LICENSE
└── README.md
```

## Configuration

Required:

- `DASHSCOPE_API_KEY`

Optional:

- `DASHSCOPE_BASE_URL`
- `QWEN_OMNI_MODEL`

Template env file:

- `plugins/frontend-vibe-suite/.env.example`

## Limits in `0.0.1`

- video translation still expects a public `video_url`
- the Wan wrapper reuses existing local Wan skills instead of shipping its own SDK client
- implementation ends at handoff generation, not automatic code patching

## Publish to GitHub

This repository is already initialized locally on branch `main`.

```bash
cd /Users/kkellyoffical/frontend-vibe-suite-plugin
git remote add origin <your-github-repo-url>
git push -u origin main --tags
```

## License

MIT
