#!/usr/bin/env python3
"""Static validation for the TRIAGE-X repository.

Checks:
  1. Repository structure (every required file exists and is non-empty).
  2. Tool modules: required files and sections; 5-8 complete failure patterns per runbook.
  3. Evaluation cases: completeness, valid enums, >= 4 cases per tool, all cross-cutting cases present.
  4. Expected outputs: every file validates against schemas/triage-result.schema.json, every input
     has a matching expected output, the four worked examples exist, and every tool is covered.
  5. Sensitive-content scan: URLs, IP addresses, e-mail addresses and secret-like strings.

Limitation: this script does NOT run behavioral evaluation (asking the skill to triage each case
and scoring the answer). That requires the in-house skill platform and integrations or recorded
tool responses. See docs/evaluation-and-improvement.md.

Usage:  python3 tests/validate.py        (exit code 0 = all checks passed)
Requires: PyYAML, jsonschema (pip install -r tests/requirements.txt)
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

try:
    import yaml
    from jsonschema import Draft202012Validator
except ImportError as exc:  # pragma: no cover
    sys.exit(f"Missing dependency: {exc.name}. Run: pip install -r tests/requirements.txt")

ROOT = Path(__file__).resolve().parent.parent

TOOLS = ["github", "jenkins", "concord", "gates", "sonarqube", "artifactory", "docker", "kubernetes", "cd-orchestration"]
STAGES = {"source-change", "ci-build", "quality-security", "package-publish", "orchestrate-deliver", "deploy", "run-operate"}
CATEGORIES = {"code-change", "configuration", "dependency", "credentials-access", "policy-gate",
              "capacity-quota", "platform-infra", "transient-flaky", "unknown"}
CLASSIFICATIONS = {"self-fix", "l1", "prod-team", None}
STATUSES = {"complete", "needs-input", "blocked-access"}

REQUIRED_FILES = [
    "README.md", "SKILL.md", "CODEOWNERS", "CHANGELOG.md", ".gitignore",
    "core/router.md", "core/lifecycle-stages.md", "core/classification.md", "core/output-contract.md",
    "core/evidence-and-confidence.md", "core/security-and-privacy.md", "core/nlh-template.md", "core/self-rca.md",
    "schemas/triage-result.schema.json",
    "integrations/jira-mcp.md", "integrations/slack.md",
    "docs/architecture.md", "docs/adding-a-tool.md", "docs/evaluation-and-improvement.md", "docs/usa-integration.md",
    "tests/validate.py", "tests/requirements.txt",
    "examples/inputs/kitt-multi-target.example.yml",
    "config/triage-x.config.example.yaml",
]

CONTEXT_SECTIONS = ["## Role in the lifecycle", "## Context to collect", "## Identifiers and target resolution",
                    "## Connector and access", "## Relationships to other tools", "## Pilot status"]
CHECKS_SECTIONS = ["## Read-only diagnostic checks", "## What-changed checks", "## Blast-radius checks", "## Never do"]
PATTERN_FIELDS = ["Lifecycle stage", "Failure category", "Symptoms", "Log or event signatures (illustrative)",
                  "Evidence to collect", "What-changed checks", "Possible cause", "Safe diagnostic checks",
                  "Developer-performed fix", "L1 escalation conditions", "Prod-team conditions", "Expected classification"]

WORKED_EXAMPLES = ["ex01-selffix-quality-gate", "ex02-l1-artifactory-403", "ex03-prod-capacity-deploy", "ex04-needs-input-multi-target"]

CASE_KEYS = ["id", "title", "input", "evidence", "expected", "safety", "rationale"]
EXPECTED_KEYS = ["lifecycle_stage", "reported_tool", "primary_tool", "secondary_tools", "failure_category",
                 "classification", "status", "question_expected", "jira_expected", "slack_expected"]
# Cross-cutting topics required by the build spec, matched against case titles (case-insensitive).
CROSS_CUTTING_TOPICS = {
    "multiple CD Orchestration tools (AKS, GKE, EKS) targets": r"multiple possible cd orchestration tools \(aks, gke, eks\) targets",
    "conflicting Concord/config evidence": r"conflicting concord",
    "missing access": r"missing access",
    "incomplete logs": r"incomplete logs",
    "reported tool is not failing tool": r"reported tool is not failing tool",
    "policy gate correctly blocks": r"policy gate correctly blocks",
    "transient (retry)": r"transient failure, first time",
    "transient (recurring)": r"transient failure, recurring",
    "multi-application symptom": r"multi-application symptom",
    "secrets in logs": r"secrets in supplied logs",
    "malicious instructions in logs": r"malicious instructions",
    "Jira failure / ambiguous write": r"jira creation fails",
    "Slack failure": r"slack notification fails",
    "duplicate ticket": r"duplicate ticket",
    "STRCONTAIN attempt": r"strcontain",
    "Self-RCA not overstated": r"self-rca not confirmed",
}

# Sensitive-content scan.
SCAN_SUFFIXES = {".md", ".yaml", ".yml", ".json", ".py", ".txt", ""}
SCAN_SKIP_DIRS = {".git", ".venv", "venv", "__pycache__"}
URL_ALLOWLIST = ("https://json-schema.org/", "https://keepachangelog.com/")
URL_RE = re.compile(r"https?://[^\s)>\"'`]+")
IP_RE = re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b")
EMAIL_RE = re.compile(r"\b[\w.+-]+@[A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)*\.[A-Za-z]{2,}\b")
SECRET_RES = [
    re.compile(r"AKIA[0-9A-Z]{16}"),
    re.compile(r"gh[pousr]_[A-Za-z0-9]{20,}"),
    re.compile(r"xox[abprs]-[A-Za-z0-9-]{10,}"),
    re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----\s*\n\s*[A-Za-z0-9+/]"),
    re.compile(r"Bearer\s+[A-Za-z0-9._\-]{20,}"),
    re.compile(r"(?i)(password|passwd|secret|api_key|apikey|token)\s*[:=]\s*['\"]?[A-Za-z0-9/+_\-]{12,}"),
]


class Report:
    def __init__(self) -> None:
        self.errors: list[str] = []
        self.passed: list[str] = []

    def check(self, name: str, errors: list[str]) -> None:
        if errors:
            self.errors += [f"[{name}] {e}" for e in errors]
            print(f"FAIL  {name} ({len(errors)} problem(s))")
        else:
            self.passed.append(name)
            print(f"PASS  {name}")


def rel(p: Path) -> str:
    return str(p.relative_to(ROOT))


def check_structure() -> list[str]:
    errs = []
    for f in REQUIRED_FILES:
        p = ROOT / f
        if not p.is_file():
            errs.append(f"missing file: {f}")
        elif p.stat().st_size == 0:
            errs.append(f"empty file: {f}")
    for d in ["examples/inputs", "examples/expected-outputs", "tests/cases"]:
        if not (ROOT / d).is_dir():
            errs.append(f"missing directory: {d}")
    return errs


def parse_patterns(text: str) -> list[tuple[str, str]]:
    """Return (heading, body) for every '## Pattern ...' section."""
    parts = re.split(r"^## Pattern (?!index)", text, flags=re.M)[1:]
    out = []
    for part in parts:
        heading, _, body = part.partition("\n")
        body = re.split(r"^## ", body, flags=re.M)[0]
        out.append((heading.strip(), body))
    return out


def check_tool_modules() -> list[str]:
    errs = []
    for tool in TOOLS + ["_template"]:
        base = ROOT / "tools" / tool
        for fname, sections in (("context.md", CONTEXT_SECTIONS), ("checks.md", CHECKS_SECTIONS), ("runbooks.md", [])):
            p = base / fname
            if not p.is_file():
                errs.append(f"tools/{tool}/{fname} missing")
                continue
            text = p.read_text()
            for s in sections:
                if s not in text:
                    errs.append(f"tools/{tool}/{fname}: missing section '{s}'")
        rb = base / "runbooks.md"
        if not rb.is_file():
            continue
        patterns = parse_patterns(rb.read_text())
        if tool == "_template":
            if not patterns:
                errs.append("tools/_template/runbooks.md: no example pattern")
            continue
        if not 5 <= len(patterns) <= 8:
            errs.append(f"tools/{tool}/runbooks.md: {len(patterns)} patterns (expected 5-8)")
        for heading, body in patterns:
            for field in PATTERN_FIELDS:
                m = re.search(r"^- \*\*" + re.escape(field) + r":\*\*(.*)$", body, flags=re.M)
                if not m:
                    errs.append(f"tools/{tool} pattern '{heading}': missing field '{field}'")
                    continue
                value = m.group(1).strip()
                if field == "Lifecycle stage" and value.strip("`") not in STAGES:
                    errs.append(f"tools/{tool} pattern '{heading}': invalid stage {value}")
                if field == "Failure category" and value.strip("`") not in CATEGORIES:
                    errs.append(f"tools/{tool} pattern '{heading}': invalid category {value}")
    return errs


def load_yaml(p: Path):
    with p.open() as fh:
        return yaml.safe_load(fh)


def check_eval_cases() -> list[str]:
    errs = []
    case_dir = ROOT / "tests" / "cases"
    seen_ids: set[str] = set()
    for tool in TOOLS:
        p = case_dir / f"{tool}.yaml"
        if not p.is_file():
            errs.append(f"tests/cases/{tool}.yaml missing")
    files = sorted(case_dir.glob("*.yaml"))
    cross = []
    for p in files:
        try:
            cases = load_yaml(p)
        except yaml.YAMLError as exc:
            errs.append(f"{rel(p)}: YAML error {exc}")
            continue
        if not isinstance(cases, list):
            errs.append(f"{rel(p)}: must be a list of cases")
            continue
        if p.stem in TOOLS and len(cases) < 4:
            errs.append(f"{rel(p)}: {len(cases)} cases (expected >= 4)")
        if p.stem == "cross-cutting":
            cross = cases
        for c in cases:
            cid = c.get("id", "<no id>") if isinstance(c, dict) else "<not a mapping>"
            if not isinstance(c, dict):
                errs.append(f"{rel(p)}: case is not a mapping")
                continue
            if cid in seen_ids:
                errs.append(f"{rel(p)}: duplicate case id {cid}")
            seen_ids.add(cid)
            for k in CASE_KEYS:
                if k not in c or c[k] in ("", None, []):
                    errs.append(f"{rel(p)} {cid}: missing or empty '{k}'")
            exp = c.get("expected") or {}
            for k in EXPECTED_KEYS:
                if k not in exp:
                    errs.append(f"{rel(p)} {cid}: expected.{k} missing")
            ls = exp.get("lifecycle_stage") or {}
            for k in ("first_failing", "reported_at"):
                if k not in ls or (ls[k] is not None and ls[k] not in STAGES):
                    errs.append(f"{rel(p)} {cid}: invalid lifecycle_stage.{k}={ls.get(k)!r}")
            for k in ("reported_tool", "primary_tool"):
                if exp.get(k) is not None and exp.get(k) not in TOOLS:
                    errs.append(f"{rel(p)} {cid}: invalid {k}={exp.get(k)!r}")
            for t in exp.get("secondary_tools") or []:
                if t not in TOOLS:
                    errs.append(f"{rel(p)} {cid}: invalid secondary tool {t!r}")
            if exp.get("failure_category") not in CATEGORIES:
                errs.append(f"{rel(p)} {cid}: invalid failure_category {exp.get('failure_category')!r}")
            if exp.get("classification", "x") not in CLASSIFICATIONS:
                errs.append(f"{rel(p)} {cid}: invalid classification {exp.get('classification')!r}")
            if exp.get("status") not in STATUSES:
                errs.append(f"{rel(p)} {cid}: invalid status {exp.get('status')!r}")
            if exp.get("status") == "complete" and exp.get("classification") is None:
                errs.append(f"{rel(p)} {cid}: status complete requires a classification")
            if exp.get("slack_expected") and exp.get("classification") != "prod-team":
                errs.append(f"{rel(p)} {cid}: slack_expected only allowed for prod-team")
            if exp.get("classification") == "self-fix" and exp.get("jira_expected"):
                errs.append(f"{rel(p)} {cid}: self-fix must not expect a Jira ticket")
            for k in ("question_expected", "jira_expected", "slack_expected"):
                if not isinstance(exp.get(k), bool):
                    errs.append(f"{rel(p)} {cid}: expected.{k} must be true/false")
    if not cross:
        errs.append("tests/cases/cross-cutting.yaml missing or empty")
    titles = " | ".join(str(c.get("title", "")) for c in cross if isinstance(c, dict)).lower()
    for topic, rx in CROSS_CUTTING_TOPICS.items():
        if not re.search(rx, titles):
            errs.append(f"cross-cutting case missing: {topic}")
    return errs


def check_expected_outputs() -> list[str]:
    errs = []
    schema = json.loads((ROOT / "schemas" / "triage-result.schema.json").read_text())
    Draft202012Validator.check_schema(schema)
    validator = Draft202012Validator(schema)
    in_dir, out_dir = ROOT / "examples" / "inputs", ROOT / "examples" / "expected-outputs"
    inputs = {p.stem for p in in_dir.glob("*.md")}
    outputs = {p.stem for p in out_dir.glob("*.yaml")}
    for missing in sorted(inputs - outputs):
        errs.append(f"no expected output for examples/inputs/{missing}.md")
    for orphan in sorted(outputs - inputs):
        errs.append(f"expected output without input: {orphan}.yaml")
    for ex in WORKED_EXAMPLES:
        if ex not in inputs or ex not in outputs:
            errs.append(f"worked example missing: {ex}")
    covered: set[str] = set()
    for p in sorted(out_dir.glob("*.yaml")):
        doc = load_yaml(p)
        if not isinstance(doc, dict) or "triage_result" not in doc:
            errs.append(f"{rel(p)}: missing triage_result")
            continue
        if not str(doc.get("human_readable", "")).startswith("TRIAGE-X Result · "):
            errs.append(f"{rel(p)}: human_readable must start with 'TRIAGE-X Result · '")
        for e in validator.iter_errors({"triage_result": doc["triage_result"]}):
            path = "/".join(str(x) for x in e.absolute_path)
            errs.append(f"{rel(p)}: schema error at {path or '<root>'}: {e.message}")
        r = doc["triage_result"]
        rca_status = (r.get("rca") or {}).get("status")
        if r.get("status") == "complete" and rca_status not in ("draft", "confirmed-by-developer"):
            errs.append(f"{rel(p)}: complete triage must include a Self-RCA (rca.status draft or confirmed-by-developer)")
        if r.get("status") == "complete" and "Self-RCA · " not in str(doc.get("human_readable", "")):
            errs.append(f"{rel(p)}: complete triage must include the Self-RCA block in human_readable")
        covered.update(t for t in [r.get("reported_tool"), r.get("primary_tool"), *r.get("secondary_tools", [])] if t)
    for t in TOOLS:
        if t not in covered:
            errs.append(f"no expected output involves tool '{t}'")
    return errs


def check_sensitive() -> list[str]:
    errs = []
    for p in sorted(ROOT.rglob("*")):
        if not p.is_file() or any(part in SCAN_SKIP_DIRS for part in p.relative_to(ROOT).parts):
            continue
        if p.suffix not in SCAN_SUFFIXES or p.name == "validate.py":
            continue
        try:
            text = p.read_text()
        except UnicodeDecodeError:
            continue
        for n, line in enumerate(text.splitlines(), 1):
            for url in URL_RE.findall(line):
                if not url.startswith(URL_ALLOWLIST):
                    errs.append(f"{rel(p)}:{n}: URL not on allowlist: {url}")
            for ip in IP_RE.findall(line):
                if all(0 <= int(x) <= 255 for x in ip.split(".")):
                    errs.append(f"{rel(p)}:{n}: IP address: {ip}")
            for em in EMAIL_RE.findall(line):
                errs.append(f"{rel(p)}:{n}: e-mail address: {em}")
        for rx in SECRET_RES:
            for m in rx.finditer(text):
                n = text.count("\n", 0, m.start()) + 1
                errs.append(f"{rel(p)}:{n}: secret-like string")
    return errs


def main() -> int:
    print(f"TRIAGE-X static validation · {ROOT}\n")
    rep = Report()
    rep.check("repository structure", check_structure())
    rep.check("tool modules", check_tool_modules())
    rep.check("evaluation cases", check_eval_cases())
    rep.check("expected outputs vs schema", check_expected_outputs())
    rep.check("sensitive-content scan", check_sensitive())
    print("\nNOT RUN: behavioral evaluation (needs the skill platform; see docs/evaluation-and-improvement.md)")
    if rep.errors:
        print(f"\n{len(rep.errors)} problem(s):")
        for e in rep.errors:
            print(f"  - {e}")
        return 1
    print(f"\nAll {len(rep.passed)} checks passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
