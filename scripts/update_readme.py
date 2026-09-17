"""Update a progress section without changing your own README text."""

import argparse
from collections import Counter

from _common import DIFFICULTIES, ROOT, load_problems, problem_number, report_errors


START = "<!-- leetcode-progress:start -->"
END = "<!-- leetcode-progress:end -->"


def main():
    argparse.ArgumentParser(description=__doc__).parse_args()
    problems, errors = load_problems()
    if errors:
        report_errors(errors)
        return 1

    completed = [(folder, values) for folder, values in problems if values["solved"] == "true"]
    counts = Counter(values["difficulty"] for _, values in completed)
    rows = [START, "## Progress", "",
            f"Solved: **{len(completed)}** · Unsolved: **{len(problems) - len(completed)}**", "",
            " · ".join(f"{difficulty}: {counts[difficulty]}" for difficulty in DIFFICULTIES), ""]
    if completed:
        rows += ["| Solved problem | Difficulty |", "| --- | --- |"]
        for folder, values in completed:
            title = values["title"].replace("|", "&#124;").replace("[", "&#91;").replace("]", "&#93;")
            link = f"[{problem_number(folder)}. {title}](solutions/{folder.name}/solution.py)"
            rows.append(f"| {link} | {values['difficulty']} |")
        rows.append("")
    rows.append(END)
    section = "\n".join(rows)
    readme = ROOT / "README.md"
    original = readme.read_text(encoding="utf-8") if readme.exists() else ""
    if START in original or END in original:
        if original.count(START) != 1 or original.count(END) != 1 or original.index(START) > original.index(END):
            report_errors(["README progress markers are missing, duplicated, or reversed; no changes made"])
            return 1
        before, rest = original.split(START, 1)
        _, after = rest.split(END, 1)
        updated = before + section + after
    else:
        separator = "" if not original or original.endswith("\n\n") else ("\n" if original.endswith("\n") else "\n\n")
        updated = original + separator + section + "\n"
    if updated != original:
        readme.write_text(updated, encoding="utf-8")
    print(f"README updated: {len(completed)} solved, {len(problems) - len(completed)} unsolved.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
