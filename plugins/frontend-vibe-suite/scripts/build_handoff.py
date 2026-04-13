#!/usr/bin/env python3
import argparse
import json
from pathlib import Path


def load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def list_or_empty(value):
    if isinstance(value, list):
        return value
    if value in (None, ""):
        return []
    return [value]


def bullet(values) -> str:
    values = list_or_empty(values)
    if not values:
        return "- none"
    return "\n".join(f"- {item}" for item in values)


def merge_handoff(style_brief: dict, translated_payload: dict, prompt_pack: dict | None) -> dict:
    translated = translated_payload.get("brief", translated_payload)
    anti_goals = list_or_empty(style_brief.get("antiGoals"))
    ambiguities = list_or_empty(translated.get("ambiguities"))
    stack_targets = list_or_empty(style_brief.get("stackTargets"))
    component_preferences = list_or_empty(style_brief.get("componentPreferences"))
    scenario_profile = prompt_pack.get("scenario_profile") if prompt_pack else None
    library_route = style_brief.get("libraryRoute") if isinstance(style_brief.get("libraryRoute"), dict) else None
    if not library_route and isinstance(translated.get("libraryRoute"), dict):
        library_route = translated.get("libraryRoute")
    if not library_route and prompt_pack:
        library_route = prompt_pack.get("stack_profile", {}).get("library_route")

    coding_prompt_parts = []
    if prompt_pack and prompt_pack.get("build_handoff_prompt"):
        coding_prompt_parts.append(prompt_pack["build_handoff_prompt"])
    coding_prompt_parts.append(
        "Implement the approved frontend using the merged handoff below. "
        "Keep the layout, hierarchy, tokens, interactions, and anti-goals stable."
    )
    coding_prompt_parts.append(
        "Style constraints:\n"
        f"{bullet(style_brief.get('mustHave'))}\n\n"
        "Stack context:\n"
        f"{bullet(stack_targets)}\n{bullet(component_preferences)}\n\n"
        "Translated regions and components:\n"
        f"{bullet(translated.get('page_regions'))}\n{bullet(translated.get('components'))}"
    )
    if library_route:
        coding_prompt_parts.append(
            "Library route:\n"
            f"Primary: {library_route.get('primary')}\n"
            f"Fallbacks: {', '.join(list_or_empty(library_route.get('fallback')))}\n"
            f"Frameworks: {', '.join(list_or_empty(library_route.get('frameworks')))}\n"
            f"Mode: {library_route.get('mode')}\n"
            f"Reason: {library_route.get('reason')}\n"
            f"Caveats: {', '.join(list_or_empty(library_route.get('caveats')))}"
        )

    return {
        "product_context": {
            "product": style_brief.get("product"),
            "surface": style_brief.get("surface"),
            "primary_goal": style_brief.get("primaryGoal"),
            "users": list_or_empty(style_brief.get("users")),
        },
        "stack_context": {
            "targets": stack_targets,
            "component_preferences": component_preferences,
            "library_route": library_route,
        },
        "scenario_context": scenario_profile,
        "source_of_truth": {
            "style_brief_priority": True,
            "translated_video_brief_used": True,
            "anti_goals": anti_goals,
        },
        "visual_system": {
            "brand_mood": list_or_empty(style_brief.get("brandMood")),
            "layout_direction": style_brief.get("layoutDirection"),
            "density": style_brief.get("density"),
            "color_direction": style_brief.get("colorDirection"),
            "typography_direction": style_brief.get("typographyDirection"),
            "translated_tokens": translated.get("visual_tokens"),
            "translated_typography": translated.get("typography"),
            "translated_color": translated.get("color"),
            "translated_spacing": translated.get("spacing"),
        },
        "implementation_requirements": {
            "must_have": list_or_empty(style_brief.get("mustHave")),
            "page_regions": list_or_empty(translated.get("page_regions")),
            "components": list_or_empty(translated.get("components")),
            "interactions": list_or_empty(translated.get("interactions")),
            "motion": list_or_empty(translated.get("motion")),
            "implementation_hints": list_or_empty(translated.get("implementation_hints")),
            "technical_constraints": list_or_empty(style_brief.get("technicalConstraints")),
            "acceptance_criteria": list_or_empty(style_brief.get("acceptanceCriteria")),
        },
        "library_route": library_route,
        "open_questions": ambiguities,
        "coding_prompt": "\n\n".join(coding_prompt_parts),
    }


