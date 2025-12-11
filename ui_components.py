"""
UI components for the Pygame Calculator.
Provides reusable, animated UI elements.
"""
import pygame
from dataclasses import dataclass
from typing import Optional, Tuple, Callable

from config import Colors, Dimensions, FontSizes, Color


def lerp_color(c1: Color, c2: Color, t: float) -> Color:
    """Linear interpolation between two colors."""
    t = max(0.0, min(1.0, t))
    return (
        int(c1[0] + (c2[0] - c1[0]) * t),
        int(c1[1] + (c2[1] - c1[1]) * t),
        int(c1[2] + (c2[2] - c1[2]) * t),
    )


def ease_out_cubic(t: float) -> float:
    """Cubic easing out function for smooth animations."""
    return 1 - pow(1 - t, 3)


@dataclass
class Button:
    """
    An animated calculator button with hover and press states.
    """
    rect: pygame.Rect
    text: str
    key_hint: str
    button_type: str  # "number", "operator", "equals", "clear", "function"
    
    # Animation state
    hover_progress: float = 0.0
    press_progress: float = 0.0
    is_pressed: bool = False
    
    # Animation speed
    HOVER_SPEED: float = 8.0
    PRESS_SPEED: float = 12.0
    
    def get_colors(self, colors: Colors) -> Tuple[Color, Color]:
        """Get the base and hover colors based on button type."""
        color_map = {
            "number": (colors.button_number, colors.button_number_hover),
            "operator": (colors.button_operator, colors.button_operator_hover),
            "equals": (colors.button_equals, colors.button_equals_hover),
            "clear": (colors.button_clear, colors.button_clear_hover),
            "function": (colors.button_number, colors.button_number_hover),
        }
        return color_map.get(self.button_type, (colors.button_number, colors.button_number_hover))
    
    def update(self, dt: float, mouse_pos: Tuple[int, int]) -> None:
        """Update animation states based on mouse position."""
        is_hovered = self.rect.collidepoint(mouse_pos)
        
        # Smooth hover transition
        target_hover = 1.0 if is_hovered else 0.0
        self.hover_progress += (target_hover - self.hover_progress) * self.HOVER_SPEED * dt
        
        # Smooth press transition
        target_press = 1.0 if self.is_pressed else 0.0
        self.press_progress += (target_press - self.press_progress) * self.PRESS_SPEED * dt
    
    def draw(self, screen: pygame.Surface, colors: Colors, 
             font_button: pygame.font.Font, font_hint: pygame.font.Font) -> None:
        """Render the button with current animation state."""
        base_color, hover_color = self.get_colors(colors)
        
        # Interpolate color based on hover
        current_color = lerp_color(base_color, hover_color, ease_out_cubic(self.hover_progress))
        
        # Apply press effect (slight darkening)
        if self.press_progress > 0:
            dark_color = tuple(max(0, c - 30) for c in current_color)
            current_color = lerp_color(current_color, dark_color, self.press_progress)
        
        # Scale effect on press
        scale = 1.0 - self.press_progress * 0.03
        scaled_rect = self.rect.inflate(
            -int(self.rect.width * (1 - scale)),
            -int(self.rect.height * (1 - scale))
        )
        
        # Draw button background
        pygame.draw.rect(screen, current_color, scaled_rect, border_radius=Dimensions.border_radius)
        
        # Draw subtle border
        border_color = lerp_color(current_color, colors.text_secondary, 0.2)
        pygame.draw.rect(screen, border_color, scaled_rect, width=1, border_radius=Dimensions.border_radius)
        
        # Draw main text
        text_surf = font_button.render(self.text, True, colors.text_primary)
        text_rect = text_surf.get_rect(center=scaled_rect.center)
        screen.blit(text_surf, text_rect)
        
        # Draw keyboard hint
        if self.key_hint:
            hint_surf = font_hint.render(self.key_hint, True, colors.text_muted)
            hint_rect = hint_surf.get_rect(bottomright=(scaled_rect.right - 8, scaled_rect.bottom - 5))
            screen.blit(hint_surf, hint_rect)
    
    def handle_click(self, pos: Tuple[int, int]) -> bool:
        """Check if position is within button and trigger press animation."""
        if self.rect.collidepoint(pos):
            self.is_pressed = True
            return True
        return False
    
    def release(self) -> None:
        """Release the button press."""
        self.is_pressed = False


