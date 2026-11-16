#!/usr/bin/env python3
"""Validate, render and publish the Stellar Wave backlog in scripts/wave-issues.json.

Every issue carries a complexity (trivial, medium, high) worth 100, 150 or 200
points. Validation runs before any GitHub mutation and refuses a backlog whose
points do not add up to the declared budget.

  ./scripts/create-issues.sh                 # dry run: validate and print totals
  ./scripts/create-issues.sh --emit FILE     # write rendered issues as JSON
  ./scripts/create-issues.sh --create        # operator: create missing issues
  ./scripts/create-issues.sh --sync-existing # operator: restyle linked issues
"""
import argparse
import collections
import json
import pathlib
import re
import subprocess
import tempfile

ROOT = pathlib.Path(__file__).resolve().parent.parent
AREAS = {"parser", "rules", "sync", "store", "api", "cli", "reports", "docs", "tooling", "security"}
COMPLEXITY_NAMES = {"trivial": "Trivial", "medium": "Medium", "high": "High"}
REPO_URL = "https://github.com/{repo}/blob/main/{path}"


def load_backlog():
    data = json.loads((ROOT / "scripts/wave-issues.json").read_text())
    points, budget, issues = data["points"], data["budget"], data["issues"]
    assert set(points) == set(COMPLEXITY_NAMES), "points must define trivial, medium and high"
    titles = set()
    for item in issues:
        title = item["title"]
        assert title not in titles, f"duplicate issue title: {title}"
        titles.add(title)
        assert item["complexity"] in points, f"unknown complexity: {title}"
        assert item["area"] in AREAS, f"unknown area {item['area']}: {title}"
        for field in ("description", "why"):
            assert item[field].strip(), f"missing {field}: {title}"
        assert len(item["acceptance_criteria"]) >= 2, f"needs 2+ acceptance criteria: {title}"
        assert isinstance(item.get("existing_issue", 0), int) and item.get("existing_issue", 0) >= 0
        for pointer in item["pointers"]:
            path = (ROOT / pointer).resolve()
            assert path.is_relative_to(ROOT) and path.exists(), f"unknown pointer {pointer}: {title}"
    total = sum(points[x["complexity"]] for x in issues)
    assert total == budget, f"backlog totals {total} points; budget is {budget}"
    return points, budget, issues


def labels(item):
    out = ["Stellar Wave", "complexity:" + item["complexity"], "area:" + item["area"]]
    if item["complexity"] == "trivial":
        out.append("good first issue")
    return out


def body(item, points, repo):
    link = lambda path: REPO_URL.format(repo=repo, path=path)
    guidance = list(item.get("guidance", []))
    guidance.append("Files to start from: " + ", ".join(f"`{p}`" for p in item["pointers"]) + ".")
    sections = [
        "## 📘 Description\n" + item["description"] + "\n\n**Why this matters:** " + item["why"],
        "## ✅ Acceptance Criteria\n" + "\n".join("- [ ] " + x for x in item["acceptance_criteria"]),
        "## 🔧 Implementation Guidance\n" + "\n".join("- " + x for x in guidance),
        "## 📚 Before You Start\n"
        f"- Read [CONTRIBUTING.md]({link('CONTRIBUTING.md')}) for setup, `make` targets, commit rules and the PR checklist.\n"
        f"- Skim [how it works]({link('docs/how-it-works.md')}) and the [trust tiers]({link('docs/trust-tiers.md')}).\n"
        "- Changes to public API paths or response shapes, the trust-tier definitions, or the database schema need "
        "maintainer approval in this issue before you write code.\n"
        "- Every number or output you put in docs or the PR must come from a command you ran.",
        "## 📋 Additional Notes\n"
        f"**Complexity: {COMPLEXITY_NAMES[item['complexity']]} ({points[item['complexity']]} points)**",
    ]
    return "\n\n".join(sections) + "\n"


def gh(*args, capture=False):
    return subprocess.run(["gh", *args], check=True, text=True,
                          stdout=subprocess.PIPE if capture else None)


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--repo", default="Soroban-CII/soroindex")
    parser.add_argument("--emit", metavar="FILE", help="write rendered issues (title, labels, body) as JSON")
    parser.add_argument("--create", action="store_true", help="operator: create issues not yet on GitHub")
    parser.add_argument("--sync-existing", action="store_true", help="operator: restyle linked issues' body and labels")
    args = parser.parse_args()
    if not re.fullmatch(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+", args.repo):
        parser.error("repo must be owner/name")
    points, budget, issues = load_backlog()  # Complete validation precedes every mutation.

    tiers = collections.Counter(x["complexity"] for x in issues)
    linked = [x for x in issues if x.get("existing_issue")]
    pending = [x for x in issues if not x.get("existing_issue")]
    summary = ", ".join(f"{tiers[c]} {c} x {points[c]}" for c in ("high", "medium", "trivial"))
    print(f"validated {len(issues)} issues = {budget} points ({summary}); "
          f"{len(linked)} on GitHub, {len(pending)} to create")
    print("areas:", dict(sorted(collections.Counter(x["area"] for x in issues).items())))

    if args.emit:
        rendered = [{"title": x["title"], "labels": labels(x), "body": body(x, points, args.repo),
                     "existing_issue": x.get("existing_issue")} for x in issues]
        pathlib.Path(args.emit).write_text(json.dumps(rendered, indent=1, ensure_ascii=False) + "\n")
        print(f"wrote {len(rendered)} rendered issues to {args.emit}")
    if not (args.create or args.sync_existing):
        return

    open_numbers = set(gh("api", "--paginate", f"repos/{args.repo}/issues?state=open&per_page=100",
                          "--jq", ".[] | select(.pull_request == null) | .number", capture=True).stdout.split())
    stale = [x for x in linked if str(x["existing_issue"]) not in open_numbers]
    if stale:  # A closed tracker means the backlog file is out of date.
        raise SystemExit("existing_issue not open: " + ", ".join(f"#{x['existing_issue']}" for x in stale))
    existing_titles = set(gh("api", "--paginate", f"repos/{args.repo}/issues?state=all&per_page=100",
                             "--jq", ".[] | select(.pull_request == null) | .title", capture=True).stdout.splitlines())
    names = {"Stellar Wave": "1D76DB", "good first issue": "7057FF"}
    names.update({f"complexity:{c}": "FBCA04" for c in points})
    names.update({f"area:{a}": "5319E7" for a in sorted(AREAS)})
    for label, color in names.items():
        gh("label", "create", label, "--repo", args.repo, "--color", color, "--force")

    for item in (linked if args.sync_existing else []):
        with tempfile.TemporaryDirectory(prefix="soroindex-issue-") as directory:
            path = pathlib.Path(directory) / "body.md"
            path.write_text(body(item, points, args.repo))
            gh("issue", "edit", str(item["existing_issue"]), "--repo", args.repo, "--body-file", str(path),
               *[a for label in labels(item) for a in ("--add-label", label)])
    created = 0
    for item in (pending if args.create else []):
        if item["title"] in existing_titles:
            print("skip (exists): " + item["title"])
            continue
        with tempfile.TemporaryDirectory(prefix="soroindex-issue-") as directory:
            path = pathlib.Path(directory) / "body.md"
            path.write_text(body(item, points, args.repo))
            gh("issue", "create", "--repo", args.repo, "--title", item["title"], "--body-file", str(path),
               *[a for label in labels(item) for a in ("--label", label)])
        created += 1
    print(f"created {created}")


if __name__ == "__main__":
    main()
