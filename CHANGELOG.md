# Pygame Calculator Changelog

> **Project:** Pygame Calculator
> **Version:** 0.0.2
> **Last Updated:** 2025-12-11

---

## [0.0.2] - 2025-12-11

### Added
- Standard arithmetic: `+`, `-`, `*`, `/`, `%`, `+/-` toggle.
- Safe expression parser using the Shunting Yard algorithm (removed `eval()` usage).
- Modern dark theme UI with smooth animations and scale effects.
- Dynamic font scaling for fitting long expressions in display.
- Scrollable and persistent calculation history.
- Full keyboard and Numpad support.
- CI/CD workflow for automated cross-platform testing.
- Dependency management using `uv`.

### Changed
- Migrated from vanilla Pygame to Pygame-CE (Community Edition).
- Refactored UI components into a modular structure (`ui_components.py`).
- Switched to `pyproject.toml` for project configuration.

### Fixed
- Improved division by zero handling with specialized error messages.
- Fixed floating point noise in results (limited to 10 decimal places).

---

## [0.0.1] - 2025-07-21

### Added
- Initial release with basic arithmetic operations.
- Simple Pygame GUI.
