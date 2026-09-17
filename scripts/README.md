# Scripts

Run these from the repository folder. Only Python is needed.

Create a problem by entering its number, name, and difficulty:

```bash
python3 scripts/new_problem.py 1 "Two Sum" --difficulty Easy
```

This creates a blank `solution.py` and a short `notes.md`. When you've solved the problem, change `solved: false` to `solved: true` at the top of its notes. This is how the scripts count solved problems. The optional `review_after:` field can stay blank or hold a date such as `2026-09-24`.

List and filter problems (filters can be combined):

```bash
python3 scripts/review_queue.py
python3 scripts/review_queue.py --number 1
python3 scripts/review_queue.py --name sum
python3 scripts/review_queue.py --difficulty Easy --solved
python3 scripts/review_queue.py --unsolved
```

The list shows your overall solved count, how many problems match the filters, and each problem's number, name, difficulty, solved status, and review date if set.

```bash
python3 scripts/check_repo.py
python3 scripts/update_readme.py
```

`check_repo.py` catches duplicate numbers, missing files, invalid notes fields, Python syntax errors, and empty solutions marked as solved. It does not run your code or judge whether the solution is correct.

`update_readme.py` refreshes the solved total, difficulty counts, and links to solved problems in the root README. It edits only the generated progress section, preserving your own writing. It does not commit or push anything to GitHub.
