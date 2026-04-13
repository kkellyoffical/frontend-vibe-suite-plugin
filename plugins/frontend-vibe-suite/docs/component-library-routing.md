# Component Library Routing

Use this reference when the user wants help choosing a frontend component library, primitive system, or Web Components stack.

## Default Routing

- Behavior-first primitives with custom styling: `Zag.js`, `Ark UI`
- Vue-first app suites: `PrimeVue`, `Element Plus`, `Naive UI`, `Vuetify`, `Quasar`
- Angular-first app suites: `PrimeNG`
- React-first app suites: `PrimeReact`
- Svelte-first primitives: `Bits UI`, `Melt UI`
- Framework-neutral Web Components: `Lit`, `Shoelace`, `Stencil`, `FAST`, `Fluent UI Web Components`, `Spectrum Web Components`, `Carbon Web Components`, `Vaadin`, `Material Web`
- CSS-only Tailwind layer: `DaisyUI`

## Library Notes

### Framework-Neutral Primitives

- `Zag.js`: behavior and accessibility logic built on finite-state machines. Route here when the UI should stay custom and portable across frameworks.
- `Ark UI`: headless primitives built on Zag with current coverage for React, Solid, Vue, and Svelte. Route here when the user wants a broader primitive surface than raw Zag.
- `Radix Vue`: Vue and Nuxt unstyled primitives with Vue-native composition. Route here when the stack is Vue-first and the user wants Radix-style ergonomics.

### Vue Ecosystem

- `PrimeVue`: broad enterprise Vue 3 suite with styled or unstyled mode, theming, and form support. Route here for the widest default Vue toolkit.
- `Quasar`: opinionated Vue app framework for SPA, PWA, mobile, desktop, and browser extension delivery. Route here when the user wants an app shell, not just a component set.
- `Element Plus`: conventional enterprise Vue 3 library with strong docs and admin/data UI fit. Route here for form-heavy dashboards and internal tools.
- `Naive UI`: TypeScript-first Vue 3 library with treeshakable components and theme overrides. Route here when the user wants a lighter Vue stack with modern ergonomics.
- `Vuetify`: Material Design Vue suite with mature ecosystem and Nuxt support. Route here when the user explicitly wants Material semantics.
- `DaisyUI`: Tailwind plugin with semantic classes and no JS dependency. Route here when the user wants portable styling on top of a Tailwind app.

### Angular Ecosystem

- `PrimeNG`: broad Angular suite with styled or unstyled mode and enterprise-friendly coverage. Route here for Angular apps that need a large component surface.
- `Ionic`: Angular, React, Vue, or script-include delivery with strong mobile and PWA fit. Route here when the app needs hybrid mobile behavior or app-shell patterns.

### React Ecosystem

- `PrimeReact`: broad React suite with styled or unstyled mode and enterprise support. Route here when the stack is React and the user wants PrimeTek parity.

### Svelte Ecosystem

- `Bits UI`: headless Svelte primitives with strong control over markup, snippets, and styling.
- `Melt UI`: Svelte builders for accessible component creation, useful when the user wants more explicit construction over wrapper components.

### Web Components and Cross-Framework Systems

- `Lit`: lowest-friction base for native Web Components that work with any framework or none.
- `Shoelace`: polished framework-agnostic component set for general-purpose application UI.
- `Ionic`: strong choice for hybrid mobile apps, gestures, and app-shell UX.
- `Stencil`: compiler for shipping one component package across multiple frameworks.
- `FAST` and `Fluent UI Web Components`: framework-neutral foundation and Microsoft-flavored enterprise UI layer.
- `Spectrum Web Components`: Adobe Spectrum as Web Components for accessible design-system-backed UI.
- `Carbon Web Components`: IBM Carbon as Web Components, with Angular, React, and Vue usage paths.
- `Vaadin`: enterprise Web Components for business apps, dashboards, and CRUD-heavy systems.
- `Material Web`: Material 3 Web Components that can be consumed across Lit, React, Vue, and Svelte.

## Routing Rules

1. If the user wants behavior portability across Vue, Svelte, Angular, and Solid, route first to `Zag.js`, `Ark UI`, or a Web Components stack.
2. If the user wants a framework-native UI suite, keep the choice inside that framework family.
3. If the user wants a design system that can outlive framework swaps, prefer Web Components or headless primitives over framework-bound suites.
4. If the user wants a Tailwind-only look with minimal runtime, route to `DaisyUI`.
5. If the user wants mobile or hybrid delivery, consider `Ionic` before defaulting to a desktop-only suite.
6. If the user wants Vue and has not specified a narrower preference, route by product shape:
   - enterprise admin or forms -> `PrimeVue` or `Element Plus`
   - app shell or multi-platform delivery -> `Quasar`
   - lighter, TS-first UI -> `Naive UI`
   - Material-first language -> `Vuetify`

## Prime Family Note

The PrimeTek ecosystem currently exposes official docs for `PrimeVue`, `PrimeNG`, and `PrimeReact`. I did not verify an official `PrimeSvelte` docs page in this pass, so do not auto-route to it without a live check.

## Source Links

- [Zag.js](https://zagjs.com/)
- [Ark UI](https://ark-ui.com/docs/overview/about)
- [Ark UI Svelte announcement](https://ark-ui.com/blog/introducing-ark-ui-svelte)
- [Radix Vue](https://www.radix-vue.com/)
- [PrimeVue](https://primevue.org/introduction/)
- [PrimeNG](https://v20.primeng.org/)
- [PrimeReact](https://primereact.org/)
- [Quasar](https://quasar.dev/)
- [Element Plus](https://element-plus.org/)
- [Naive UI](https://github.com/tusen-ai/naive-ui)
- [Vuetify](https://vuetifyjs.com/en/getting-started/installation/)
- [DaisyUI](https://daisyui.com/)
- [Bits UI](https://www.bits-ui.com/docs/introduction)
- [Melt UI](https://www.melt-ui.com/docs/introduction)
- [Lit](https://lit.dev/)
- [Shoelace](https://shoelace.style/)
- [Ionic](https://ionicframework.com/docs/)
- [Stencil](https://stenciljs.com/)
- [FAST](https://fast.design/docs/1.x/introduction/)
- [Fluent UI Web Components](https://learn.microsoft.com/en-us/fluent-ui/web-components/)
- [Spectrum Web Components](https://opensource.adobe.com/spectrum-web-components/)
- [Carbon Web Components](https://carbondesignsystem.com/developing/frameworks/web-components/)
- [Vaadin Design System](https://vaadin.com/design-system)
- [Material Web](https://material-web.dev/)
