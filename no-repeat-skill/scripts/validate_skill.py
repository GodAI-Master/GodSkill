#!/usr/bin/env python3
"""Run dependency-free static checks against an Agent Skill directory."""

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Optional
from urllib.parse import unquote


NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
FRONTMATTER_RE = re.compile(r"\A---\n(?P<body>.*?)\n---(?:\n|\Z)", re.DOTALL)
FIELD_RE = re.compile(r"^([A-Za-z][A-Za-z0-9_-]*):\s*(.*)$")
LINK_RE = re.compile(r"(?<!!)\[[^\]]*\]\(([^)]+)\)|!\[[^\]]*\]\(([^)]+)\)")
POLLUTANT_NAMES = {".DS_Store", "Thumbs.db"}
POLLUTANT_SUFFIXES = {".pyc", ".pyo", ".swp", ".swo", ".tmp", ".bak"}
POLLUTANT_DIRS = {"__pycache__", ".pytest_cache", ".mypy_cache"}
TEXT_SUFFIXES = {".md", ".txt", ".yaml", ".yml", ".json", ".py", ".sh", ".toml"}
RESOURCE_DIRS = {"references", "assets", "evals", "examples"}


def scalar(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}:
        if value[0] == '"':
            try:
                return json.loads(value)
            except json.JSONDecodeError:
                pass
        return value[1:-1]
    return value


def frontmatter(text: str) -> tuple[dict[str, str], int]:
    match = FRONTMATTER_RE.match(text)
    if not match:
        return {}, 0
    values: dict[str, str] = {}
    for line in match.group("body").splitlines():
        field = FIELD_RE.match(line)
        if field:
            values[field.group(1)] = scalar(field.group(2))
    return values, match.end()


def link_target(raw: str) -> Optional[str]:
    target = raw.strip()
    if target.startswith("<") and target.endswith(">"):
        target = target[1:-1]
    elif " " in target:
        target = target.split(None, 1)[0]
    target = unquote(target).split("#", 1)[0]
    if not target or target.startswith(("http://", "https://", "mailto:", "data:")):
        return None
    return target


