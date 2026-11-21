#!/usr/bin/env python3
"""Scan local skill layers (L1 builtin, L2 installed) and rank them against keywords.

Dependency-free. Parses SKILL.md frontmatter with a minimal scalar parser, deduplicates
by skill name while keeping the highest version, and reports matches as Markdown or JSON.

The script only covers the two local layers. Remote layers are network calls handled
by the calling agent; this script cannot prove remote availability.
"""

import argparse
import json
import os
import re
import sys
from pathlib import Path
from typing import Iterable

FRONTMATTER_RE = re.compile(r"\A---\s*\n(?P<body>.*?)\n---", re.DOTALL)
FIELD_RE = re.compile(r"^([A-Za-z][A-Za-z0-9_-]*):\s*(?P<value>.*)$")
VERSION_RE = re.compile(r"\d+(?:\.\d+)*")
VERSION_DIR_RE = re.compile(r"^\d+\.\d+")
BLOCK_INDICATORS = {"|", ">", "|-", ">-", "|+", ">+"}
NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
MAX_DEPTH = 9
SKIP_DIRS = {"node_modules", "__pycache__", ".git", ".venv", "venv"}


def strip_scalar(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}:
        return value[1:-1]
    return value


def read_frontmatter(path: Path) -> dict:
    """Return scalar frontmatter fields, including folded multi-line values."""
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return {}
    match = FRONTMATTER_RE.match(text)
    if not match:
        return {}
    fields: dict[str, str] = {}
    current_key = None
    buffer: list[str] = []
    for raw in match.group("body").splitlines():
        field = FIELD_RE.match(raw)
        if field and not raw.startswith((" ", "\t")):
            if current_key and buffer:
                fields[current_key] = " ".join(buffer).strip()
            current_key = field.group(1)
            value = strip_scalar(field.group("value"))
            if value in BLOCK_INDICATORS:
                buffer = []
            else:
                fields[current_key] = value
                buffer = []
        elif current_key and raw.strip():
            buffer.append(raw.strip())
    if current_key and buffer and current_key not in fields:
        fields[current_key] = " ".join(buffer).strip()
    return fields


def guess_version(fields: dict, path: Path) -> str:
    declared = fields.get("version", "")
    if VERSION_DIR_RE.match(declared):
        return declared
    for parent in path.parents:
        if VERSION_DIR_RE.match(parent.name):
            return parent.name
    return "0"


def version_key(version: str) -> tuple:
    numbers: list[int] = []
    for token in VERSION_RE.findall(version):
        for piece in token.split("."):
            if piece.isdigit():
                numbers.append(int(piece))
    return tuple(numbers) if numbers else (0,)


def iter_skill_files(root: Path) -> Iterable[Path]:
    if not root.exists():
        return
    base_depth = len(root.parts)
    for dirpath, dirnames, filenames in os.walk(root):
        current = Path(dirpath)
        if len(current.parts) - base_depth >= MAX_DEPTH:
            dirnames[:] = []
        dirnames[:] = [name for name in dirnames if name not in SKIP_DIRS]
        if "SKILL.md" in filenames:
            yield current / "SKILL.md"


def collect_layer(roots: list[Path], layer: str) -> dict:
    """Collect skills from roots, keeping the highest version per skill name."""
    collected: dict[str, dict] = {}
    for root in roots:
        for skill_file in iter_skill_files(root):
            fields = read_frontmatter(skill_file)
            name = fields.get("name", "").strip()
            if not NAME_RE.fullmatch(name):
                name = skill_file.parent.name.lower()
            description = fields.get("description", "").strip()
            if not name or not description:
                continue
            version = guess_version(fields, skill_file)
            record = {
                "name": name,
                "layer": layer,
                "version": version,
                "path": str(skill_file.parent),
                "description": description,
                "display": fields.get("display_name_zh") or fields.get("displayName") or "",
            }
            previous = collected.get(name)
            if previous is None or version_key(version) > version_key(previous["version"]):
                if previous is not None:
                    record["shadowed"] = previous["version"]
                collected[name] = record
            else:
                collected[name].setdefault("shadowed_count", 0)
                collected[name]["shadowed_count"] = collected[name].get("shadowed_count", 0) + 1
    return collected


