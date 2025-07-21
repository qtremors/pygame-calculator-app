# pygame_calculator_final_v5.py

import pygame
import sys
import os

# ==============================================================================
# 1. SETUP AND INITIALIZATION
# ==============================================================================

pygame.init()

# Screen Dimensions
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 650
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pygame Calculator")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIGHT_GRAY = (235, 235, 235)
DARK_GRAY = (50, 50, 50)
GRAY_SCROLLBAR = (200, 200, 200)
BUTTON_BLUE = (30, 144, 255)
BUTTON_HOVER_BLUE = (100, 180, 255)
ERROR_RED = (220, 20, 60)
CLEAR_BUTTON_RED = (255, 80, 80)

# Fonts
font_display = pygame.font.Font(None, 80)
font_button = pygame.font.Font(None, 48)
font_history = pygame.font.Font(None, 28)
font_key_label = pygame.font.Font(None, 20)
font_clear_btn = pygame.font.Font(None, 25)

# Calculator State
current_expression = ""
history = []
HISTORY_FILE = "calculator_history.txt"
is_result_displayed = False
history_scroll_offset = 0

# ==============================================================================
# 2. UI LAYOUT AND CONFIGURATION
# ==============================================================================

display_rect = pygame.Rect(20, 20, SCREEN_WIDTH - 40, 100)
history_rect = pygame.Rect(20, 130, SCREEN_WIDTH - 40, 180)
# --- FIX: Moved the button left by changing -22 to -35 ---
clear_history_rect = pygame.Rect(history_rect.right - 35, history_rect.top + 5, 20, 20)

BUTTON_MARGIN = 10
button_grid_start_y = history_rect.bottom + BUTTON_MARGIN
grid_height = SCREEN_HEIGHT - button_grid_start_y - BUTTON_MARGIN
BUTTON_COLS = 4
BUTTON_ROWS = 5
BUTTON_WIDTH = (SCREEN_WIDTH - (BUTTON_COLS + 1) * BUTTON_MARGIN) / BUTTON_COLS
BUTTON_HEIGHT = (grid_height - (BUTTON_ROWS - 1) * BUTTON_MARGIN) / BUTTON_ROWS
button_layout = [
    ('C',   (0, 0), (1, 1), 'Del'), ('+/-', (0, 1), (1, 1), ''),   ('%',   (0, 2), (1, 1), '%'), ('/',   (0, 3), (1, 1), '/'),
    ('7',   (1, 0), (1, 1), '7'),   ('8',   (1, 1), (1, 1), '8'),   ('9',   (1, 2), (1, 1), '9'), ('*',   (1, 3), (1, 1), '*'),
    ('4',   (2, 0), (1, 1), '4'),   ('5',   (2, 1), (1, 1), '5'),   ('6',   (2, 2), (1, 1), '6'), ('-',   (2, 3), (1, 1), '-'),
    ('1',   (3, 0), (1, 1), '1'),   ('2',   (3, 1), (1, 1), '2'),   ('3',   (3, 2), (1, 1), '3'), ('+',   (3, 3), (1, 1), '+'),
    ('0',   (4, 0), (2, 1), '0'),   ('.',   (4, 2), (1, 1), '.'),   ('=',   (4, 3), (1, 1), 'Enter'),
]
buttons = {}
for text, grid_pos, span, key_label in button_layout:
    row, col = grid_pos; col_span, row_span = span
    x = BUTTON_MARGIN + col * (BUTTON_WIDTH + BUTTON_MARGIN)
    y = button_grid_start_y + row * (BUTTON_HEIGHT + BUTTON_MARGIN)
    width = col_span * BUTTON_WIDTH + (col_span - 1) * BUTTON_MARGIN
    height = row_span * BUTTON_HEIGHT + (row_span - 1) * BUTTON_MARGIN
    buttons[text] = {'rect': pygame.Rect(x, y, width, height), 'key_label': key_label}

# ==============================================================================
# 3. HISTORY MANAGEMENT (File I/O)
# ==============================================================================
def save_history():
    with open(HISTORY_FILE, 'w') as f:
        for entry in history: f.write(entry + '\n')

def load_history():
    global history
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, 'r') as f:
            history = [line.strip() for line in f if line.strip()]

def clear_history():
    global history, history_scroll_offset
    history.clear()
    history_scroll_offset = 0
    save_history()

# ==============================================================================
# 4. CORE CALCULATOR LOGIC
# ==============================================================================
def process_input(value):
    global current_expression, history, is_result_displayed
    if is_result_displayed and value not in ['=', '+/-', '%']:
        if value in "0123456789.": current_expression = ""
        is_result_displayed = False
    if value == 'C': current_expression = ""; is_result_displayed = False
    elif value == '=':
        if not current_expression: return
        try:
            result = str(eval(current_expression))
            history.append(f"{current_expression} = {result}")
            if len(history) > 100: history.pop(0)
            current_expression = result; save_history(); is_result_displayed = True
        except ZeroDivisionError: current_expression = "Error: Cannot divide by zero"; is_result_displayed = True
        except (SyntaxError, NameError): current_expression = "Error: Invalid syntax"; is_result_displayed = True
        except Exception as e: current_expression = "Error"; is_result_displayed = True; print(f"Error: {e}")
    elif value == '+/-':
        if current_expression.startswith("Error"): return
        if current_expression and current_expression[0] == '-': current_expression = current_expression[1:]
        elif current_expression: current_expression = '-' + current_expression
    elif value == '%':
        if not current_expression or current_expression.startswith("Error"): return
        try:
            current_expression = str(float(current_expression) / 100); is_result_displayed = True
        except (ValueError, TypeError): current_expression = "Error: Invalid input for %"; is_result_displayed = True
    elif value == 'backspace':
        if is_result_displayed or current_expression.startswith("Error"): current_expression = ""; is_result_displayed = False
        else: current_expression = current_expression[:-1]
    else:
        if current_expression == "0" and value != '.': current_expression = ""
        current_expression += value

