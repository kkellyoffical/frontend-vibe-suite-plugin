---
name: frontend-build-handoff
description: Merge the style brief and translated video brief into an implementation-ready handoff for frontend coding skills and agents.
---

# Frontend Build Handoff

Use this skill after:

- the style interview is done
- the prompt pack exists
- a design video has been translated into a UI brief
- optional stack targets or component preferences are known

If the stack choice is still broad, resolve it first with `frontend-library-router`.

## Goal

Produce a build handoff that is strict enough for implementation and explicit enough to avoid drifting away from the approved visual direction.

## Inputs

- `style_brief.json`
- `video_ui_brief.json`
- optional `prompt_pack.json`

## Script

Run:

```bash
python3 plugins/frontend-vibe-suite/scripts/build_handoff.py \
  --style-brief path/to/style-brief.json \
  --translated-brief path/to/video-ui-brief.json \
  --prompt-pack path/to/frontend-prompt-pack.json \
  --output-json path/to/build-handoff.json \
  --output-md path/to/build-handoff.md
```

## Required Output

The handoff should contain:

- product and surface context
- immutable anti-goals
- visual system constraints
- stack targets and component preferences
- recommended component family or Web Components route when the stack is broad
- page regions and components
- interaction and motion requirements
- implementation constraints
- unresolved questions
- a coding prompt that can be handed to `frontend-skill` or `ui-ux-pro-max`

If the style brief names a stack, keep that stack visible in the handoff instead of collapsing it into generic React language.

## Rule

Do not let the implementation step silently override the approved visual direction. If the translated brief conflicts with the original style brief, surface the conflict explicitly and favor the original brief unless the user says otherwise.
