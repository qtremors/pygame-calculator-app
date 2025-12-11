# 🧮 Pygame Calculator

A modern desktop calculator built with Python and Pygame-CE featuring a dark theme, smooth animations, and a safe expression parser.

<img src="screenshots/home.png" alt="Home Screen" width="350"/>

## Features

- Standard arithmetic: `+`, `-`, `*`, `/`, `%`, `+/-`
- Full keyboard support
- Persistent calculation history
- Smooth hover/press animations
- Safe expression parsing (no `eval()`)

## Quick Start

```bash
# Install and run with uv
uv sync
uv run python calculator.py

# Or with pip
pip install pygame-ce
python calculator.py
```

## Controls

| Action | Keyboard |
|--------|----------|
| Numbers | `0-9`, `.` |
| Operators | `+`, `-`, `*`, `/` |
| Calculate | `Enter` |
| Clear | `C` / `Delete` |
| Backspace | `Backspace` |
| Exit | `Esc` |

## Project Structure

```
├── calculator.py        # App entry point
├── config.py            # Colors, dimensions, constants
├── calculator_engine.py # Safe expression parser
├── ui_components.py     # Animated UI components
└── test_calculator.py   # Tests (34 cases)
```