def score_skill(record: dict, keywords: list[str]) -> dict:
    haystack = " ".join(
        [record["name"], record["display"], record["description"]]
    ).lower()
    name_haystack = record["name"].lower()
    matched = []
    name_hits = 0
    for keyword in keywords:
        needle = keyword.strip().lower()
        if not needle:
            continue
        if needle in haystack:
            matched.append(keyword)
            if needle in name_haystack:
                name_hits += 1
    coverage = len(matched) / len(keywords) if keywords else 0.0
    score = round(coverage * 80 + name_hits * 20, 1)
    result = dict(record)
    result["matched"] = matched
    result["score"] = score
    return result


def render_markdown(rows: list[dict], keywords: list[str], counts: dict) -> str:
    lines = []
    lines.append("# 本地层扫描结果")
    lines.append("")
    lines.append("关键词：" + "、".join(keywords) if keywords else "关键词：未提供")
    lines.append("")
    lines.append("| 层 | 目录 | 解析到的技能数 |")
    lines.append("| --- | --- | --- |")
    for layer, info in counts.items():
        lines.append(f"| {layer} | {info['roots']} | {info['skills']} |")
    lines.append("")
    if not rows:
        lines.append("零命中：本地两层未发现与关键词匹配的技能。")
        return "\n".join(lines)
    lines.append("| 技能 | 层 | 版本 | 匹配词 | 匹配分 | 路径 |")
    lines.append("| --- | --- | --- | --- | --- | --- |")
    for row in rows:
        matched = "、".join(row["matched"]) if row["matched"] else "—"
        lines.append(
            f"| {row['name']} | {row['layer']} | {row['version']} | {matched} | {row['score']} | {row['path']} |"
        )
    return "\n".join(lines)


def default_roots() -> dict:
    home = Path(os.path.expanduser("~"))
    return {
        "L1": [home / ".workbuddy" / "plugins" / "cache"],
        "L2": [
            home / ".workbuddy" / "skills",
            Path.cwd() / ".workbuddy" / "skills",
            home / ".workbuddy" / "skills-marketplace" / "skills",
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Scan local L1/L2 skill layers, deduplicate by name, rank against keywords."
    )
    parser.add_argument("--keywords", nargs="*", default=[], help="keywords in any language")
    parser.add_argument("--builtin-root", action="append", default=[], help="extra L1 root, repeatable")
    parser.add_argument("--user-root", action="append", default=[], help="extra L2 root, repeatable")
    parser.add_argument("--json", dest="json_path", help="also write results as JSON")
    parser.add_argument("--top", type=int, default=0, help="limit output rows, 0 means all")
    parser.add_argument("--root-label", default="", help="label printed in the header")
    args = parser.parse_args()

    roots = default_roots()
    roots["L1"].extend(Path(p) for p in args.builtin_root)
    roots["L2"].extend(Path(p) for p in args.user_root)

    merged: dict[str, dict] = {}
    counts: dict[str, dict] = {}
    for layer, layer_roots in roots.items():
        collected = collect_layer(layer_roots, layer)
        counts[layer] = {
            "roots": ", ".join(str(root) for root in layer_roots),
            "skills": len(collected),
        }
        for name, record in collected.items():
            existing = merged.get(name)
            if existing is None:
                merged[name] = record
            else:
                merged[name].setdefault("mirrors", [])
                merged[name]["mirrors"].append({"layer": record["layer"], "path": record["path"]})

    rows = [score_skill(record, args.keywords) for record in merged.values()]
    rows.sort(key=lambda item: (-item["score"], item["name"]))
    if args.keywords:
        rows = [row for row in rows if row["matched"]]
    if args.top > 0:
        rows = rows[: args.top]

    if args.root_label:
        print(f"扫描标签：{args.root_label}")

    print(render_markdown(rows, args.keywords, counts))

    if args.json_path:
        payload = {
            "keywords": args.keywords,
            "counts": counts,
            "results": rows,
        }
        Path(args.json_path).write_text(
            json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8"
        )
        print(f"\nJSON 已写入：{args.json_path}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
