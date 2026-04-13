# Frontend Build Handoff

## Product Context
- Product: AI operations dashboard
- Surface: desktop-first web app
- Primary goal: help operators scan system health, spot anomalies, and act quickly
- Users: ops lead, support engineer, founder reviewing status

## Visual System
- Brand mood: precise, calm, high-signal, premium
- Layout direction: left navigation, wide workspace, compact top filters, right-side detail drawer
- Density: dense but readable
- Color direction: charcoal base with cool neutral surfaces and one cyan action accent
- Typography direction: clean grotesk sans for UI with a tighter data-oriented scale
- Translated tokens: {"surface": "dark neutral", "accent": "cyan", "radius": "small", "shadow": "minimal"}

## Implementation Requirements
Must have:
- status summary row
- alerts timeline
- chart area
- task queue
- detail drawer

Page regions:
- left navigation rail
- top filter and status bar
- primary chart workspace
- alerts and task queue column
- detail drawer

Components:
- status chips
- metric strip
- line chart
- alerts list
- queue table
- slide-over details panel

Interactions:
- filter chips update active state
- hover reveals richer data on charts
- row click opens detail drawer

Motion:
- short panel slide-in
- chart value easing
- subtle highlight pulse on critical rows

Technical constraints:
- Next.js app router
- Tailwind CSS
- desktop and tablet support
- WCAG AA contrast

Acceptance criteria:
- operators can understand state in under 10 seconds
- critical alerts are obvious without scrolling
- layout remains stable with long labels

## Anti-goals
- marketing hero language
- glassmorphism
- oversized cards
- purple-heavy palette

## Open Questions
- mobile collapse behavior is not visible
- chart tooltip content is implied but not fully shown

## Coding Prompt
Implement this frontend strictly from the translated UI brief and the original style brief.
Product: AI operations dashboard
Primary surface: desktop-first web app
Primary goal: help operators scan system health, spot anomalies, and act quickly
Target users: ops lead, support engineer, founder reviewing status
Brand mood: precise, calm, high-signal, premium
Layout direction: left navigation, wide workspace, compact top filters, right-side detail drawer
Density: dense but readable
Color direction: charcoal base with cool neutral surfaces and one cyan action accent
Typography direction: clean grotesk sans for UI with a tighter data-oriented scale
Motion direction: short purposeful reveals, panel slides, subtle chart transitions
Content tone: operational and direct
Visual references: Linear, Stripe Dashboard
Must-have elements:
- status summary row
- alerts timeline
- chart area
- task queue
- detail drawer
Anti-goals:
- marketing hero language
- glassmorphism
- oversized cards
- purple-heavy palette
Technical constraints:
- Next.js app router
- Tailwind CSS
- desktop and tablet support
- WCAG AA contrast
Acceptance criteria:
- operators can understand state in under 10 seconds
- critical alerts are obvious without scrolling
- layout remains stable with long labels
Preserve the hierarchy, visual tone, motion attitude, and anti-goals. Do not improvise new product directions. Call out any ambiguity that remains after the video translation.

Implement the approved frontend using the merged handoff below. Keep the layout, hierarchy, tokens, interactions, and anti-goals stable.

Style constraints:
- status summary row
- alerts timeline
- chart area
- task queue
- detail drawer

Translated regions and components:
- left navigation rail
- top filter and status bar
- primary chart workspace
- alerts and task queue column
- detail drawer
- status chips
- metric strip
- line chart
- alerts list
- queue table
- slide-over details panel
