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
8. constraints, stack, and acceptance criteria
9. anti-goals

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
  "layoutDirection": "",
  "density": "",
  "colorDirection": "",
  "typographyDirection": "",
  "motionDirection": "",
  "contentTone": "",
  "mustHave": [],
  "antiGoals": [],
  "technicalConstraints": [],
  "acceptanceCriteria": []
}
```

## Exit Criteria

You are done only when:

- the brief can drive a visual prototype without guessing
- the anti-goals are concrete
- the primary surface is explicit
- the implementation constraints are known or intentionally assumed

## Hand-off

When complete, pass the brief into `render_prompt_pack.py` and move to the video prototype phase.
