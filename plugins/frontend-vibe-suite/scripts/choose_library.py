#!/usr/bin/env python3
import argparse
import json
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent
CATALOG_PATH = SCRIPT_DIR.parent / "data" / "component-libraries.json"


def load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def list_or_empty(value):
    if isinstance(value, list):
        return [str(item) for item in value]
    if value in (None, ""):
        return []
    return [str(value)]


def infer_frameworks(brief: dict, framework_args: list[str]) -> list[str]:
    frameworks = [item.strip() for item in framework_args if item.strip()]
    if frameworks:
        return frameworks
    frameworks = []
    for item in list_or_empty(brief.get("stackTargets")):
        item_lower = item.lower()
        if "next" in item_lower:
            frameworks.extend(["Next.js", "React"])
        elif "nuxt" in item_lower:
            frameworks.extend(["Nuxt", "Vue"])
        elif "react" in item_lower:
            frameworks.append("React")
        elif "vue" in item_lower:
            frameworks.append("Vue")
        elif "angular" in item_lower:
            frameworks.append("Angular")
        elif "svelte" in item_lower:
            frameworks.append("Svelte")
        elif "solid" in item_lower:
            frameworks.append("Solid")
        elif "web component" in item_lower or "lit" in item_lower:
            frameworks.append("Web Components")
        elif "tailwind" in item_lower:
            frameworks.append("Tailwind CSS")
    return list(dict.fromkeys(frameworks))


def score_library(library: dict, frameworks: list[str], mode: str, delivery: str, tailwind: bool, portable: bool) -> int:
    score = 0
    lib_frameworks = set(library.get("frameworks", []))
    if not frameworks:
        score += 1
    else:
        for framework in frameworks:
            if framework in lib_frameworks:
                score += 5
            elif framework == "Next.js" and "React" in lib_frameworks:
                score += 4
            elif framework == "Nuxt" and "Vue" in lib_frameworks:
                score += 4
            elif framework == "Tailwind CSS" and library.get("tailwindFriendly"):
                score += 2

    if portable:
        if library.get("portability") == "high":
            score += 5
        if "Web Components" in lib_frameworks:
            score += 3

    if mode and library.get("mode") == mode:
        score += 8
    elif mode == "headless" and library.get("mode") in {"headless", "behavior-first"}:
        score += 4
    elif mode == "portable" and library.get("mode") in {"portable", "behavior-first"}:
        score += 4
    elif mode == "full-suite" and library.get("mode") in {"full-suite", "app-framework"}:
        score += 4
    elif mode == "source-first" and library.get("mode") == "source-first":
        score += 4
    elif mode == "css-layer" and library.get("mode") == "css-layer":
        score += 4
    elif mode:
        score -= 2

    if delivery:
        for item in library.get("delivery", []):
            if delivery == item:
                score += 4
            elif delivery in {"dashboard", "admin", "enterprise"} and item in {"dashboard", "admin", "enterprise", "crud"}:
                score += 3
            elif delivery in {"mobile", "hybrid app", "pwa"} and item in {"mobile", "hybrid app", "pwa"}:
                score += 3
            elif delivery == "design system" and item in {"design system", "portable UI"}:
                score += 3

    if tailwind and library.get("tailwindFriendly"):
        score += 3
    if not tailwind and library.get("styling") not in {"tailwind", "unstyled"}:
        score += 1
    return score


def choose_route(catalog: dict, frameworks: list[str], mode: str, delivery: str, tailwind: bool, portable: bool) -> dict:
    libraries = catalog.get("libraries", [])
    ranked = sorted(
        libraries,
        key=lambda item: score_library(item, frameworks, mode, delivery, tailwind, portable),
        reverse=True,
    )
    primary = ranked[0]
    fallbacks = [item["name"] for item in ranked[1:4]]
    reason_bits = []
    if frameworks:
        reason_bits.append(f"framework fit for {', '.join(frameworks)}")
    if mode:
        reason_bits.append(f"{mode} delivery mode")
    if delivery:
        reason_bits.append(f"{delivery} product shape")
    if tailwind:
        reason_bits.append("Tailwind-friendly path")
    if portable:
        reason_bits.append("high portability")

    return {
        "libraryRoute": {
            "primary": primary["name"],
            "fallback": fallbacks,
            "frameworks": primary["frameworks"],
            "mode": primary["mode"],
            "reason": ", ".join(reason_bits) or primary["reason"],
            "caveats": [
                f"styling: {primary['styling']}",
                f"docs: {primary['officialDocs']}"
            ]
        }
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Choose a frontend component library route from stack, mode, delivery, and portability hints."
    )
    parser.add_argument("--brief", help="Optional style brief JSON path.")
    parser.add_argument("--framework", action="append", default=[], help="Framework hint such as React, Vue, Angular, Svelte, Web Components.")
    parser.add_argument(
        "--mode",
        default="",
        choices=["", "behavior-first", "headless", "full-suite", "portable", "source-first", "css-layer", "app-framework"],
        help="Preferred library mode.",
    )
    parser.add_argument("--delivery", default="", help="Product shape such as dashboard, admin, design system, mobile, hybrid app, pwa.")
    parser.add_argument("--tailwind", action="store_true", help="Prefer Tailwind-friendly options.")
    parser.add_argument("--portable", action="store_true", help="Prefer high-portability or Web Components routes.")
    parser.add_argument("--output", help="Optional output JSON path.")
    args = parser.parse_args()

    brief = load_json(Path(args.brief)) if args.brief else {}
    frameworks = infer_frameworks(brief, args.framework)
    route = choose_route(
        catalog=load_json(CATALOG_PATH),
        frameworks=frameworks,
        mode=args.mode,
        delivery=args.delivery,
        tailwind=args.tailwind,
        portable=args.portable,
    )

    if args.output:
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(json.dumps(route, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    else:
        print(json.dumps(route, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
