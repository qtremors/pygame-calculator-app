# Pygame Calculator - Tasks

> **Project:** Pygame Calculator  
> **Version:** 2.0.0  
> **Last Updated:** 2026-01-12

---

## ✅ Completed (v2.0.0)

### Engine & Logic
- [x] Implement Shunting Yard expression parser.
- [x] Replace `eval()` with safe tokenization.
- [x] Support for operator precedence and parentheses.
- [x] Persistent history storage in text format.

### UI & UX
- [x] Design modern dark theme with Glassmorphism tones.
- [x] Implement cubic easing for hover and press animations.
- [x] Dynamic font scaling for the display area.
- [x] Multi-platform keyboard and Numpad support.

---

## 🚧 In Progress

### Documentation
- [/] Aligning all project docs with the new Tremors branding templates.

---

## 📋 To Do

### High Priority
- [ ] **Scientific Mode**
  - Add support for `sin`, `cos`, `tan`, `log`, and `sqrt`.
- [ ] **Theme Switcher**
  - Allow users to toggle between dark, light, and high-contrast modes.

### Medium Priority
- [ ] **Bracket Support in UI**
  - Add `(` and `)` buttons to the grid (engine already supports them).
- [ ] **History Export**
  - Allow exporting history to `.csv` or `.json` formats.

### Low Priority
- [ ] **Sound Effects**
  - Optional subtle click sounds for button presses.

---

## 🏗️ Architecture Notes

- Keep `calculator_engine.py` completely platform-agnostic (no Pygame imports).
- Use `config.py` as the single source for all UI tokens.

---
