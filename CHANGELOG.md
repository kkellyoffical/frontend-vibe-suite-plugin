# Changelog

## 0.0.4 - 2026-04-19

Publishing-hardening and metadata-transparency release.

Included:

- explicit publisher metadata for package family, host targets, and tag taxonomy
- explicit runtime contract covering env vars, network behavior, subprocesses, and file IO
- release preflight script enforcing version, metadata, and bundle hygiene checks
- repo-level `requirements.txt` documenting standard-library-only Python usage
- CI extended to validate publisher/runtime metadata and run release preflight
- removal of compiled Python bytecode from the release tree

## 0.0.2 - 2026-04-19

Quality, routing, and prompt-template release.

Included:

- component-library routing across React, Vue, Angular, Svelte, and Web Components
- machine-readable library catalog and chooser script
- scenario-aware prompt generation covering 20+ frontend situations
- scenario selector script and scenario profiles in examples
- scenario and library routing carried into prompt packs and build handoffs
- Python unit tests for routing, scenarios, and prompt/handoff generation
- GitHub Actions CI for script compilation, JSON validation, and tests

## 0.0.1 - 2026-04-13

Initial public repository release.

Included:

- standalone GitHub-ready repository layout
- local Codex plugin manifest and marketplace entry
- style interview workflow
- prompt-pack generation
- Wan image and video wrapper flow
- Qwen Omni video-to-UI translation
- implementation handoff generation
- example briefs and generated handoff artifacts
