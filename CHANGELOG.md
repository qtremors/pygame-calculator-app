# Pygame Calculator Changelog

> **Project:** Pygame Calculator  
> **Version:** 2.0.0  
> **Last Updated:** 2026-01-12

---

## [2.0.0] - 2026-01-12

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

## [1.0.0] - 2025-12-15

### Added
- Initial release with basic arithmetic operations.
- Simple Pygame GUI.
