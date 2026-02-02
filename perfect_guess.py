#!/usr/bin/env python3
"""
perfect_guess.py

A clean, testable number-guessing CLI game with:
- Difficulty presets (Easy/Medium/Hard) + custom range option
- Attempts limits per difficulty
- I/O separation for easy testing (inject input_fn/output_fn)
- Deterministic RNG support (pass a seed or Random instance)
- Best-score persistence per difficulty (JSON file in user home)
- Graceful KeyboardInterrupt handling
"""

from __future__ import annotations

import argparse
import json
import random
from pathlib import Path
from typing import Callable, Dict, Optional, Tuple

# Type aliases for I/O injection to make unit testing simple
InputFn = Callable[[str], str]
OutputFn = Callable[[str], None]

DEFAULT_SCORE_FILE = Path.home() / ".perfect_guess_highscores.json"


def safe_load_scores(path: Path = DEFAULT_SCORE_FILE) -> Dict[str, int]:
    """Load high scores from disk. Returns empty dict on errors or missing file."""
    try:
        if not path.exists():
            return {}
        with path.open("r", encoding="utf-8") as fh:
            data = json.load(fh)
            # validate format: expect mapping of str->int
            return {k: int(v) for k, v in data.items()}
    except Exception:
        # On any issue, don't crash the game; return empty scores
        return {}


def safe_save_scores(scores: Dict[str, int], path: Path = DEFAULT_SCORE_FILE) -> None:
    """Save high scores to disk. Swallows I/O errors to avoid breaking gameplay."""
    try:
        with path.open("w", encoding="utf-8") as fh:
            json.dump(scores, fh, indent=2)
    except Exception:
        # Intentionally ignore save errors (e.g., permission issues).
        pass


def get_valid_number(
    prompt: str,
    min_value: int,
    max_value: int,
    input_fn: InputFn = input,
    output_fn: OutputFn = print,
) -> int:
    """
    Prompt until user enters an integer between min_value and max_value.
    Uses injected input_fn/output_fn for testability.
    """
    while True:
        try:
            raw = input_fn(prompt)
            value = int(raw)
            if min_value <= value <= max_value:
                return value
            output_fn(f"⚠ Enter a number between {min_value} and {max_value}.")
        except ValueError:
            output_fn("❌ Invalid input! Please enter numbers only.")


def get_yes_no(
    prompt: str, input_fn: InputFn = input, output_fn: OutputFn = print
) -> bool:
    """
    Ask the user a yes/no question. Accepts y/yes or n/no (case-insensitive).
    Returns True for yes, False for no.
    """
    while True:
        choice = input_fn(prompt).strip().lower()
        if choice in {"y", "yes"}:
            return True
        if choice in {"n", "no"}:
            return False
        output_fn("❌ Please enter y/yes or n/no.")


def play_game(
    min_value: int,
    max_value: int,
    max_attempts: Optional[int] = None,
    rng: Optional[random.Random] = None,
    input_fn: InputFn = input,
    output_fn: OutputFn = print,
) -> Tuple[int, bool]:
    """
    Run a single game session.

    Returns:
        (attempts_used, won) where won==True if player guessed the number.
    """
    rng = rng or random.Random()
    secret_number = rng.randint(min_value, max_value)

    attempts = 0
    output_fn(f"\n🎯 Guess the number between {min_value} and {max_value}")

    while True:
        attempts += 1
        guess = get_valid_number(
            f"Attempt {attempts}: Enter your guess → ",
            min_value,
            max_value,
            input_fn,
            output_fn,
        )

        if guess < secret_number:
            output_fn("📈 Higher number please.")
        elif guess > secret_number:
            output_fn("📉 Lower number please.")
        else:
            output_fn(
                f"\n🎉 Correct! You guessed the number {secret_number} in {attempts} attempts.\n"
            )
            return attempts, True

        if max_attempts is not None and attempts >= max_attempts:
            output_fn(
                f"\n💀 Game Over! You've used all {max_attempts} attempts.\nThe correct number was {secret_number}.\n"
            )
            return attempts, False


