"""
Pygame Calculator - A modern, keyboard-accessible desktop calculator.

A fully functional calculator application built with Python and Pygame,
featuring a beautiful dark theme, smooth animations, and persistent history.
"""
import pygame
import sys
import os
from typing import Dict, Optional

from config import (
    Colors, Dimensions, FontSizes, 
    APP_NAME, HISTORY_FILE, MAX_HISTORY_ENTRIES, BUTTON_LAYOUT
)
from calculator_engine import CalculatorEngine
from ui_components import Button, Display, HistoryPanel


class CalculatorApp:
    """
    Main application class orchestrating the calculator UI and logic.
    """
    
    def __init__(self) -> None:
        """Initialize Pygame and set up the application."""
        pygame.init()
        
        # Configuration
        self.colors = Colors()
        self.dims = Dimensions()
        
        # Screen setup
        self.screen = pygame.display.set_mode(
            (self.dims.screen_width, self.dims.screen_height)
        )
        pygame.display.set_caption(APP_NAME)
        
        # Try to set window icon
        self._set_icon()
        
        # Fonts
        self.font_display = pygame.font.Font(None, FontSizes.display)
        self.font_button = pygame.font.Font(None, FontSizes.button)
        self.font_history = pygame.font.Font(None, FontSizes.history)
        self.font_hint = pygame.font.Font(None, FontSizes.key_hint)
        
        # Calculator engine
        self.engine = CalculatorEngine()
        
        # UI Components
        self._setup_ui()
        
        # Load history
        self._load_history()
        
        # Clock for delta time
        self.clock = pygame.time.Clock()
        self.running = True
    
    def _set_icon(self) -> None:
        """Set window icon if available."""
        icon_path = os.path.join(os.path.dirname(__file__), "icon.png")
        if os.path.exists(icon_path):
            try:
                icon = pygame.image.load(icon_path)
                pygame.display.set_icon(icon)
            except pygame.error:
                pass
    
    def _setup_ui(self) -> None:
        """Initialize all UI components."""
        margin = self.dims.button_margin
        
        # Display rectangle
        display_rect = pygame.Rect(
            20, 20, 
            self.dims.screen_width - 40, 
            self.dims.display_height
        )
        self.display = Display(display_rect, self.font_display, self.colors)
        
        # History panel rectangle
        history_y = display_rect.bottom + margin
        history_rect = pygame.Rect(
            20, history_y,
            self.dims.screen_width - 40,
            self.dims.history_height
        )
        self.history_panel = HistoryPanel(history_rect, self.font_history, self.colors)
        
        # Calculate button grid
        button_start_y = history_rect.bottom + margin
        grid_height = self.dims.screen_height - button_start_y - margin
        
        button_width = (self.dims.screen_width - (self.dims.button_cols + 1) * margin) / self.dims.button_cols
        button_height = (grid_height - (self.dims.button_rows - 1) * margin) / self.dims.button_rows
        
        # Create buttons
        self.buttons: Dict[str, Button] = {}
        for text, grid_pos, span, key_hint, btn_type in BUTTON_LAYOUT:
            row, col = grid_pos
            col_span, row_span = span
            
            x = margin + col * (button_width + margin)
            y = button_start_y + row * (button_height + margin)
            width = col_span * button_width + (col_span - 1) * margin
            height = row_span * button_height + (row_span - 1) * margin
            
            rect = pygame.Rect(x, y, width, height)
            self.buttons[text] = Button(rect, text, key_hint, btn_type)
        
        # Store clear history button rect (updated each frame)
        self.clear_history_rect: Optional[pygame.Rect] = None
    
    def _load_history(self) -> None:
        """Load calculation history from file."""
        if os.path.exists(HISTORY_FILE):
            try:
                with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
                    entries = [line.strip() for line in f if line.strip()]
                    self.engine.state.history = entries[-MAX_HISTORY_ENTRIES:]
            except (IOError, OSError):
                pass
    
    def _save_history(self) -> None:
        """Save calculation history to file."""
        try:
            with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
                for entry in self.engine.history[-MAX_HISTORY_ENTRIES:]:
                    f.write(entry + '\n')
        except (IOError, OSError):
            pass
    
    def _handle_input(self, value: str) -> None:
        """Process calculator input from button or keyboard."""
        if value == 'C':
            self.engine.clear()
        elif value == '=':
            result = self.engine.calculate()
            if result is not None:
                self._save_history()
        elif value == '+/-':
            self.engine.toggle_sign()
        elif value == '%':
            self.engine.percentage()
        elif value == 'backspace':
            self.engine.backspace()
        elif value in '0123456789.+-*/':
            self.engine.append(value)
    
    def _handle_events(self) -> None:
        """Process all pygame events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            # Mouse wheel for history scrolling
            elif event.type == pygame.MOUSEWHEEL:
                if self.history_panel.rect.collidepoint(pygame.mouse.get_pos()):
                    self.history_panel.scroll(event.y, len(self.engine.history))
            
            # Mouse click
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                # Check clear history button
                if (self.clear_history_rect and 
                    self.clear_history_rect.collidepoint(event.pos) and 
                    self.engine.history):
                    self.engine.clear_history()
                    self.history_panel.scroll_offset = 0
                    self._save_history()
                else:
                    # Check calculator buttons
                    for text, button in self.buttons.items():
                        if button.handle_click(event.pos):
                            self._handle_input(text)
                            break
            
            # Mouse release
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                for button in self.buttons.values():
                    button.release()
            
            # Keyboard input
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                    self._handle_input('=')
                elif event.key == pygame.K_BACKSPACE:
                    self._handle_input('backspace')
                elif event.key in (pygame.K_DELETE, pygame.K_c):
                    self._handle_input('C')
                elif event.unicode in '0123456789.+-*/%':
                    self._handle_input(event.unicode)
    
    def _update(self, dt: float) -> None:
        """Update all animated components."""
        mouse_pos = pygame.mouse.get_pos()
        
        # Update buttons
        for button in self.buttons.values():
            button.update(dt, mouse_pos)
        
        # Update history panel scroll
        self.history_panel.update(dt, len(self.engine.history))
    
    def _draw(self) -> None:
        """Render the entire UI."""
        # Background
        self.screen.fill(self.colors.background)
        
        # Display
        self.display.draw(
            self.screen, 
            self.engine.display_text, 
            self.engine.is_error
        )
        
        # History panel
        self.clear_history_rect = self.history_panel.draw(
            self.screen, 
            self.engine.history
        )
        
        # Buttons
        for button in self.buttons.values():
            button.draw(self.screen, self.colors, self.font_button, self.font_hint)
        
        pygame.display.flip()
    
    def run(self) -> None:
        """Main application loop."""
        while self.running:
            dt = self.clock.tick(60) / 1000.0  # Delta time in seconds
            
            self._handle_events()
            self._update(dt)
            self._draw()
        
        # Cleanup
        pygame.quit()
        sys.exit()


def main() -> None:
    """Entry point for the calculator application."""
    app = CalculatorApp()
    app.run()


if __name__ == "__main__":
    main()
