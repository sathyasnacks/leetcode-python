"""Check for missing files, duplicate problem numbers, and Python syntax errors."""

import argparse
import ast

from _common import load_problems, problem_folders, report_errors


def main():
    argparse.ArgumentParser(description=__doc__).parse_args()
    problems, errors = load_problems()
    solved = {folder for folder, values in problems if values["solved"] == "true"}
    for folder in problem_folders():
        path = folder / "solution.py"
        if not path.is_file():
            continue
        try:
            code = path.read_text(encoding="utf-8")
            tree = ast.parse(code, filename=str(path))
            compile(tree, str(path), "exec")
            if folder in solved and not any(
                not (isinstance(node, ast.Expr) and isinstance(node.value, ast.Constant)
                     and isinstance(node.value.value, str)) for node in tree.body
            ):
                errors.append(f"{folder.name}: marked solved but solution.py has no code")
        except (SyntaxError, ValueError, OSError, UnicodeError) as error:
            errors.append(f"{folder.name}/solution.py: {error}")
    if errors:
        report_errors(errors)
        return 1
    print(f"Checked {len(problems)} problems: files, notes fields, and Python syntax look good.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