def difficulty_presets() -> Dict[str, Dict[str, Optional[int]]]:
    """
    Return difficulty preset definitions.
    Each entry includes name, min, max, attempts.
    """
    return {
        "1": {"name": "Easy", "min": 1, "max": 9, "attempts": None},
        "2": {"name": "Medium", "min": 1, "max": 20, "attempts": 7},
        "3": {"name": "Hard", "min": 1, "max": 50, "attempts": 5},
    }


def run_interactive(
    seed: Optional[int] = None,
    score_file: Path = DEFAULT_SCORE_FILE,
    input_fn: InputFn = input,
    output_fn: OutputFn = print,
) -> None:
    """
    Full interactive loop with persistent best-score handling.
    """
    rng = random.Random(seed) if seed is not None else random.Random()
    scores = safe_load_scores(score_file)

    presets = difficulty_presets()
    best_score = scores  # dict mapping difficulty key -> best attempts (int)

    output_fn("\n..:: THE PERFECT GUESS ::..\n")

    try:
        while True:
            output_fn("Choose Difficulty:")
            for key, level in presets.items():
                attempts_str = (
                    "unlimited"
                    if level["attempts"] is None
                    else f"{level['attempts']} attempts"
                )
                output_fn(
                    f"{key}. {level['name']} ({level['min']}–{level['max']}, {attempts_str})"
                )

            output_fn("4. Custom range")
            choice = input_fn("Enter your choice (1/2/3/4): ").strip()

            if choice == "4":
                # custom range
                min_v = int(input_fn("Enter minimum (integer): ").strip())
                max_v = int(input_fn("Enter maximum (integer): ").strip())
                if min_v > max_v:
                    output_fn(
                        "Minimum must be <= maximum. Returning to difficulty menu.\n"
                    )
                    continue
                level = {"name": "Custom", "min": min_v, "max": max_v, "attempts": None}
                difficulty_key = f"custom_{min_v}_{max_v}"
            elif choice in presets:
                level = presets[choice]
                difficulty_key = choice
            else:
                output_fn("❌ Invalid choice. Try again.\n")
                continue

            attempts_used, won = play_game(
                level["min"],
                level["max"],
                level["attempts"],
                rng,
                input_fn,
                output_fn,
            )

            # Update persistent best scores only on wins
            if won:
                prev_best = best_score.get(difficulty_key)
                if prev_best is None or attempts_used < int(prev_best):
                    best_score[difficulty_key] = attempts_used
                    safe_save_scores(best_score, score_file)
                    output_fn(
                        f"🏆 New best score for {level['name']}: {attempts_used} attempts!\n"
                    )
                else:
                    output_fn(
                        f"Your attempts: {attempts_used}. Best for this difficulty: {prev_best} attempts.\n"
                    )
            else:
                output_fn("Try again to beat the best score!\n")

            if not get_yes_no("🔁 Play again? (y/n): ", input_fn, output_fn):
                output_fn("\n👋 Thanks for playing. Goodbye!\n")
                if best_score:
                    output_fn("🥇 Best scores saved:")
                    for k, v in best_score.items():
                        # Make keys readable for preset difficulties
                        title = presets[k]["name"] if k in presets else k
                        output_fn(f"- {title}: {v} attempts")
                return

    except KeyboardInterrupt:
        output_fn("\n\nInterrupted. Goodbye.")


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="Perfect Guess — a deterministic & testable number-guessing CLI"
    )
    p.add_argument(
        "--seed",
        type=int,
        help="Seed for RNG (useful for deterministic runs and testing)",
    )
    p.add_argument(
        "--reset-scores", action="store_true", help="Reset saved high scores and exit"
    )
    p.add_argument(
        "--score-file",
        type=Path,
        default=DEFAULT_SCORE_FILE,
        help="Path to store high scores (JSON)",
    )
    return p.parse_args()


def main() -> None:
    args = parse_args()

    if args.reset_scores:
        try:
            if args.score_file.exists():
                args.score_file.unlink()
            print("High scores reset.")
        except Exception:
            print("Failed to reset high scores (permission or file error).")
        return

    run_interactive(seed=args.seed, score_file=args.score_file)


if __name__ == "__main__":
    main()
