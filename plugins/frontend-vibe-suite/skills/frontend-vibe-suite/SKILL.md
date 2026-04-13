---
name: frontend-vibe-suite
description: Run a multimodal frontend workflow that interviews for design intent, generates Wan2.7 prompts and showcase videos, translates the resulting video with Qwen Omni, and then hands a grounded brief back to implementation skills.
---

# Frontend Vibe Suite

Use this skill when the user wants a stronger frontend ideation loop than direct code generation.

This workflow is for cases where the right output is:

1. a clarified style and product brief
2. a generated concept image or short design video
3. a structured translation of that visual direction back into frontend language
4. implementation using the normal coding path

## Use When

- the user wants `vibecoding` for frontend work
- the brief is visual, product-heavy, or under-specified
- the user wants to lock style before writing code
- the user wants Wan2.7 and Qwen Omni in the loop

## Do Not Use When

- the user already has a final Figma or production-ready spec
- the task is a narrow bug fix, refactor, or one-off component edit
- the user only wants code review or a design critique

## Workflow

### Phase 1: Interview the style from multiple angles

Invoke `frontend-style-interview` and keep going until these are specific:

- product type and primary surface
- target users and operating context
- brand temperature and emotional tone
- density and interaction style
- color and typography direction
- motion attitude
- anti-goals
- implementation constraints

The output of this phase is a concise JSON or bullet brief that can drive prompt generation.

### Phase 2: Render a prompt pack

Take the agreed brief and render the prompt pack:

```bash
python3 plugins/frontend-vibe-suite/scripts/render_prompt_pack.py \
  --brief path/to/frontend-style-brief.json \
  --output path/to/frontend-prompt-pack.json
```

That prompt pack contains:

- `wan_image_prompt`
- `wan_video_prompt`
- `omni_translation_prompt`
- `build_handoff_prompt`

### Phase 3: Generate visual prototypes

Use the prompt pack with the existing local skills:

- `wan27-image` for still concept frames
- `wan27-video` for a short design showcase video

Or use the wrapper:

```bash
python3 plugins/frontend-vibe-suite/scripts/run_visual_loop.py \
  --prompt-pack path/to/frontend-prompt-pack.json \
  --manifest-output path/to/visual-run.json \
  --image-output path/to/concept/frame.png \
  --video-output path/to/concept/showcase.mp4
```

Keep the video short and concrete. Good defaults:

- 5 to 8 seconds
- one primary flow or state transition
- visible hierarchy, navigation, content blocks, and motion style

### Phase 4: Translate the video back into frontend language

Invoke `video-to-ui-brief` or run the translator directly:

```bash
python3 plugins/frontend-vibe-suite/scripts/video_to_ui_brief.py \
  --video-url https://example.com/design-preview.mp4 \
  --prompt-pack path/to/frontend-prompt-pack.json \
  --output path/to/video-ui-brief.json
```

The translated brief should capture:

- layout regions
- design tokens
- interaction model
- motion cues
- content structure
- likely implementation stack hints

### Phase 5: Implement on the normal path

First, build the implementation handoff:

```bash
python3 plugins/frontend-vibe-suite/scripts/build_handoff.py \
  --style-brief path/to/frontend-style-brief.json \
  --translated-brief path/to/video-ui-brief.json \
  --prompt-pack path/to/frontend-prompt-pack.json \
  --output-json path/to/build-handoff.json \
  --output-md path/to/build-handoff.md
```

Once the visual direction is grounded, continue with:

- `frontend-skill` for visual execution
- `ui-ux-pro-max` for systemized layout, tokens, states, and interaction polish
- `visual-verdict` for iterative screenshot QA
- `web-clone` only if the user is cloning a live reference site

Treat the build handoff as the implementation source of truth unless the user overrides it.

## Required Outputs

Before you finish this skill, produce:

1. a style brief
2. a prompt pack
3. a design video or an explicit blocker
4. a translated UI brief
5. a build handoff file or prompt

## Notes

- Ask enough questions to remove ambiguity, but keep each round focused.
- The goal is not cinematic spectacle. The goal is a faithful visual artifact that is easy to translate into code.
- If the Wan result is too vague, revise the brief and rerender the prompt pack instead of forcing implementation from a weak prototype.
