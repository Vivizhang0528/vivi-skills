#!/usr/bin/env python3
"""Build an editable, backend-neutral academic-slide progress plan.

Input JSON: {"slides": [{"id": "cover", "role": "cover"},
{"id": "toc", "role": "contents"}, {"id": "p1", "role": "part", "part": "1"},
{"id": "s1", "role": "content", "part": "1"}, ...]}
Use roles conclusion/limitation for main pages, references/qa for completed
main progress, and appendix for an independent supplementary rail.
"""
import argparse
import json
import sys
from pathlib import Path

MAIN_ROLES = {"part", "content", "conclusion", "limitation"}
ROLES = MAIN_ROLES | {"cover", "contents", "references", "qa", "appendix"}


def build_plan(slides, x=40.0, width=640.0, y=397.0, gap=5.0):
    if len(slides) < 3 or [s.get("role") for s in slides[:2]] != ["cover", "contents"]:
        raise ValueError("Start with cover, then contents.")
    ids = [s.get("id") for s in slides]
    if any(not isinstance(v, str) or not v.strip() for v in ids) or len(set(ids)) != len(ids):
        raise ValueError("Every slide must have a unique, nonempty string id.")
    groups, by_part, tail = [], {}, False
    for slide in slides[2:]:
        role = slide.get("role")
        if role not in ROLES - {"cover", "contents"}:
            raise ValueError("Unknown or misplaced role: " + str(role))
        if role not in MAIN_ROLES:
            tail = True
            if slide.get("part") is not None:
                raise ValueError("Tail pages must not carry a main part.")
            continue
        if tail:
            raise ValueError("Keep main Parts before references, Q&A and appendix.")
        part = "" if slide.get("part") is None else str(slide["part"]).strip()
        if not part:
            raise ValueError("Main pages require a part.")
        if not groups or groups[-1]["part"] != part:
            if part in by_part or role != "part":
                raise ValueError("Each Part must be contiguous and begin with a part divider.")
            group = {"part": part, "target": slide["id"], "slides": []}
            groups.append(group)
            by_part[part] = group
        elif role == "part":
            raise ValueError("Use one opening divider per Part.")
        groups[-1]["slides"].append(slide["id"])
    if not groups:
        raise ValueError("At least one main Part is required.")
    if width <= gap * max(len(groups) - 1, 0):
        raise ValueError("Rail width is too small.")
    main_n = sum(len(g["slides"]) for g in groups)
    appendix = [s["id"] for s in slides if s["role"] == "appendix"]
    part_segments, left = [], x
    usable = width - gap * (len(groups) - 1)
    for group in groups:
        size = usable * len(group["slides"]) / main_n
        part_segments.append({"label": group["part"], "target": group["target"],
                              "x": left, "width": size})
        left += size + gap
    output = []
    for number, slide in enumerate(slides, 1):
        role, current, fraction = slide["role"], None, 0.0
        segments = [dict(s) for s in part_segments]
        stage = "intro"
        if role in MAIN_ROLES:
            stage = "main"
            current = next(i for i, g in enumerate(groups) if g["part"] == str(slide["part"]))
            pages = groups[current]["slides"]
            fraction = pages.index(slide["id"]) / (len(pages) - 1) if len(pages) > 1 else 1.0
        elif role in {"references", "qa"}:
            stage, current, fraction = "completed", len(groups) - 1, 1.0
        elif role == "appendix":
            stage, current, fraction = "appendix", appendix.index(slide["id"]), 1.0
            if width <= gap * (len(appendix) - 1):
                raise ValueError("Rail width is too small for the appendix.")
            size = (width - gap * (len(appendix) - 1)) / len(appendix)
            segments = [{"label": str(i + 1), "target": sid,
                         "x": x + i * (size + gap), "width": size}
                        for i, sid in enumerate(appendix)]
        cursor = x
        for index, segment in enumerate(segments):
            fill = 0.0 if current is None else 1.0 if index < current else fraction if index == current else 0.0
            segment["fill"] = round(fill, 6)
            segment["state"] = "current" if index == current else "complete" if fill == 1 else "upcoming"
            if index == current:
                cursor = segment["x"] + segment["width"] * fraction
        output.append({"slide_id": slide["id"], "page": number, "stage": stage,
                       "track_y": y, "track_height": 2.0,
                       "cursor": {"x": round(cursor, 4), "y": y + 1.0, "radius": 3.0},
                       "segments": segments})
    return {"main_page_count": main_n, "part_count": len(groups),
            "appendix_page_count": len(appendix), "pages": output,
            "reminder": "Reserve footer space; verify rendered citations, page numbers and rails do not overlap."}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest", type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--x", type=float, default=40.0)
    parser.add_argument("--width", type=float, default=640.0)
    parser.add_argument("--y", type=float, default=397.0)
    parser.add_argument("--gap", type=float, default=5.0)
    args = parser.parse_args()
    try:
        source = json.loads(args.manifest.read_text(encoding="utf-8-sig"))
        slides = source["slides"] if isinstance(source, dict) else source
        result = build_plan(slides, args.x, args.width, args.y, args.gap)
    except (OSError, ValueError, KeyError, TypeError) as exc:
        parser.error(str(exc))
    text = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        args.output.write_text(text, encoding="utf-8")
    else:
        sys.stdout.write(text)


if __name__ == "__main__":
    main()

