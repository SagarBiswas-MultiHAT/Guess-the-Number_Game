# Perfect Guess

<div align="right">

[![CI](https://github.com/SagarBiswas-MultiHAT/GuessTheNumber-Game/actions/workflows/ci.yml/badge.svg)](https://github.com/SagarBiswas-MultiHAT/GuessTheNumber-Game/actions/workflows/ci.yml)
[![Python](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/)
[![Tests](https://img.shields.io/badge/tests-pytest-brightgreen)](https://github.com/SagarBiswas-MultiHAT/GuessTheNumber-Game/actions)
[![License](https://img.shields.io/github/license/SagarBiswas-MultiHAT/GuessTheNumber-Game)](https://github.com/SagarBiswas-MultiHAT/GuessTheNumber-Game/blob/main/LICENSE)
[![Last commit](https://img.shields.io/github/last-commit/SagarBiswas-MultiHAT/GuessTheNumber-Game)](https://github.com/SagarBiswas-MultiHAT/GuessTheNumber-Game)
[![Issues](https://img.shields.io/github/issues/SagarBiswas-MultiHAT/GuessTheNumber-Game)](https://github.com/SagarBiswas-MultiHAT/GuessTheNumber-Game/issues)

</div>

A small, well-tested, and production-quality CLI number-guessing game written in Python.
This repository demonstrates clean separation of concerns, deterministic testing, persistent user state, and GitHub Actions CI — ideal for portfolios and interviews.

## Features

## Quick start

```bash
# run locally
python perfect_guess.py

# deterministic run (useful for testing)
python perfect_guess.py --seed 12345

# reset high scores
python perfect_guess.py --reset-scores

# Perfect Guess — deterministic & testable number-guessing CLI

[![CI](https://github.com/OWNER/REPO/actions/workflows/ci.yml/badge.svg)](https://github.com/OWNER/REPO/actions/workflows/ci.yml)

A small, friendly, and thoroughly testable command-line number-guessing game. The codebase emphasizes clarity and developer ergonomics: I/O injection for tests, deterministic RNG for reproducible runs, and simple persistent best-score storage.

**Why read this README?** It explains everything you need: features, how to play, how to run tests locally, and how to get a green check on the GitHub Actions CI badge.

**Highlights**
- Clean CLI with difficulty presets and custom ranges.
- Test-friendly design: functions accept `input_fn`/`output_fn` for easy unit tests.
- Deterministic runs via `--seed` for reproducible behavior.
- Persistent best-score storage (JSON) saved in the user home by default.
- GitHub Actions workflow included to run `ruff`, `black --check`, and `pytest`.

**Files of interest**
- `perfect_guess.py`: Main program and library code ([perfect_guess.py](perfect_guess.py#L1-L400)).
- `.github/workflows/ci.yml`: CI workflow ([.github/workflows/ci.yml](.github/workflows/ci.yml)).
- `tests/test_perfect_guess.py`: Unit tests ([tests/test_perfect_guess.py](tests/test_perfect_guess.py#L1-L200)).

**Quick start — Play now**

Run the program directly (no install required):

```bash
python perfect_guess.py
```

Useful options:

- `--seed N` — use deterministic RNG seed.
- `--reset-scores` — delete saved high scores and exit.
- `--score-file PATH` — store scores to a custom path (default: `~/.perfect_guess_highscores.json`).

Example deterministic run:

```bash
python perfect_guess.py --seed 42
```

**Gameplay summary**

- Choose a difficulty: Easy / Medium / Hard or a custom numeric range.
- Hints tell you to guess higher or lower.
- Medium & Hard have attempt limits; Easy and custom are unlimited unless specified.
- Winning with fewer attempts updates a per-difficulty best score stored on disk.

**Development & testing (local)**

The CI runs the following checks. Run them locally to ensure parity before pushing:

```bash
python -m pip install --upgrade pip
pip install pytest black ruff

# Run linting and format checks (same as CI)
ruff .
black --check .
pytest -q
```

If `black --check .` fails, run `black .` to auto-format, then re-run checks.

**CI (GitHub Actions) — how it runs & getting a green tick**

The workflow `.github/workflows/ci.yml` is configured to run on pushes and PRs targeting `main`. It installs dependencies, runs `ruff` (lint), verifies formatting with `black --check`, and executes tests with `pytest`.

Badge instructions

- Replace `OWNER/REPO` in the badge link at the top of this file with your GitHub user/org and repository name so the badge points to your repository.
- Badge SVG: `https://github.com/OWNER/REPO/actions/workflows/ci.yml/badge.svg`
- Workflow page: `https://github.com/OWNER/REPO/actions/workflows/ci.yml`

To get the green check on that badge:

1. Run the local commands above and confirm `ruff`, `black --check`, and `pytest` pass for your environment.
2. Commit and push your branch to GitHub (or open a PR against `main`).
3. The workflow will run automatically; if all steps succeed, the badge will show success.

Notes: the badge reports status for the default branch and the workflow named `ci.yml`. If your repo or branch is different, adjust the badge URL accordingly.

**Design notes**

- I/O injection and deterministic RNG are intentional: they make unit tests simple and reliable.
- The high-score saving intentionally ignores(save errors to avoid breaking the user experience when the home directory is not writable.

**Contributing**

- Open issues or PRs for fixes and improvements.
- Keep changes formatted with `black` and ensure tests pass locally.

**Troubleshooting**

- If `ruff .` reports style issues, fix them or add a targeted suppression.
- If `black --check .` fails, run `black .`.
- For failing tests, run `pytest -q` and inspect the traceback.

**License**

- Add a license file if you plan to publish or reuse this project broadly.

---
