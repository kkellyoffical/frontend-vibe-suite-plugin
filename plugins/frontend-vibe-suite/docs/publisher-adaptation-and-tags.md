# Publisher Adaptation and Tags

This document makes the plugin's publishing contract explicit.

It answers three questions:

1. what this bundle is adapted for
2. which hosts are first-class targets
3. which tags and labels should be treated as canonical

The machine-readable source of truth is [`../data/publisher-metadata.json`](../data/publisher-metadata.json).

Runtime-facing requirements live separately in [`../data/runtime-contract.json`](../data/runtime-contract.json) so release metadata and runtime behavior do not drift.

## Publishing Identity

- Package name: `frontend-vibe-suite`
- Display name: `Frontend Vibe Suite`
- Family: `bundle-plugin`
- Bundle format: `codex`
- Host targets: `codex`, `openclaw`
- Source repo: `kkellyoffical/frontend-vibe-suite-plugin`
- Source path: `plugins/frontend-vibe-suite`
- Channel: `community`

## Host Adaptation

### Codex

Primary authoring surface.

Expected to consume:

- `.codex-plugin/plugin.json`
- `skills/`
- docs, examples, and local helper scripts

### OpenClaw

Compatible bundle target.

This bundle is intentionally shaped so OpenClaw can map:

- skill roots
- MCP defaults when present
- compatible hook-pack roots if later added

OpenClaw bundle mapping is selective. This bundle should be described as:

- portable at the content level
- not a native OpenClaw runtime plugin
- source-linked and capability-mapped

### ClawHub

Registry target for distribution.

Publish as:

- family: `bundle-plugin`
- format: `codex`
- host targets: `codex,openclaw`

Do not describe it as a native OpenClaw plugin unless a separate `openclaw.plugin.json` implementation exists.

## Canonical Tag Taxonomy

These tags are intentionally grouped instead of treated as one flat bag.

### Capability tags

- `frontend-development`
- `design-to-code`
- `prompt-routing`
- `component-library-routing`
- `release-preflight`

### Framework tags

- `react`
- `nextjs`
- `vue`
- `nuxt`
- `angular`
- `svelte`
- `solid`
- `web-components`

### Modality tags

- `wan2.7`
- `qwen-omni`
- `image-generation`
- `video-generation`
- `video-understanding`

### Delivery tags

- `dashboard`
- `workspace`
- `admin`
- `commerce`
- `documentation`
- `mobile`

### Library tags

- `react-aria`
- `radix-ui`
- `shadcn-ui`
- `mui`
- `ant-design`
- `chakra-ui`
- `mantine`
- `ark-ui`
- `zagjs`
- `primevue`
- `primeng`
- `primereact`
- `quasar`
- `element-plus`
- `naive-ui`
- `vuetify`
- `bits-ui`
- `melt-ui`
- `lit`
- `shoelace`
- `stencil`
- `daisyui`
- `ionic`

## Quality Bar

Before publishing a new version:

1. version in `.codex-plugin/plugin.json` matches the release target
2. version badge in root `README.md` matches
3. hero asset version matches
4. changelog contains the release entry
5. tests pass
6. JSON catalogs validate
7. release metadata still matches the repo source path and package name
8. `clean_release_tree.py` has been run so no bytecode artifacts are packed

## Why this file exists

Without an explicit publishing contract, the repo can drift into:

- mismatched version numbers
- unstable or incomplete tags
- ambiguous host claims
- ClawHub publish commands assembled differently each time

This file keeps those concerns visible and auditable.
