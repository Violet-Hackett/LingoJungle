from event_handler import get_relative_mouse_position, add_event_trigger
import pygame
from typing import Callable
import state

pygame.font.init()
DEFAULT_FONT = pygame.font.Font(f"{state.FONTS_FP}\\Tiny5\\Tiny5-Regular.ttf", 8)

# Abstract class
class UIElement:

    # Abstract method
    def render_to(self, root: pygame.Surface):
        raise NotImplementedError()

BUTTON_COLOR = pygame.Color(255, 0, 0)
BUTTON_HOVERED_COLOR = pygame.Color(0, 0, 255)
BUTTON_PRESSED_COLOR = pygame.Color(0, 255, 0)
BUTTON_TEXT_COLOR = pygame.Color(255, 255, 255)
class Button(UIElement):
    def __init__(self, function: Callable, hitbox: pygame.Rect, text: str|None = None, icon_id: str|None = None, 
                 button_texture_visible: bool = True, hold: bool = False):
        self._function = function
        self._hitbox = hitbox
        self._text = text
        self._icon_id = icon_id
        self._button_texture_visible = button_texture_visible
        self._hold = hold
        self._color: pygame.Color = BUTTON_COLOR

        self._init_event_triggers()

    def _init_event_triggers(self):
        # Hover trigger
        add_event_trigger(self._hovered, self._unhovered, hitbox=self._hitbox)
        # Pressed trigger
        add_event_trigger(self._pressed, event_type=pygame.MOUSEBUTTONDOWN, hitbox=self._hitbox)
        # Activate function trigger
        function_call_event_type = pygame.MOUSEBUTTONDOWN if self._hold else pygame.MOUSEBUTTONUP
        add_event_trigger(self._function, event_type=function_call_event_type, hitbox=self._hitbox)

    def _unhovered(self):
        self._color = BUTTON_COLOR
    def _hovered(self):
        self._color = BUTTON_HOVERED_COLOR
    def _pressed(self):
        self._color = BUTTON_PRESSED_COLOR

    def _render_button_texture_to(self, root: pygame.Surface):
        if self._button_texture_visible:
            pygame.draw.rect(root, self._color, self._hitbox)

    def _render_text_to(self, root: pygame.Surface):
        if self._text:
            rendered_text = DEFAULT_FONT.render(self._text, False, BUTTON_TEXT_COLOR)
            text_pos = (self._hitbox.left + self._hitbox.width/2 - rendered_text.width/2,
                        self._hitbox.top + self._hitbox.height/2 - rendered_text.height/2)
            root.blit(rendered_text, text_pos)
    
    def _render_icon_to(self, root: pygame.Surface):
        if self._icon_id:
            raise NotImplementedError()
    
    def render_to(self, root: pygame.Surface):
        self._render_button_texture_to(root)
        self._render_text_to(root)
        self._render_icon_to(root)

_ui_elements: list[UIElement] = []

def clear_ui_elements():
    global _ui_elements
    _ui_elements.clear()

def add_ui_element(ui_element: UIElement):
    global _ui_elements
    _ui_elements.append(ui_element)

def render_ui_elements_to(root: pygame.Surface):
    global _ui_elements
    for ui_element in _ui_elements:
        ui_element.render_to(root)