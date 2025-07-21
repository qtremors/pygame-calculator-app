# pygame_calculator

 
import pygame
import sys
import os

# ==============================================================================
# 1. SETUP AND INITIALIZATION
# ==============================================================================

# Initialize all imported Pygame modules
pygame.init()

# --- Screen Configuration ---
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 650
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pygame Calculator")

# --- Color Palette ---
# Defines the color constants used throughout the application for a consistent theme.
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIGHT_GRAY = (235, 235, 235)       # For the history panel background
DARK_GRAY = (50, 50, 50)           # For the main display background
GRAY_SCROLLBAR = (200, 200, 200)   # For the scrollbar track
BUTTON_BLUE = (30, 144, 255)       # Default button color
BUTTON_HOVER_BLUE = (100, 180, 255)# Button color on mouse hover
ERROR_RED = (220, 20, 60)          # For displaying error messages
CLEAR_BUTTON_RED = (255, 80, 80)   # For the 'Clear History' button

# --- Font Configuration ---
# Defines the fonts for different text elements in the UI.
font_display = pygame.font.Font(None, 80)    # For the main calculator display
font_button = pygame.font.Font(None, 48)     # For the text on calculator buttons
font_history = pygame.font.Font(None, 28)    # For the text in the history panel
font_key_label = pygame.font.Font(None, 20)  # For the small key hints on buttons
font_clear_btn = pygame.font.Font(None, 25)  # For the 'X' on the clear history button

# --- Calculator State Variables ---
# These variables track the current state of the calculator.
current_expression = ""           # The string of the current calculation (e.g., "12+5")
history = []                      # A list to store past calculations
HISTORY_FILE = "calculator_history.txt" # File to save and load history
is_result_displayed = False       # Flag to check if the display shows a result
history_scroll_offset = 0         # Tracks the current scroll position of the history panel

# ==============================================================================
# 2. UI LAYOUT AND CONFIGURATION
# ==============================================================================

# --- UI Element Rectangles ---
# These pygame.Rect objects define the position and size of the main UI components.
display_rect = pygame.Rect(20, 20, SCREEN_WIDTH - 40, 100)
history_rect = pygame.Rect(20, 130, SCREEN_WIDTH - 40, 180)
clear_history_rect = pygame.Rect(history_rect.right - 35, history_rect.top + 5, 20, 20)

# --- Dynamic Button Grid Calculation ---
# This block calculates the size of each button based on the screen dimensions
# and the space available, making the layout responsive to size changes.
BUTTON_MARGIN = 10
button_grid_start_y = history_rect.bottom + BUTTON_MARGIN
grid_height = SCREEN_HEIGHT - button_grid_start_y - BUTTON_MARGIN
BUTTON_COLS = 4
BUTTON_ROWS = 5
BUTTON_WIDTH = (SCREEN_WIDTH - (BUTTON_COLS + 1) * BUTTON_MARGIN) / BUTTON_COLS
BUTTON_HEIGHT = (grid_height - (BUTTON_ROWS - 1) * BUTTON_MARGIN) / BUTTON_ROWS

# --- Button Layout Definition ---
# A list of tuples defining each button's properties:
# (Text, (Grid Row, Grid Col), (Column Span, Row Span), Keyboard Hint)
button_layout = [
    ('C',   (0, 0), (1, 1), 'Del/C'), ('+/-', (0, 1), (1, 1), ''),   ('%',   (0, 2), (1, 1), '%'), ('/',   (0, 3), (1, 1), '/'),
    ('7',   (1, 0), (1, 1), '7'),   ('8',   (1, 1), (1, 1), '8'),   ('9',   (1, 2), (1, 1), '9'), ('*',   (1, 3), (1, 1), '*'),
    ('4',   (2, 0), (1, 1), '4'),   ('5',   (2, 1), (1, 1), '5'),   ('6',   (2, 2), (1, 1), '6'), ('-',   (2, 3), (1, 1), '-'),
    ('1',   (3, 0), (1, 1), '1'),   ('2',   (3, 1), (1, 1), '2'),   ('3',   (3, 2), (1, 1), '3'), ('+',   (3, 3), (1, 1), '+'),
    ('0',   (4, 0), (2, 1), '0'),   ('.',   (4, 2), (1, 1), '.'),   ('=',   (4, 3), (1, 1), 'Enter'),
]

