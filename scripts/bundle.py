#!/usr/bin/env python3
"""Bundle TRIAGE-X into one Markdown file for platforms that load a single skill file.

Output: dist/triage-x-skill.md (SKILL.md first, then core, integrations and tool modules).
Usage:  python3 scripts/bundle.py [--out PATH] [--tools jenkins,sonarqube,cd-orchestration]
The default includes every tool. Use --tools to make a smaller pilot bundle.
"""
from __future__ import annotations

import argparse
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CORE = ["router.md", "lifecycle-stages.md", "classification.md", "evidence-and-confidence.md",
        "output-contract.md", "self-rca.md", "nlh-template.md", "security-and-privacy.md"]
ALL_TOOLS = ["github", "jenkins", "concord", "gates", "sonarqube", "artifactory", "docker", "kubernetes", "cd-orchestration"]
TOOL_FILES = ["context.md", "checks.md", "runbooks.md"]


def section(path: Path) -> str:
    rel = path.relative_to(ROOT)
    return f"\n\n<!-- ===== {rel} ===== -->\n\n" + path.read_text().strip() + "\n"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=str(ROOT / "dist" / "triage-x-skill.md"))
    ap.add_argument("--tools", default=",".join(ALL_TOOLS))
    args = ap.parse_args()
    tools = [t.strip() for t in args.tools.split(",") if t.strip()]
    unknown = sorted(set(tools) - set(ALL_TOOLS))
    if unknown:
        raise SystemExit(f"Unknown tool(s): {', '.join(unknown)}")

    parts = [(ROOT / "SKILL.md").read_text().strip() + "\n",
             "\n\n# Reference material\n\nThe sections below are the TRIAGE-X reference files, in the order the workflow uses them. "
             "Where SKILL.md points to a file path, the matching section is below."]
    parts += [section(ROOT / "core" / f) for f in CORE]
    parts += [section(ROOT / "integrations" / f) for f in ("jira-mcp.md", "slack.md")]
    for t in tools:
        parts += [section(ROOT / "tools" / t / f) for f in TOOL_FILES]
    if set(tools) != set(ALL_TOOLS):
        skipped = ", ".join(t for t in ALL_TOOLS if t not in tools)
        parts.append(f"\n\n<!-- Tools not included in this bundle: {skipped}. Treat requests for them as outside this bundle's scope. -->\n")

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    text = "".join(parts)
    out.write_text(text)
    print(f"Wrote {out} ({len(text.splitlines())} lines, {len(text) // 1024} KB, tools: {', '.join(tools)})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