def validate_route_cases(data: object, rel: Path, errors: list[str]) -> None:
    """Validate the optional route-cases.json convention without claiming to run it."""
    if not isinstance(data, dict) or not isinstance(data.get("cases"), list):
        errors.append(f"{rel} must contain a top-level cases array")
        return
    allowed_types = {"positive", "negative", "near-neighbor"}
    allowed_expected = {"trigger", "no-trigger", "other-capability"}
    counts = {case_type: 0 for case_type in allowed_types}
    identifiers: set[str] = set()
    for index, case in enumerate(data["cases"]):
        label = f"{rel} case #{index + 1}"
        if not isinstance(case, dict):
            errors.append(f"{label} must be an object")
            continue
        for field in ("id", "type", "query", "expected", "reason"):
            if not isinstance(case.get(field), str) or not case[field].strip():
                errors.append(f"{label} has missing or empty '{field}'")
        identifier = case.get("id")
        if isinstance(identifier, str):
            if identifier in identifiers:
                errors.append(f"{label} duplicates id '{identifier}'")
            identifiers.add(identifier)
        case_type = case.get("type")
        if case_type not in allowed_types:
            errors.append(f"{label} has unsupported type '{case_type}'")
        else:
            counts[case_type] += 1
        expected = case.get("expected")
        if expected not in allowed_expected:
            errors.append(f"{label} has unsupported expected value '{expected}'")
        if case_type == "positive" and expected != "trigger":
            errors.append(f"{label} positive cases must expect 'trigger'")
        if case_type == "negative" and expected != "no-trigger":
            errors.append(f"{label} negative cases must expect 'no-trigger'")
        if case_type == "near-neighbor" and expected != "other-capability":
            errors.append(f"{label} near-neighbor cases must expect 'other-capability'")
    for case_type, count in counts.items():
        if count == 0:
            errors.append(f"{rel} must include at least one {case_type} case")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Check Skill frontmatter, local links, JSON, placeholders, private paths, and release debris."
    )
    parser.add_argument("skill_directory", type=Path)
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Treat warnings, including unreferenced supporting resources, as failures.",
    )
    args = parser.parse_args()
    root = args.skill_directory.resolve()
    errors: list[str] = []
    warnings: list[str] = []

    if not root.is_dir():
        print(f"ERROR: skill directory does not exist: {root}")
        return 1

    skill_file = root / "SKILL.md"
    if not skill_file.is_file():
        print("ERROR: SKILL.md is missing")
        return 1

    try:
        skill_text = skill_file.read_text(encoding="utf-8")
    except UnicodeDecodeError as exc:
        print(f"ERROR: SKILL.md is not valid UTF-8: {exc}")
        return 1

    metadata, body_start = frontmatter(skill_text)
    if not metadata:
        errors.append("SKILL.md has missing or malformed YAML frontmatter")
    name = metadata.get("name", "")
    description = metadata.get("description", "")
    if not name:
        errors.append("frontmatter is missing name")
    elif not NAME_RE.fullmatch(name):
        errors.append("name must use lowercase letters, digits, and single hyphens")
    elif len(name) > 64:
        errors.append("name is longer than 64 characters")
    if name and name != root.name:
        errors.append(f"frontmatter name '{name}' does not match directory '{root.name}'")
    if not description:
        errors.append("frontmatter is missing description")
    else:
        if len(description) > 1024:
            errors.append("description is longer than 1024 characters")
        if len(description) < 40:
            warnings.append("description may be too short to distinguish routing intent")
        if "<" in description or ">" in description:
            errors.append("description contains angle brackets")

    markdown_files = [path for path in root.rglob("*.md") if path.is_file()]
    linked_files: set[Path] = set()
    for source in markdown_files:
        try:
            content = source.read_text(encoding="utf-8")
        except UnicodeDecodeError as exc:
            errors.append(f"{source.relative_to(root)} is not valid UTF-8: {exc}")
            continue
        scan_content = content[body_start:] if source == skill_file else content
        for match in LINK_RE.finditer(scan_content):
            raw = match.group(1) or match.group(2) or ""
            target = link_target(raw)
            if target is None:
                continue
            target_path = (source.parent / target).resolve()
            try:
                target_path.relative_to(root)
            except ValueError:
                errors.append(f"{source.relative_to(root)} links outside the Skill: {target}")
                continue
            if not target_path.exists():
                errors.append(f"{source.relative_to(root)} has a broken local link: {target}")
            elif target_path.is_file():
                linked_files.add(target_path)

    placeholder_terms = ("TO" + "DO", "T" + "BD", "待" + "补", "待" + "定")
    private_path_patterns = (
        re.compile(r"/Users/[^/\s]+/"),
        re.compile(r"/home/[^/\s]+/"),
        re.compile(r"[A-Za-z]:\\\\Users\\\\[^\\\s]+\\\\"),
    )
    secret_patterns = (
        re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
        re.compile(r"\b(?:sk|ghp|github_pat)_[A-Za-z0-9_-]{20,}\b"),
    )

    package_entries = sorted(root.rglob("*"))
    for path in package_entries:
        rel = path.relative_to(root)
        if path.is_dir():
            if path.name in POLLUTANT_DIRS:
                errors.append(f"release debris directory found: {rel}")
            continue
        if path.name in POLLUTANT_NAMES or path.suffix.lower() in POLLUTANT_SUFFIXES or path.name.endswith("~"):
            errors.append(f"release debris file found: {rel}")
        if path.suffix.lower() == ".json":
            try:
                json_data = json.loads(path.read_text(encoding="utf-8"))
            except (UnicodeDecodeError, json.JSONDecodeError) as exc:
                errors.append(f"invalid JSON in {rel}: {exc}")
            else:
                if rel.as_posix() == "evals/route-cases.json":
                    validate_route_cases(json_data, rel, errors)
        if path.suffix.lower() not in TEXT_SUFFIXES or rel.as_posix() == "scripts/validate_skill.py":
            continue
        try:
            file_text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        for term in placeholder_terms:
            if term in file_text:
                errors.append(f"unfinished placeholder '{term}' found in {rel}")
        for pattern in private_path_patterns:
            if pattern.search(file_text):
                warnings.append(f"possible machine-specific path found in {rel}")
                break
        for pattern in secret_patterns:
            if pattern.search(file_text):
                errors.append(f"possible secret material found in {rel}")
                break

    for dirname in RESOURCE_DIRS:
        directory = root / dirname
        if not directory.is_dir():
            continue
        for candidate in directory.rglob("*"):
            if candidate.is_file() and candidate.resolve() not in linked_files:
                warnings.append(f"supporting resource is not linked from package Markdown: {candidate.relative_to(root)}")

    print(f"Checked: {root}")
    for item in errors:
        print(f"ERROR: {item}")
    for item in warnings:
        print(f"WARNING: {item}")
    print(f"Summary: {len(errors)} error(s), {len(warnings)} warning(s)")

    if errors or (args.strict and warnings):
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
