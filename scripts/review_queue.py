"""List your problems and solved count, with optional filters."""

import argparse

from _common import DIFFICULTIES, load_problems, positive_int, problem_number, report_errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--number", type=positive_int, help="find a LeetCode problem number")
    parser.add_argument("--name", help="search part of a problem name")
    parser.add_argument("--difficulty", type=str.capitalize, choices=DIFFICULTIES)
    status = parser.add_mutually_exclusive_group()
    status.add_argument("--solved", action="store_true", help="show only solved problems")
    status.add_argument("--unsolved", action="store_true", help="show only unfinished problems")
    args = parser.parse_args()
    problems, errors = load_problems()
    if errors:
        report_errors(errors)
        return 1

    solved = sum(values["solved"] == "true" for _, values in problems)
    print(f"Overall: {solved} solved / {len(problems)} problems")
    matches = []
    for folder, values in problems:
        if args.number is not None and problem_number(folder) != args.number:
            continue
        if args.name and args.name.casefold() not in values["title"].casefold():
            continue
        if args.difficulty and values["difficulty"] != args.difficulty:
            continue
        if args.solved and values["solved"] != "true":
            continue
        if args.unsolved and values["solved"] != "false":
            continue
        matches.append((folder, values))
    if not matches:
        print("No matching problems." if problems else "No problems yet.")
        return 0
    match_solved = sum(values["solved"] == "true" for _, values in matches)
    print(f"Showing: {len(matches)} problems ({match_solved} solved)\n")
    for folder, values in matches:
        state = "Solved" if values["solved"] == "true" else "Unsolved"
        review = f" | Review: {values['review_after']}" if values.get("review_after") else ""
        print(f"{problem_number(folder)}. {values['title']} | {values['difficulty']} | {state}{review}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
