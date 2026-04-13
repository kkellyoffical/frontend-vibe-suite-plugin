# Frontend Vibe Suite Plugin

`frontend-vibe-suite-plugin` is a GitHub-ready local Codex plugin repository for a multimodal frontend workflow:

1. interview for style and product intent
2. generate Wan2.7 image and video prompts
3. create a short UI showcase video
4. translate that video into a structured frontend brief with Qwen Omni
5. hand the result into normal frontend coding skills

## Repository Layout

```text
.
├── .agents/plugins/marketplace.json
├── plugins/
│   └── frontend-vibe-suite/
│       ├── .codex-plugin/plugin.json
│       ├── skills/
│       ├── scripts/
│       ├── examples/
│       └── README.md
├── .gitignore
├── LICENSE
└── README.md
```

## Included Plugin

- `frontend-vibe-suite`

The plugin bundles:

- style interview workflow
- prompt-pack generation
- Wan wrapper runner
- Qwen Omni video translation
- implementation handoff generation

## Local Usage

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

## Configuration

Set `DASHSCOPE_API_KEY` before calling the Wan or Qwen scripts.

Optional:

- `DASHSCOPE_BASE_URL`
- `QWEN_OMNI_MODEL`

The plugin also ships `plugins/frontend-vibe-suite/.env.example`.

## GitHub Publishing

This directory is already initialized as a git repository with branch `main`.

Typical next steps:

```bash
cd /Users/kkellyoffical/frontend-vibe-suite-plugin
git add .
git commit -m "Package multimodal frontend vibe workflow as a reusable Codex plugin"
git remote add origin <your-github-repo-url>
git push -u origin main
```

If you want to publish it as open source, review:

- plugin metadata
- author fields
- example assets
- whether your local marketplace naming should stay `kkellyoffical-local`

## Current Limits

- media translation still expects a public `video_url`
- the visual loop wrapper reuses existing local Wan skills instead of bundling its own SDK client
- implementation is still handoff-driven, not direct code patch generation
