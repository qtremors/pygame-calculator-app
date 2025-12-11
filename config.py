"""
Configuration module for the Pygame Calculator.
Contains all theme, layout, and application constants.
"""
from dataclasses import dataclass
from typing import Tuple

# Type alias for RGB colors
Color = Tuple[int, int, int]


@dataclass(frozen=True)
class Colors:
    """Modern dark theme color palette with glassmorphism-inspired tones."""
    # Backgrounds
    background: Color = (18, 18, 24)
    surface: Color = (28, 28, 38)
    display_bg: Color = (22, 22, 32)
    history_bg: Color = (25, 25, 35)
    
    # Buttons
    button_number: Color = (45, 45, 65)
    button_number_hover: Color = (60, 60, 85)
    button_operator: Color = (88, 86, 214)
    button_operator_hover: Color = (108, 106, 234)
    button_equals: Color = (79, 195, 247)
    button_equals_hover: Color = (99, 215, 255)
    button_clear: Color = (255, 107, 129)
    button_clear_hover: Color = (255, 130, 150)
    
    # Text
    text_primary: Color = (255, 255, 255)
    text_secondary: Color = (180, 180, 200)
    text_muted: Color = (120, 120, 140)
    
    # Accents
    accent: Color = (147, 112, 219)
    error: Color = (255, 107, 129)
    scrollbar_track: Color = (40, 40, 55)
    scrollbar_thumb: Color = (80, 80, 110)


@dataclass(frozen=True)
class Dimensions:
    """Screen and layout dimensions."""
    screen_width: int = 400
    screen_height: int = 650
    button_margin: int = 10
    border_radius: int = 12
    display_height: int = 100
    history_height: int = 180
    button_cols: int = 4
    button_rows: int = 5


@dataclass(frozen=True)
class FontSizes:
    """Font size configuration."""
    display: int = 72
    button: int = 44
    history: int = 26
    key_hint: int = 18
    clear_btn: int = 22


# Application metadata
APP_NAME = "Pygame Calculator"
APP_VERSION = "2.0.0"
HISTORY_FILE = "calculator_history.txt"
MAX_HISTORY_ENTRIES = 100

# Button layout: (text, grid_pos, span, keyboard_hint, button_type)
# button_type: "number", "operator", "equals", "clear", "function"
BUTTON_LAYOUT = [
    ("C",   (0, 0), (1, 1), "Del/C",  "clear"),
    ("+/-", (0, 1), (1, 1), "",       "function"),
    ("%",   (0, 2), (1, 1), "%",      "function"),
    ("/",   (0, 3), (1, 1), "/",      "operator"),
    ("7",   (1, 0), (1, 1), "7",      "number"),
    ("8",   (1, 1), (1, 1), "8",      "number"),
    ("9",   (1, 2), (1, 1), "9",      "number"),
    ("*",   (1, 3), (1, 1), "*",      "operator"),
    ("4",   (2, 0), (1, 1), "4",      "number"),
    ("5",   (2, 1), (1, 1), "5",      "number"),
    ("6",   (2, 2), (1, 1), "6",      "number"),
    ("-",   (2, 3), (1, 1), "-",      "operator"),
    ("1",   (3, 0), (1, 1), "1",      "number"),
    ("2",   (3, 1), (1, 1), "2",      "number"),
    ("3",   (3, 2), (1, 1), "3",      "number"),
    ("+",   (3, 3), (1, 1), "+",      "operator"),
    ("0",   (4, 0), (2, 1), "0",      "number"),
    (".",   (4, 2), (1, 1), ".",      "number"),
    ("=",   (4, 3), (1, 1), "Enter",  "equals"),
]