# --- Button Object Creation ---
# This loop iterates through the layout definition to create pygame.Rect objects
# and store them in a dictionary for easy access.
buttons = {}
for text, grid_pos, span, key_label in button_layout:
    row, col = grid_pos
    col_span, row_span = span
    
    # Calculate the pixel position and size for each button based on the grid layout.
    x = BUTTON_MARGIN + col * (BUTTON_WIDTH + BUTTON_MARGIN)
    y = button_grid_start_y + row * (BUTTON_HEIGHT + BUTTON_MARGIN)
    width = col_span * BUTTON_WIDTH + (col_span - 1) * BUTTON_MARGIN
    height = row_span * BUTTON_HEIGHT + (row_span - 1) * BUTTON_MARGIN
    
    buttons[text] = {'rect': pygame.Rect(x, y, width, height), 'key_label': key_label}

# ==============================================================================
# 3. HISTORY MANAGEMENT (File I/O)
# ==============================================================================

def save_history():
    """Saves the current history list to the text file."""
    with open(HISTORY_FILE, 'w') as f:
        for entry in history:
            f.write(entry + '\n')

def load_history():
    """Loads history from the text file if it exists."""
    global history
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, 'r') as f:
            history = [line.strip() for line in f if line.strip()]

def clear_history():
    """Clears the history list, resets the scroll, and updates the file."""
    global history, history_scroll_offset
    history.clear()
    history_scroll_offset = 0
    save_history()

# ==============================================================================
# 4. CORE CALCULATOR LOGIC
# ==============================================================================

def process_input(value):
    """Handles all button clicks and key presses to update the calculator state."""
    global current_expression, history, is_result_displayed

    # If a result is on display, pressing a number starts a new calculation.
    # Pressing an operator continues the calculation with the result.
    if is_result_displayed and value not in ['=', '+/-', '%']:
        if value in "0123456789.":
            current_expression = ""
        is_result_displayed = False

    # --- Handle different input types ---
    if value == 'C':
        current_expression = ""
        is_result_displayed = False
    elif value == '=':
        if not current_expression: return
        try:
            # Use eval() for simplicity. In a production app, a safer parser is recommended.
            result = str(eval(current_expression))
            history.append(f"{current_expression} = {result}")
            if len(history) > 100: history.pop(0) # Limit history to 100 entries
            current_expression = result
            save_history()
            is_result_displayed = True
        # Catch specific math/syntax errors and display user-friendly messages.
        except ZeroDivisionError:
            current_expression = "Error: Cannot divide by zero"
            is_result_displayed = True
        except (SyntaxError, NameError):
            current_expression = "Error: Invalid syntax"
            is_result_displayed = True
        except Exception as e:
            current_expression = "Error"
            is_result_displayed = True
            print(f"An unexpected error occurred: {e}") # For debugging
    elif value == '+/-':
        if current_expression.startswith("Error"): return
        if current_expression and current_expression.startswith('-'):
            current_expression = current_expression[1:]
        elif current_expression:
            current_expression = '-' + current_expression
    elif value == '%':
        if not current_expression or current_expression.startswith("Error"): return
        try:
            current_expression = str(float(current_expression) / 100)
            is_result_displayed = True
        except (ValueError, TypeError):
            current_expression = "Error: Invalid input for %"
            is_result_displayed = True
    elif value == 'backspace':
        if is_result_displayed or current_expression.startswith("Error"):
            current_expression = ""
            is_result_displayed = False
        else:
            current_expression = current_expression[:-1]
    # For numbers and operators, append them to the current expression.
    else:
        if current_expression == "0" and value != '.':
            current_expression = ""
        current_expression += value

# ==============================================================================
# 5. DRAWING FUNCTIONS (VIEW)
# ==============================================================================