# ==============================================================================
# 5. DRAWING FUNCTIONS (VIEW)
# ==============================================================================
def draw_ui():
    screen.fill(WHITE)
    mouse_pos = pygame.mouse.get_pos()
    pygame.draw.rect(screen, DARK_GRAY, display_rect, border_radius=10)
    text_color = ERROR_RED if current_expression.startswith("Error") else WHITE
    display_text = current_expression or "0"
    font = font_display
    text_surf = font.render(display_text, True, text_color)
    available_width = display_rect.width - 30
    if text_surf.get_width() > available_width:
        scale_factor = available_width / text_surf.get_width()
        new_font_size = int(font.get_height() * scale_factor)
        font = pygame.font.Font(None, min(font_display.get_height(), new_font_size))
        text_surf = font.render(display_text, True, text_color)
    text_rect = text_surf.get_rect(midright=(display_rect.right - 15, display_rect.centery))
    screen.blit(text_surf, text_rect)
    pygame.draw.rect(screen, LIGHT_GRAY, history_rect, border_radius=10)
    clip_area = history_rect.inflate(-20, -20)
    screen.set_clip(clip_area)
    y_offset = clip_area.top
    line_height = font_history.get_linesize()
    max_lines = clip_area.height // line_height
    reversed_history = list(reversed(history))
    visible_slice = reversed_history[history_scroll_offset : history_scroll_offset + max_lines]
    for entry in visible_slice:
        history_surf = font_history.render(entry, True, DARK_GRAY)
        screen.blit(history_surf, (clip_area.left, y_offset))
        y_offset += line_height
    screen.set_clip(None)
    if len(history) > max_lines:
        scrollbar_track_rect = pygame.Rect(history_rect.right - 12, history_rect.top, 7, history_rect.height)
        pygame.draw.rect(screen, GRAY_SCROLLBAR, scrollbar_track_rect, border_radius=3)
        viewable_ratio = max_lines / len(history)
        thumb_height = history_rect.height * viewable_ratio
        scroll_ratio = history_scroll_offset / (len(history) - max_lines)
        thumb_y = history_rect.top + (history_rect.height - thumb_height) * scroll_ratio
        thumb_rect = pygame.Rect(scrollbar_track_rect.left, thumb_y, 7, thumb_height)
        pygame.draw.rect(screen, DARK_GRAY, thumb_rect, border_radius=3)
    if history:
        pygame.draw.rect(screen, CLEAR_BUTTON_RED, clear_history_rect, border_radius=5)
        clear_text_surf = font_clear_btn.render('X', True, WHITE)
        clear_text_rect = clear_text_surf.get_rect(center=clear_history_rect.center)
        screen.blit(clear_text_surf, clear_text_rect)
    for text, data in buttons.items():
        rect = data['rect']; is_hovered = rect.collidepoint(mouse_pos)
        color = BUTTON_HOVER_BLUE if is_hovered else BUTTON_BLUE
        pygame.draw.rect(screen, color, rect, border_radius=8)
        text_surf_btn = font_button.render(text, True, WHITE); text_rect_btn = text_surf_btn.get_rect(center=rect.center)
        screen.blit(text_surf_btn, text_rect_btn)
        key_label = data.get('key_label')
        if key_label:
            label_surf = font_key_label.render(key_label, True, WHITE)
            label_rect = label_surf.get_rect(bottomright=(rect.right - 8, rect.bottom - 5))
            screen.blit(label_surf, label_rect)

# ==============================================================================
# 6. MAIN LOOP & 7. CLEANUP
# ==============================================================================
load_history()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: running = False
        if event.type == pygame.MOUSEWHEEL:
            if history_rect.collidepoint(pygame.mouse.get_pos()):
                line_height = font_history.get_linesize()
                max_lines = (history_rect.height - 20) // line_height
                history_scroll_offset -= event.y
                history_scroll_offset = max(0, history_scroll_offset)
                history_scroll_offset = min(history_scroll_offset, max(0, len(history) - max_lines))
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if clear_history_rect.collidepoint(event.pos) and history:
                    clear_history()
                else:
                    for text, data in buttons.items():
                        if data['rect'].collidepoint(event.pos): process_input(text); break
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE: running = False
            elif event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER: process_input('=')
            elif event.key == pygame.K_BACKSPACE: process_input('backspace')
            elif event.key == pygame.K_DELETE or event.key == pygame.K_c: process_input('C')
            elif event.unicode in "0123456789.+-*/%": process_input(event.unicode)
    draw_ui()
    pygame.display.flip()

pygame.quit()
sys.exit()