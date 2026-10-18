# 🏏 Odd or Eve

**Hand cricket against the computer, right in your terminal.**

[![tests](https://github.com/Ishaan7497/Odd-Or-Eve/actions/workflows/tests.yml/badge.svg)](https://github.com/Ishaan7497/Odd-Or-Eve/actions/workflows/tests.yml)
![Python](https://img.shields.io/badge/python-3.9%2B-blue)
![Dependencies](https://img.shields.io/badge/dependencies-none-brightgreen)
[![License: MIT](https://img.shields.io/badge/license-MIT-green)](LICENSE)

## About

Inspired by the traditional Indian hand game Odd or Eve (Hand Cricket), this project digitizes a game that children commonly play using fingers and quick mental math. The Python program simulates the same rules in a command-line environment, allowing the player to face off against the computer.

It uses only the Python standard library. The scoring rules are kept in small, pure functions, and every input is validated, so typos, blank lines and out-of-range numbers are asked again instead of crashing the game. A test suite covers the rules, the input handling and complete games.

> 🎥 **Sequel:** [Odd_or_Eve_CV](https://github.com/Ishaan7497/Odd_or_Eve_CV) plays the same game with real hand gestures through a webcam, using computer vision.

## How to play

```bash
git clone https://github.com/Ishaan7497/Odd-Or-Eve.git
cd Odd-Or-Eve
python odd_or_eve.py
```

1. **Pick a mode:** `1` for 1 to 6, `2` for 1 to 10, or `3` for CRAZY.
2. **Toss:** call `odd` or `eve`, then pick 1 or 2. The computer picks too, and the sum decides who wins. The winner chooses to `bat` or `bowl`.
3. **Batting:** type a number. You score that many runs, unless the computer bowled the **same** number, in which case you're **out**.
4. **Bowling:** try to guess the computer's number to get it out.
5. **The chase:** the second innings ends when the batter is out or passes the target.
6. **Tie?** It goes to a **super over**: 6 balls each. Getting out costs that ball's runs, but you keep batting.

### CRAZY mode
- Numbers next to each other (like 4 vs 5, or 10 vs 1) are **out**.
- The **same** number scores its **square**: 7 vs 7 = 49 runs!

## Example

```
Batting (1 to 6): 4
You scored 4
Total runs: 4

Batting (1 to 6): 6
OUT! The computer bowled you out! The computer bowled 6.
Target to win: 5
```

## Testing

```bash
pip install pytest
pytest
```

The tests cover every scoring pair in every mode, invalid input (letters, blanks, negatives, decimals, out-of-range numbers), innings and chase endings, super overs, complete games, and Ctrl-C. They run on every push with GitHub Actions.

## License

[MIT](LICENSE)