def draw_ui():
    """Renders the entire calculator interface to the screen each frame."""
    screen.fill(WHITE)
    mouse_pos = pygame.mouse.get_pos()

    # --- Draw Main Display ---
    pygame.draw.rect(screen, DARK_GRAY, display_rect, border_radius=10)
    text_color = ERROR_RED if current_expression.startswith("Error") else WHITE
    display_text = current_expression or "0"
    
    # Dynamic font scaling: If text is too wide, it's rendered with a smaller font.
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

    # --- Draw History Panel ---
    pygame.draw.rect(screen, LIGHT_GRAY, history_rect, border_radius=10)
    
    # Use a clipping area so history text doesn't draw outside its box.
    clip_area = history_rect.inflate(-20, -20)
    screen.set_clip(clip_area)

    y_offset = clip_area.top
    line_height = font_history.get_linesize()
    max_lines = clip_area.height // line_height
    
    # Determine which part of the history is visible based on the scroll offset.
    reversed_history = list(reversed(history))
    visible_slice = reversed_history[history_scroll_offset : history_scroll_offset + max_lines]
    
    for entry in visible_slice:
        history_surf = font_history.render(entry, True, DARK_GRAY)
        screen.blit(history_surf, (clip_area.left, y_offset))
        y_offset += line_height

    screen.set_clip(None) # Reset the clipping area to draw normally again.

    # --- Draw Scrollbar and Clear Button ---
    # These are only drawn if the history is long enough to require them.
    if len(history) > max_lines:
        # Draw the scrollbar track and the movable thumb.
        scrollbar_track_rect = pygame.Rect(history_rect.right - 12, history_rect.top, 7, history_rect.height)
        pygame.draw.rect(screen, GRAY_SCROLLBAR, scrollbar_track_rect, border_radius=3)
        viewable_ratio = max_lines / len(history)
        thumb_height = history_rect.height * viewable_ratio
        scroll_ratio = history_scroll_offset / (len(history) - max_lines)
        thumb_y = history_rect.top + (history_rect.height - thumb_height) * scroll_ratio
        thumb_rect = pygame.Rect(scrollbar_track_rect.left, thumb_y, 7, thumb_height)
        pygame.draw.rect(screen, DARK_GRAY, thumb_rect, border_radius=3)
        
    if history:
        # Draw the 'X' button to clear history.
        pygame.draw.rect(screen, CLEAR_BUTTON_RED, clear_history_rect, border_radius=5)
        clear_text_surf = font_clear_btn.render('X', True, WHITE)
        clear_text_rect = clear_text_surf.get_rect(center=clear_history_rect.center)
        screen.blit(clear_text_surf, clear_text_rect)

    # --- Draw Calculator Buttons ---
    for text, data in buttons.items():
        rect = data['rect']
        is_hovered = rect.collidepoint(mouse_pos)
        color = BUTTON_HOVER_BLUE if is_hovered else BUTTON_BLUE
        pygame.draw.rect(screen, color, rect, border_radius=8)
        
        # Draw the main text on the button.
        text_surf_btn = font_button.render(text, True, WHITE)
        text_rect_btn = text_surf_btn.get_rect(center=rect.center)
        screen.blit(text_surf_btn, text_rect_btn)
        
        # Draw the small keyboard hint in the corner.
        key_label = data.get('key_label')
        if key_label:
            label_surf = font_key_label.render(key_label, True, WHITE)
            label_rect = label_surf.get_rect(bottomright=(rect.right - 8, rect.bottom - 5))
            screen.blit(label_surf, label_rect)

# ==============================================================================
# 6. MAIN APPLICATION LOOP
# ==============================================================================

# Load any saved history when the application starts.
load_history()
running = True
while running:
    # --- Event Handling ---
    # Process all events in the queue (mouse clicks, key presses, etc.).
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        # Handle mouse wheel scrolling for the history panel.
        if event.type == pygame.MOUSEWHEEL:
            if history_rect.collidepoint(pygame.mouse.get_pos()):
                line_height = font_history.get_linesize()
                max_lines = (history_rect.height - 20) // line_height
                history_scroll_offset -= event.y # event.y is 1 for up, -1 for down
                # Clamp the scroll offset to prevent scrolling past the history content.
                history_scroll_offset = max(0, history_scroll_offset)
                history_scroll_offset = min(history_scroll_offset, max(0, len(history) - max_lines))
        
        # Handle mouse button clicks.
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1: # Left mouse button
                if clear_history_rect.collidepoint(event.pos) and history:
                    clear_history()
                else:
                    for text, data in buttons.items():
                        if data['rect'].collidepoint(event.pos):
                            process_input(text)
                            break
                        
        # Handle keyboard presses.
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                process_input('=')
            elif event.key == pygame.K_BACKSPACE:
                process_input('backspace')
            elif event.key == pygame.K_DELETE or event.key == pygame.K_c:
                process_input('C')
            elif event.unicode in "0123456789.+-*/%":
                process_input(event.unicode)
            
    # --- Drawing ---
    # Redraw the entire UI every frame.
    draw_ui()
    
    # --- Update Display ---
    # Update the full display Surface to the screen.
    pygame.display.flip()

# ==============================================================================
# 7. CLEANUP
# ==============================================================================

# Uninitialize Pygame modules and exit the program.
pygame.quit()
sys.exit()
