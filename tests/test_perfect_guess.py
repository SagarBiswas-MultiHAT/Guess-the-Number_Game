#!/usr/bin/env python3
import random

import perfect_guess as pg


def test_get_valid_number_accepts_valid_input(monkeypatch, capsys):
    inputs = iter(["5"])
    monkeypatch.setattr("builtins.input", lambda prompt="": next(inputs))
    v = pg.get_valid_number("prompt", 1, 10, input_fn=input)
    assert v == 5


def test_get_valid_number_rejects_non_int_then_accepts(monkeypatch, capsys):
    inputs = iter(["x", "12", "7"])
    monkeypatch.setattr("builtins.input", lambda prompt="": next(inputs))
    outputs = []
    monkeypatch.setattr(
        "builtins.print",
        lambda *args, **kwargs: outputs.append(" ".join(map(str, args))),
    )
    v = pg.get_valid_number("prompt", 1, 10, input_fn=input, output_fn=print)
    assert v == 7
    # ensure error message printed at least once
    assert any("Invalid input" in o or "Enter a number between" in o for o in outputs)


def test_play_game_win_and_loss(monkeypatch):
    # Deterministic RNG with seed that guarantees a number => seed 0
    rng = random.Random(0)
    # For the seeded RNG and range 1..10, secret is deterministic
    # We'll feed guesses to hit the secret
    secret = rng.randint(1, 10)
    # Reset RNG for the game
    rng = random.Random(0)
    inputs = iter([str(secret)])
    monkeypatch.setattr("builtins.input", lambda prompt="": next(inputs))
    attempts, won = pg.play_game(1, 10, rng=rng, input_fn=input)
    assert won is True
    assert attempts == 1


def test_scores_persistence(tmp_path):
    p = tmp_path / "scores.json"
    scores = {"1": 3, "2": 5}
    pg.safe_save_scores(scores, path=p)
    loaded = pg.safe_load_scores(path=p)
    assert loaded == {"1": 3, "2": 5}