def to_markdown(handoff: dict) -> str:
    product = handoff["product_context"]
    visual = handoff["visual_system"]
    impl = handoff["implementation_requirements"]
    scenario = handoff.get("scenario_context") or {}
    library_route = handoff.get("library_route")
    library_route_block = ""
    if library_route:
        library_route_block = (
            f"- Library route: {json.dumps(library_route, ensure_ascii=False)}\n\n"
        )
    scenario_block = ""
    if scenario:
        scenario_block = (
            f"- Scenario: {scenario.get('label')} ({scenario.get('id')})\n"
            f"- Delivery shape: {scenario.get('deliveryShape')}\n"
            f"- Fallbacks: {', '.join(scenario.get('fallbackCandidates', []))}\n\n"
        )
    return (
        "# Frontend Build Handoff\n\n"
        "## Product Context\n"
        f"- Product: {product.get('product')}\n"
        f"- Surface: {product.get('surface')}\n"
        f"- Primary goal: {product.get('primary_goal')}\n"
        f"- Users: {', '.join(product.get('users', []))}\n\n"
        "## Scenario Context\n"
        f"{scenario_block}"
        "## Stack Context\n"
        f"- Targets: {', '.join(handoff.get('stack_context', {}).get('targets', []))}\n"
        f"- Component preferences: {', '.join(handoff.get('stack_context', {}).get('component_preferences', []))}\n\n"
        f"{library_route_block}"
        "## Visual System\n"
        f"- Brand mood: {', '.join(visual.get('brand_mood', []))}\n"
        f"- Layout direction: {visual.get('layout_direction')}\n"
        f"- Density: {visual.get('density')}\n"
        f"- Color direction: {visual.get('color_direction')}\n"
        f"- Typography direction: {visual.get('typography_direction')}\n"
        f"- Translated tokens: {json.dumps(visual.get('translated_tokens'), ensure_ascii=False)}\n\n"
        "## Implementation Requirements\n"
        f"Must have:\n{bullet(impl.get('must_have'))}\n\n"
        f"Page regions:\n{bullet(impl.get('page_regions'))}\n\n"
        f"Components:\n{bullet(impl.get('components'))}\n\n"
        f"Interactions:\n{bullet(impl.get('interactions'))}\n\n"
        f"Motion:\n{bullet(impl.get('motion'))}\n\n"
        f"Technical constraints:\n{bullet(impl.get('technical_constraints'))}\n\n"
        f"Acceptance criteria:\n{bullet(impl.get('acceptance_criteria'))}\n\n"
        "## Anti-goals\n"
        f"{bullet(handoff['source_of_truth'].get('anti_goals'))}\n\n"
        "## Open Questions\n"
        f"{bullet(handoff.get('open_questions'))}\n\n"
        "## Coding Prompt\n"
        f"{handoff.get('coding_prompt')}\n"
    )


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Create an implementation-ready frontend handoff from the style brief and translated video brief."
    )
    parser.add_argument("--style-brief", required=True)
    parser.add_argument("--translated-brief", required=True)
    parser.add_argument("--prompt-pack")
    parser.add_argument("--output-json", required=True)
    parser.add_argument("--output-md", required=True)
    args = parser.parse_args()

    style_brief = load_json(Path(args.style_brief))
    translated_brief = load_json(Path(args.translated_brief))
    prompt_pack = load_json(Path(args.prompt_pack)) if args.prompt_pack else None

    handoff = merge_handoff(style_brief, translated_brief, prompt_pack)

    output_json = Path(args.output_json)
    output_md = Path(args.output_md)
    output_json.parent.mkdir(parents=True, exist_ok=True)
    output_md.parent.mkdir(parents=True, exist_ok=True)

    output_json.write_text(json.dumps(handoff, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    output_md.write_text(to_markdown(handoff), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
