"""Create a blank solution and short notes for one problem."""

import argparse
import re
import unicodedata

from _common import DIFFICULTIES, ROOT, SOLUTIONS, positive_int, problem_folders, problem_number


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("number", type=positive_int)
    parser.add_argument("title")
    parser.add_argument("--difficulty", type=str.capitalize, choices=DIFFICULTIES, required=True)
    args = parser.parse_args()

    title = args.title.strip()
    if "\n" in title or "\r" in title:
        parser.error("title must be a single line")
    ascii_title = unicodedata.normalize("NFKD", title).encode("ascii", "ignore").decode()
    slug = re.sub(r"[^a-z0-9]+", "-", ascii_title.lower()).strip("-")
    if not slug:
        parser.error("title needs at least one letter or number")
    if any(problem_number(folder) == args.number for folder in problem_folders()):
        parser.error(f"problem {args.number} already exists")

    folder = SOLUTIONS / f"{args.number:04d}-{slug}"
    try:
        folder.mkdir(parents=True, exist_ok=False)
    except FileExistsError:
        parser.error(f"{folder.name} already exists")
    (folder / "solution.py").touch(exist_ok=False)
    (folder / "notes.md").write_text(
        f"---\ndifficulty: {args.difficulty}\nsolved: false\nreview_after:\n---\n\n"
        f"# {args.number}. {title}\n\n"
        f"[Problem](https://leetcode.com/problems/{slug}/)\n\n"
        "## Notes\n\n",
        encoding="utf-8",
    )
    print(f"Created {folder.relative_to(ROOT)}")
    print("Paste your Python code into solution.py. Change solved to true in notes.md when finished.")


if __name__ == "__main__":
    main()
