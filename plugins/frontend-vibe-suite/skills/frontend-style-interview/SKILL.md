---
name: frontend-style-interview
description: Conduct a multi-round frontend design interview that locks product intent, interaction tone, visual style, anti-goals, and technical constraints before any code is generated.
---

# Frontend Style Interview

This skill exists to prevent weak frontend generation caused by thin requirements.

Run a compact but thorough interview. The goal is not endless questions. The goal is to get enough specificity to drive Wan prompts and implementation without guessing.

## Interview Areas

Cover these angles:

1. product and task
2. user type and usage context
3. visual mood and references
4. information density and layout rhythm
5. typography and color direction
6. motion and interaction feel
7. content tone and copy sharpness
8. target framework and component system
9. scenario and delivery shape
10. constraints and acceptance criteria
11. anti-goals

If the stack is still broad, split the decision into:

- framework family: Vue, Svelte, Angular, Solid, React, or Web Components
- component strategy: framework-native suite, headless primitives, or portable Web Components

## Prompting Rules

- Ask in rounds, not in one giant checklist.
- Each round should test one uncertainty from a different angle.
- If the user gives broad aesthetic words like `高级`, `科技感`, or `现代`, force them into concrete UI consequences.
- Always ask for anti-goals. They prevent prompt drift.
- If the user has no references, ask for contrasts instead:
  - more editorial or more operational
  - more calm or more theatrical
  - more spacious or more dense
  - more sharp or more soft

## Minimum Brief Fields

Before moving on, collect enough detail to write:

```json
{
  "product": "",
  "surface": "",
  "primaryGoal": "",
  "users": [],
  "brandMood": [],
  "visualReferences": [],
  "promptScenario": "",
  "deliveryShape": "",
  "layoutDirection": "",
  "density": "",
  "colorDirection": "",
  "typographyDirection": "",
  "motionDirection": "",
  "contentTone": "",
  "stackTargets": [],
  "componentPreferences": [],
  "mustHave": [],
  "antiGoals": [],
  "technicalConstraints": [],
  "acceptanceCriteria": []
}
```

`stackTargets` should list the chosen framework family or component system family, not just a package name.
`componentPreferences` should list the preferred primitive or component libraries, for example `PrimeVue`, `Ark UI`, `Bits UI`, `Lit`, or `DaisyUI`.
If a separate routing step is used, keep the concrete decision in `libraryRoute` and mirror only the primary choice into `stackTargets`.
Use `frontend-library-router` when the user has only specified product shape and framework family, not an actual library.
Use `promptScenario` for a concrete UI situation such as `analytics-dashboard`, `admin-crud`, `mobile-hybrid-shell`, or `design-system-docs`.
Use `deliveryShape` for a broader shape such as `dashboard`, `workspace`, `landing`, `commerce`, `documentation`, or `mobile`.

## Exit Criteria

You are done only when:

- the brief can drive a visual prototype without guessing
- the anti-goals are concrete
- the primary surface is explicit
- the scenario or delivery shape is explicit, or intentionally broad
- the target stack or component model is explicit, or intentionally left broad
- the implementation constraints are known or intentionally assumed

## Hand-off

When complete, pass the brief into `render_prompt_pack.py` and move to the video prototype phase.