class Display:
    """
    The main calculator display with dynamic font scaling.
    """
    
    def __init__(self, rect: pygame.Rect, font: pygame.font.Font, colors: Colors):
        self.rect = rect
        self.base_font = font
        self.colors = colors
        self.font_size = FontSizes.display
    
    def draw(self, screen: pygame.Surface, text: str, is_error: bool = False) -> None:
        """Draw the display with the given text."""
        # Background with subtle gradient effect (simulated with border)
        pygame.draw.rect(screen, self.colors.display_bg, self.rect, 
                        border_radius=Dimensions.border_radius)
        
        # Subtle inner glow/border
        inner_rect = self.rect.inflate(-2, -2)
        border_color = lerp_color(self.colors.display_bg, self.colors.accent, 0.15)
        pygame.draw.rect(screen, border_color, inner_rect, width=1, 
                        border_radius=Dimensions.border_radius - 1)
        
        # Text color
        text_color = self.colors.error if is_error else self.colors.text_primary
        
        # Dynamic font scaling
        font = self.base_font
        text_surf = font.render(text, True, text_color)
        available_width = self.rect.width - 30
        
        if text_surf.get_width() > available_width:
            scale_factor = available_width / text_surf.get_width()
            new_size = max(24, int(self.font_size * scale_factor))
            font = pygame.font.Font(None, new_size)
            text_surf = font.render(text, True, text_color)
        
        # Right-align the text
        text_rect = text_surf.get_rect(midright=(self.rect.right - 15, self.rect.centery))
        screen.blit(text_surf, text_rect)


class HistoryPanel:
    """
    Scrollable history panel showing past calculations.
    """
    
    def __init__(self, rect: pygame.Rect, font: pygame.font.Font, colors: Colors):
        self.rect = rect
        self.font = font
        self.colors = colors
        self.scroll_offset: int = 0
        self.scroll_velocity: float = 0.0
        self.SCROLL_FRICTION: float = 0.85
    
    def get_max_scroll(self, history_length: int) -> int:
        """Calculate maximum scroll offset."""
        line_height = self.font.get_linesize()
        visible_lines = (self.rect.height - 20) // line_height
        return max(0, history_length - visible_lines)
    
    def scroll(self, delta: int, history_length: int) -> None:
        """Apply scroll with momentum."""
        self.scroll_velocity = delta * 3
    
    def update(self, dt: float, history_length: int) -> None:
        """Update scroll momentum."""
        if abs(self.scroll_velocity) > 0.1:
            self.scroll_offset -= int(self.scroll_velocity)
            self.scroll_velocity *= self.SCROLL_FRICTION
            
            # Clamp scroll
            max_scroll = self.get_max_scroll(history_length)
            self.scroll_offset = max(0, min(self.scroll_offset, max_scroll))
        else:
            self.scroll_velocity = 0
    
    def draw(self, screen: pygame.Surface, history: list, 
             clear_button_callback: Optional[Callable] = None) -> pygame.Rect:
        """Draw the history panel. Returns the clear button rect."""
        # Background
        pygame.draw.rect(screen, self.colors.history_bg, self.rect, 
                        border_radius=Dimensions.border_radius)
        
        # Border
        border_color = lerp_color(self.colors.history_bg, self.colors.text_muted, 0.2)
        pygame.draw.rect(screen, border_color, self.rect, width=1, 
                        border_radius=Dimensions.border_radius)
        
        # Clip area for history text
        clip_area = self.rect.inflate(-20, -20)
        screen.set_clip(clip_area)
        
        line_height = self.font.get_linesize()
        max_lines = clip_area.height // line_height
        
        # Draw history entries (reversed, most recent first)
        reversed_history = list(reversed(history))
        visible_slice = reversed_history[self.scroll_offset:self.scroll_offset + max_lines]
        
        y_offset = clip_area.top
        for entry in visible_slice:
            text_surf = self.font.render(entry, True, self.colors.text_secondary)
            screen.blit(text_surf, (clip_area.left, y_offset))
            y_offset += line_height
        
        screen.set_clip(None)
        
        # Draw scrollbar if needed
        if len(history) > max_lines:
            self._draw_scrollbar(screen, len(history), max_lines)
        
        # Clear history button
        clear_btn_rect = pygame.Rect(self.rect.right - 35, self.rect.top + 8, 22, 22)
        if history:
            pygame.draw.rect(screen, self.colors.button_clear, clear_btn_rect, 
                           border_radius=6)
            font_clear = pygame.font.Font(None, FontSizes.clear_btn)
            x_surf = font_clear.render("×", True, self.colors.text_primary)
            x_rect = x_surf.get_rect(center=clear_btn_rect.center)
            screen.blit(x_surf, x_rect)
        
        return clear_btn_rect
    
    def _draw_scrollbar(self, screen: pygame.Surface, total: int, visible: int) -> None:
        """Draw the scrollbar track and thumb."""
        track_rect = pygame.Rect(
            self.rect.right - 10,
            self.rect.top + 5,
            5,
            self.rect.height - 10
        )
        pygame.draw.rect(screen, self.colors.scrollbar_track, track_rect, border_radius=2)
        
        # Thumb
        thumb_height = max(20, track_rect.height * (visible / total))
        max_scroll = self.get_max_scroll(total)
        scroll_ratio = self.scroll_offset / max_scroll if max_scroll > 0 else 0
        thumb_y = track_rect.top + (track_rect.height - thumb_height) * scroll_ratio
        
        thumb_rect = pygame.Rect(track_rect.left, thumb_y, 5, thumb_height)
        pygame.draw.rect(screen, self.colors.scrollbar_thumb, thumb_rect, border_radius=2)
