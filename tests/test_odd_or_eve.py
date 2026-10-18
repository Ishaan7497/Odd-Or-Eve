import itertools
import os
import random
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import odd_or_eve as game  # noqa: E402


# ── helpers ──────────────────────────────────────────────────────────────────

def feed(monkeypatch, *answers):
    """Make input() return these answers in order (fails if more are needed)."""
    it = iter(answers)
    monkeypatch.setattr("builtins.input", lambda prompt="": next(it))


def fix_computer(monkeypatch, *numbers):
    """Make the computer play these numbers in order."""
    it = iter(numbers)
    monkeypatch.setattr(game.random, "randint", lambda a, b: next(it))


# ── scoring rules ────────────────────────────────────────────────────────────

@pytest.mark.parametrize("mode,rng", [("1 to 6", range(1, 7)), ("1 to 10", range(1, 11))])
def test_normal_modes_out_only_on_same_number(mode, rng):
    for bat, bowl in itertools.product(rng, repeat=2):
        expected = (0, True) if bat == bowl else (bat, False)
        assert game.resolve_ball(bat, bowl, mode) == expected


@pytest.mark.parametrize("bat,bowl", [(3, 4), (4, 3), (1, 2), (9, 10), (1, 10), (10, 1)])
def test_crazy_adjacent_is_out(bat, bowl):
    assert game.resolve_ball(bat, bowl, "CRAZY") == (0, True)


@pytest.mark.parametrize("n", range(1, 11))
def test_crazy_same_number_scores_square(n):
    assert game.resolve_ball(n, n, "CRAZY") == (n * n, False)


def test_crazy_other_numbers_score_normally():
    for bat, bowl in itertools.product(range(1, 11), repeat=2):
        if abs(bat - bowl) in (0, 1, 9):
            continue
        assert game.resolve_ball(bat, bowl, "CRAZY") == (bat, False)


def test_super_over_same_number_is_out():
    assert game.resolve_ball(4, 4, "super_over") == (0, True)
    assert game.resolve_ball(4, 2, "super_over") == (4, False)


# ── input validation ─────────────────────────────────────────────────────────

@pytest.mark.parametrize("bad", ["", " ", "abc", "-1", "0", "7", "3.5", "1e3"])
def test_ask_number_rejects_bad_input_then_accepts_valid(monkeypatch, capsys, bad):
    feed(monkeypatch, bad, "4")
    assert game.ask_number("> ", range(1, 7)) == 4
    assert "Please enter a number" in capsys.readouterr().out


def test_ask_number_strips_spaces(monkeypatch):
    feed(monkeypatch, "  5  ")
    assert game.ask_number("> ", range(1, 7)) == 5


@pytest.mark.parametrize("answer,expected", [("odd", "ODD"), ("ODD", "ODD"), (" Eve ", "EVE"), ("even", "EVE")])
def test_toss_call_accepts_any_case_and_even(monkeypatch, answer, expected):
    feed(monkeypatch, answer)
    assert game.ask_choice("> ", {"ODD": "ODD", "EVE": "EVE", "EVEN": "EVE"}) == expected


def test_ask_choice_repeats_until_valid(monkeypatch, capsys):
    feed(monkeypatch, "maybe", "", "bowl")
    assert game.ask_choice("> ", {"BAT": "BAT", "BOWL": "BOWL"}) == "BOWL"
    assert capsys.readouterr().out.count("Please type one of") == 2


@pytest.mark.parametrize("answer,expected", [
    ("1", ("1 to 6", range(1, 7))),
    ("2", ("1 to 10", range(1, 11))),
    ("3", ("CRAZY", range(1, 11))),
])
def test_select_mode(monkeypatch, answer, expected):
    feed(monkeypatch, "9", answer)
    assert game.select_mode() == expected


# ── innings ──────────────────────────────────────────────────────────────────

def test_batting_ends_at_first_wicket(monkeypatch):
    fix_computer(monkeypatch, 1, 2, 3)
    feed(monkeypatch, "4", "5", "3")
    assert game.batting(range(1, 7), "1 to 6") == 9


def test_out_first_ball_scores_zero(monkeypatch):
    fix_computer(monkeypatch, 2)
    feed(monkeypatch, "2")
    assert game.batting(range(1, 7), "1 to 6") == 0


def test_bowling_counts_computer_runs(monkeypatch):
    fix_computer(monkeypatch, 6, 6, 1)
    feed(monkeypatch, "2", "3", "1")
    assert game.bowling(range(1, 7), "1 to 6") == 12


def test_chase_stops_once_target_passed(monkeypatch):
    fix_computer(monkeypatch, 1, 1)          # only two balls should be needed
    feed(monkeypatch, "6", "6")
    assert game.batting(range(1, 7), "1 to 6", target=10) == 12


def test_equalling_target_does_not_end_chase(monkeypatch):
    fix_computer(monkeypatch, 1, 1, 5)
    feed(monkeypatch, "5", "5", "5")
    assert game.batting(range(1, 7), "1 to 6", target=10) == 10


def test_crazy_squares_and_adjacent_out(monkeypatch):
    fix_computer(monkeypatch, 7, 1, 4)
    feed(monkeypatch, "7", "5", "5")         # 49, +5, then 5 vs 4 = out
    assert game.batting(range(1, 11), "CRAZY") == 54


def test_super_over_is_six_balls_and_wickets_cost_only_that_ball(monkeypatch):
    fix_computer(monkeypatch, 1, 2, 3, 4, 5, 6)
    feed(monkeypatch, "1", "3", "3", "5", "5", "1")
    assert game.batting(range(1, 7), "super_over") == 3 + 5 + 1


def test_super_over_chase_stops_early(monkeypatch):
    fix_computer(monkeypatch, 6, 6)
    feed(monkeypatch, "1", "1")
    assert game.bowling(range(1, 7), "super_over", target=10) == 12


# ── whole games ──────────────────────────────────────────────────────────────

def test_full_game_runs_without_crashing(monkeypatch, capsys):
    random.seed(0)
    answers = {"Enter:": "2", "Odd or Eve": "odd", "toss": "1", "BAT or BOWL": "bat",
               "Play again": "n"}
    plays = itertools.cycle(["1", "4", "7", "10", "2", "9", "3"])

    def fake_input(prompt=""):
        for key, value in answers.items():
            if key in prompt:
                return value
        return next(plays)

    monkeypatch.setattr("builtins.input", fake_input)
    game.main()
    out = capsys.readouterr().out
    assert any(r in out for r in ("You win!", "You lose!", "tie"))
    assert "Exiting..." in out


@pytest.mark.parametrize("error", [KeyboardInterrupt, EOFError])
def test_ctrl_c_and_end_of_input_exit_cleanly(monkeypatch, capsys, error):
    def boom(prompt=""):
        raise error
    monkeypatch.setattr("builtins.input", boom)
    game.main()
    assert "Exiting..." in capsys.readouterr().out


def test_computer_number_is_not_shown_before_player_chooses(monkeypatch, capsys):
    fix_computer(monkeypatch, 3)
    shown_before = []

    def spy(prompt=""):
        shown_before.append(capsys.readouterr().out)
        return "3"

    monkeypatch.setattr("builtins.input", spy)
    game.batting(range(1, 7), "1 to 6")
    assert "3" not in shown_before[0].replace("1 to 6", "")
