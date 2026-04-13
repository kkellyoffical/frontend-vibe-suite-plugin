---
name: frontend-library-router
description: Route frontend requests to the right component library family, primitive system, or Web Components stack across Vue, Svelte, Angular, Solid, React, and portable design systems.
---

# Frontend Library Router

Use this skill when the user is choosing a frontend component library, a primitive system, or a Web Components stack.

## Goal

Select the smallest library family that satisfies the request without boxing the user into the wrong framework.

## Ask First

If any of these are unclear, ask before recommending a library:

- target framework or framework family
- whether the user wants framework-native ergonomics or portability
- whether the user wants a full suite, headless primitives, or Web Components
- whether mobile, PWA, desktop, or enterprise CRUD is the primary shape
- whether Tailwind-only styling is acceptable

## Routing Workflow

1. Identify the primary framework family.
2. Identify whether the user wants behavior primitives, a full suite, or portable Web Components.
3. Identify the delivery shape: admin app, marketing site, mobile shell, hybrid app, or design system.
4. Recommend one primary route and one fallback.
5. When useful, run the routing script to produce a machine-readable `libraryRoute`.

## Default Routes

### Behavior First

- `Zag.js` when the user wants portable behavior and state logic.
- `Ark UI` when the user wants a broader primitive surface across React, Vue, Solid, and Svelte.

### Vue

- `PrimeVue` for the broad enterprise default.
- `Quasar` for app shells, PWA, mobile, desktop, and extension delivery.
- `Element Plus` for conventional admin and data-heavy interfaces.
- `Naive UI` for lighter, TypeScript-first Vue work.
- `Vuetify` for Material Design.
- `DaisyUI` when Tailwind-only styling is preferred.

### Angular

- `PrimeNG` for the broad Angular suite.
- `Ionic` when the app should behave like a mobile shell or hybrid app.

### React

- `React Aria` or `Radix UI` for accessibility-focused headless primitives.
- `Headless UI` for simpler React or Vue headless patterns.
- `shadcn/ui` for source-first Tailwind React stacks.
- `MUI`, `Ant Design`, `Chakra UI`, `Mantine`, or `PrimeReact` for full suites.

### Svelte

- `Bits UI` for unstyled primitives with tight markup control.
- `Melt UI` for Svelte builders and custom component assembly.

### Web Components / Portable UI

- `Lit` when the user wants the cleanest Web Components base.
- `Shoelace` when the user wants ready-made portable application components.
- `Stencil` when the goal is to ship one component package across frameworks.
- `FAST` or `Fluent UI Web Components` for Microsoft-flavored enterprise systems.
- `Spectrum Web Components`, `Carbon Web Components`, or `Vaadin` for design-system-backed enterprise UI.
- `Material Web` when Material 3 is explicitly required.

## Output

Return a compact decision note with:

- `libraryRoute.primary`
- `libraryRoute.fallback`
- `libraryRoute.frameworks`
- `libraryRoute.mode`
- `libraryRoute.reason`
- `libraryRoute.caveats`

Example shape:

```json
{
  "libraryRoute": {
    "primary": "PrimeVue",
    "fallback": ["Element Plus", "Quasar"],
    "frameworks": ["Vue"],
    "mode": "framework-native suite",
    "reason": "broad enterprise Vue app with forms and tables",
    "caveats": ["Vue-only"]
  }
}
```

## Reference

Use [`docs/component-library-routing.md`](../../docs/component-library-routing.md) as the canonical matrix.

Script companion:

```bash
python3 plugins/frontend-vibe-suite/scripts/choose_library.py \
  --framework React \
  --mode headless \
  --delivery design-system \
  --tailwind
```
