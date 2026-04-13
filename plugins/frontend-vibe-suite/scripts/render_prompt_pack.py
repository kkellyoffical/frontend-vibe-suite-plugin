#!/usr/bin/env python3
import argparse
import json
from pathlib import Path


def load_brief(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def bullet_list(values) -> str:
    if not values:
        return "- none provided"
    return "\n".join(f"- {value}" for value in values)


def render_prompt_pack(brief: dict) -> dict:
    product = brief.get("product", "product")
    surface = brief.get("surface", "web application")
    goal = brief.get("primaryGoal", "deliver a clear primary user task")
    users = ", ".join(brief.get("users", [])) or "general users"
    mood = ", ".join(brief.get("brandMood", [])) or "clear, modern, high-signal"
    layout = brief.get("layoutDirection", "structured and readable")
    density = brief.get("density", "balanced")
    color = brief.get("colorDirection", "brand-aligned, readable contrast")
    typography = brief.get("typographyDirection", "clean sans-serif system")
    motion = brief.get("motionDirection", "restrained, meaningful transitions")
    content_tone = brief.get("contentTone", "product-facing, concise, useful")
    visual_refs = ", ".join(brief.get("visualReferences", [])) or "no explicit references"

    must_have = bullet_list(brief.get("mustHave", []))
    anti_goals = bullet_list(brief.get("antiGoals", []))
    constraints = bullet_list(brief.get("technicalConstraints", []))
    acceptance = bullet_list(brief.get("acceptanceCriteria", []))

    common_context = (
        f"Product: {product}\n"
        f"Primary surface: {surface}\n"
        f"Primary goal: {goal}\n"
        f"Target users: {users}\n"
        f"Brand mood: {mood}\n"
        f"Layout direction: {layout}\n"
        f"Density: {density}\n"
        f"Color direction: {color}\n"
        f"Typography direction: {typography}\n"
        f"Motion direction: {motion}\n"
        f"Content tone: {content_tone}\n"
        f"Visual references: {visual_refs}\n"
        f"Must-have elements:\n{must_have}\n"
        f"Anti-goals:\n{anti_goals}\n"
        f"Technical constraints:\n{constraints}\n"
        f"Acceptance criteria:\n{acceptance}"
    )

    wan_image_prompt = (
        "Create a polished UI concept frame for a modern digital product.\n"
        f"{common_context}\n"
        "Show a realistic product interface, not a moodboard. Preserve readable hierarchy, "
        "clear spacing, and believable product chrome. No watermark. No explanatory labels."
    )

    wan_video_prompt = (
        "Create a short showcase video of a frontend product experience.\n"
        f"{common_context}\n"
        "The video should reveal the page hierarchy, navigation, content rhythm, and motion language. "
        "Favor one concrete product flow over abstract camera movement. Keep the scene grounded in real UI."
    )

    omni_translation_prompt = (
        "Analyze this UI design video as a frontend lead. Return a structured brief that names layout regions, "
        "design tokens, interaction patterns, motion cues, content structure, component types, likely stack fit, "
        "and open ambiguities. Prefer concrete frontend language over cinematic commentary.\n"
        f"{common_context}"
    )

    build_handoff_prompt = (
        "Implement this frontend strictly from the translated UI brief and the original style brief.\n"
        f"{common_context}\n"
        "Preserve the hierarchy, visual tone, motion attitude, and anti-goals. "
        "Do not improvise new product directions. Call out any ambiguity that remains after the video translation."
    )

    return {
        "style_brief": brief,
        "wan_image_prompt": wan_image_prompt,
        "wan_video_prompt": wan_video_prompt,
        "omni_translation_prompt": omni_translation_prompt,
        "build_handoff_prompt": build_handoff_prompt,
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Render a multimodal prompt pack from a frontend style brief JSON file."
    )
    parser.add_argument("--brief", required=True, help="Path to the input style brief JSON.")
    parser.add_argument("--output", required=True, help="Path to write the prompt pack JSON.")
    args = parser.parse_args()

    brief_path = Path(args.brief)
    output_path = Path(args.output)

    prompt_pack = render_prompt_pack(load_brief(brief_path))
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as handle:
        json.dump(prompt_pack, handle, ensure_ascii=False, indent=2)
        handle.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
