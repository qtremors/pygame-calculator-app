# Pygame Calculator - Developer Documentation

> Comprehensive documentation for developers working on the Pygame Calculator.

**Version:** 2.0.0 | **Last Updated:** 2026-01-12

---

## Table of Contents

- [Architecture Overview](#architecture-overview)
- [Project Structure](#project-structure)
- [Configuration](#configuration)
- [Testing](#testing)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)

---

## Architecture Overview

Pygame Calculator follows a **Component-based OOP** architecture:

```
┌──────────────────────────────────────────────────────────────┐
│                        App Orchestrator                      │
│            Main loop, event handling, and UI sync.           │
└──────────────────────────────────────────────────────────────┘
                               │
                               ▼
┌──────────────────────────────────────────────────────────────┐
│                         UI Components                        │
│          Animated buttons, Display, and History Panel.       │
└──────────────────────────────────────────────────────────────┘
                               │
                               ▼
┌──────────────────────────────────────────────────────────────┐
│                      Expression Engine                       │
│      Safe math evaluation using Shunting Yard algorithm.     │
└──────────────────────────────────────────────────────────────┘
```

### Key Design Decisions

| Decision | Rationale |
|----------|-----------|
| **Shunting Yard Parser** | Avoids the security risks of `eval()` while providing precise control over operator precedence. |
| **Custom Animation Engine** | Implements manual linear interpolation (LERP) and easing for high-performance, smooth GUI interactions. |
| **State-Display Decoupling** | The engine maintains a pure `CalculatorState` that is rendered by the UI layer independent of calculation logic. |

---

## Project Structure

```
pygame-calculator-app/
├── assets/                   # Static assets like icons and preview images
├── .github/                  # CI/CD and GitHub automation
│   └── workflows/
│       └── tests.yml         # GitHub Actions test runner
├── calculator.py             # Main entry point; contains the CalculatorApp class
├── calculator_engine.py      # Core logic; contains the Shunting Yard engine
├── ui_components.py          # UI layer; contains generic and specific UI elements
├── config.py                 # Central config for colors, dimensions, and layout
├── README.md                 # User-facing documentation
├── DEVELOPMENT.md            # This file
├── CHANGELOG.md              # Version history
├── LICENSE.md                # License terms
└── pyproject.toml            # Project dependencies and build configuration
```

---

## Configuration

The application is highly configurable via `config.py`.

### Theme Colors
Defined in the `Colors` dataclass using RGB tuples.
- `background`: Main window background.
- `surface`: Base color for components.
- `button_operator`: Accent color for mathematical operators.

### Layout Dimensions
Defined in the `Dimensions` dataclass.
- `screen_width/height`: Main window dimensions.
- `button_margin`: Spacing between button elements.
- `border_radius`: Rounding for all UI rectangles.

---

## Key Components

### CalculatorEngine
The safest way to solve math.
- `calculate()`: Tokenizes the input and evaluates the internal postfix expression.
- `_tokenize()`: Converts the string expression into semantic tokens.

### Button
A self-contained animated element.
- `update(dt, mouse_pos)`: Updates the hover and press animation progress.
- `draw(screen, ...)`: Renders the button with interpolated colors and scale.

---

## Testing

### Running Tests

```bash
# Run all tests using pytest
uv run pytest

# Run with verbose output
uv run pytest -v
```

### Test Coverage
The project includes 34 test cases in `test_calculator.py` covering:
- Basic operations and operator precedence.
- Edge cases like division by zero and modulo zero.
- Decimal precision and negative number handling.
- Internal state management (Clear, Backspace, History).

---

## Deployment

### Local Development
1. Ensure you have `uv` installed (`pip install uv`).
2. Run `uv sync` to install dependencies.
3. Run `uv run calculator` to start the app.

### CI/CD
GitHub Actions is configured to run tests on every push and pull request across Windows, Linux, and macOS.

---

## Troubleshooting

### High CPU Usage
Ensure the delta time (`dt`) is being calculated correctly in the main loop. The app is capped at 60 FPS to minimize resource usage.

### Missing Icons
Verify that the `assets/` folder contains all required files defined in the `_set_icon` method.

---

## Contributing

### Code Style
- Follow PEP 8 guidelines.
- Use type hints for all function signatures.
- Keep the `CalculatorEngine` decoupled from Pygame-specific logic.

---

<p align="center">
  <a href="README.md">← Back to README</a>
</p>
