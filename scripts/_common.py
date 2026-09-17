"""Shared paths and problem loading."""

import argparse
from datetime import date
from pathlib import Path
import re
import sys


ROOT = Path(__file__).resolve().parents[1]
SOLUTIONS = ROOT / "solutions"
DIFFICULTIES = ("Easy", "Medium", "Hard")


def problem_folders():
    return sorted(path for path in SOLUTIONS.iterdir() if path.is_dir()) if SOLUTIONS.exists() else []


def problem_number(folder):
    prefix = folder.name.split("-", 1)[0]
    return int(prefix) if re.fullmatch(r"[0-9]+", prefix) else None


def read_notes(folder):
    lines = (folder / "notes.md").read_text(encoding="utf-8").splitlines()
    if not lines or lines[0] != "---" or "---" not in lines[1:]:
        raise ValueError("notes.md needs its opening tracking block between --- lines")
    end = lines.index("---", 1)
    values = {}
    for line in lines[1:end]:
        if not line.strip():
            continue
        key, separator, value = line.partition(":")
        if not separator or key.strip() in values:
            raise ValueError("invalid or duplicate notes field")
        values[key.strip()] = value.strip()
    if values.get("difficulty") not in DIFFICULTIES:
        raise ValueError("difficulty must be Easy, Medium, or Hard")
    if values.get("solved") not in ("true", "false"):
        raise ValueError("solved must be true or false")
    review = values.get("review_after", "")
    if review:
        if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", review):
            raise ValueError("review_after must be blank or YYYY-MM-DD")
        date.fromisoformat(review)
    title = next((line[2:] for line in lines[end + 1:] if line.startswith("# ")), folder.name)
    values["title"] = re.sub(r"^[0-9]+\.\s*", "", title)
    return values


def load_problems():
    problems, errors, seen = [], [], set()
    for folder in problem_folders():
        number = problem_number(folder)
        if not re.fullmatch(r"[0-9]{4,}-[a-z0-9]+(?:-[a-z0-9]+)*", folder.name) or not number:
            errors.append(f"{folder.name}: expected a name like 0001-two-sum")
        if number in seen:
            errors.append(f"{folder.name}: duplicate problem number {number}")
        seen.add(number)
        if not (folder / "solution.py").is_file():
            errors.append(f"{folder.name}: missing solution.py")
        try:
            values = read_notes(folder)
            if number:
                problems.append((folder, values))
        except (OSError, UnicodeError, ValueError) as error:
            errors.append(f"{folder.name}: {error}")
    return sorted(problems, key=lambda item: problem_number(item[0])), errors


def positive_int(value):
    try:
        number = int(value)
        if number > 0:
            return number
    except ValueError:
        pass
    raise argparse.ArgumentTypeError("use a positive whole number")


def report_errors(errors):
    for error in errors:
        print(f"Error: {error}", file=sys.stderr)
