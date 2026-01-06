from event_handler import add_event_trigger_explicit, remove_event_trigger, EventTrigger
import pygame
from typing import Callable
import state
from enum import Enum
from audio_handler import AudioBuffer

pygame.font.init()
DEFAULT_FONT = pygame.font.Font(f"{state.FONTS_FP}\\Tiny5\\Tiny5-Regular.ttf", 8)

# Abstract class, a renderable object with a built-in buffer (just implement _render_to() method)
class Renderable:
    def __init__(self, always_flag_buffer_update = False):
        self._buffer = pygame.Surface(state.ROOT_SIZE, pygame.SRCALPHA)
        self._flagged_for_buffer_update: bool = True
        self._always_flag_buffer_update = always_flag_buffer_update

    def flag_for_buffer_update(self):
        self._flagged_for_buffer_update = True

    # Renders to a surface from the renderable's buffer, updating it if flagged
    def render_to(self, root: pygame.Surface):
        if self._flagged_for_buffer_update:
            self._buffer = pygame.Surface(root.size, pygame.SRCALPHA)
            self._render_to(self._buffer)
            if not self._always_flag_buffer_update:
                self._flagged_for_buffer_update = False
        root.blit(self._buffer)

    # Abstract method, internal rendering to a surface implementation ignoring the buffer
    def _render_to(self, root: pygame.Surface, position: tuple[int, int] = (0, 0)):
        raise NotImplementedError("Abstract _render_to() method must be implemented in child classes.")
    
class StaticTexture(Renderable):
    def __init__(self, texture_name, position: tuple[int, int]):
        super().__init__()
        self.texture_name = texture_name
        self.position = position

    def set_position(self, position: tuple[int, int]):
        self.position = position
        self.flag_for_buffer_update()

    def change_position(self, dx: int, dy: int):
        self.position = (self.position[0] + dx, self.position[1] + dy)
        self.flag_for_buffer_update()

    def _render_to(self, root: pygame.Surface):
        root.blit(load_texture(self.texture_name), self.position)

class LayerBuffer(Renderable):
    def __init__(self, renderables: list[Renderable]):
        super().__init__()
        self._renderables = renderables

    def update_buffer_update_flag(self):
        for renderable in self._renderables:
            if renderable._flagged_for_buffer_update:
                self.flag_for_buffer_update()

    def destruct(self):
        for renderable in self._renderables:
            if issubclass(type(renderable), UIElement):
                renderable.clear_event_triggers() # type: ignore

    def _render_to(self, root: pygame.Surface):
        for renderable in self._renderables:
            renderable.render_to(root)

# Abstract class
class UIElement(Renderable):
    def __init__(self):
        super().__init__()
        self._event_triggers: list[EventTrigger] = []
        add_ui_element(self)

    def clear_event_triggers(self):
        for event_trigger in self._event_triggers:
            remove_event_trigger(event_trigger)

class ButtonState(Enum):
    UNTOUCHED = 0
    HOVERED = 1
    PRESSED = 2

DEFAULT_BUTTON_COLOR = pygame.Color(232, 229, 223)
DEFAULT_TEXT_COLOR = pygame.Color(74, 73, 71)
BUTTON_TEXTURE_MIN_WIDTH = 7
BUTTON_TEXTURE_HEIGHT = 17
BUTTON_PRESSED_Y_OFFSET = 2
BUTTON_PRESS_SFX = AudioBuffer('button_press')
BUTTON_RELEASE_SFX = AudioBuffer('button_release')
class Button(UIElement):
    def __init__(self, function: Callable, hitbox: pygame.Rect, text: str|None = None, 
                 icon_id: str|None = None, button_color: pygame.Color = DEFAULT_BUTTON_COLOR,
                 text_color: pygame.Color = DEFAULT_TEXT_COLOR, 
                 show_button_texture: bool = True, hold: bool = False, 
                 press_sfx: AudioBuffer = BUTTON_PRESS_SFX, 
                 release_sfx: AudioBuffer = BUTTON_RELEASE_SFX):
        super().__init__()
        self._function = function
        self._hitbox = hitbox
        self._text = text
        self._icon_id = icon_id
        self._button_color = button_color
        self._text_color = text_color
        self._show_button_texture = show_button_texture
        self._hold = hold
        self.button_state: ButtonState = ButtonState.UNTOUCHED
        self._press_sfx = press_sfx
        self._release_sfx = release_sfx

        self._check_texture_constraints()
        self._init_event_triggers()

    def _init_event_triggers(self):

        # Hover trigger
        self._event_triggers.append(EventTrigger(self._hovered, self._untouched, hitbox=self._hitbox))
        # Pressed trigger
        self._event_triggers.append(EventTrigger(self._pressed, event_type=pygame.MOUSEBUTTONDOWN, hitbox=self._hitbox))
        # Activate function trigger
        function_call_event_type = pygame.MOUSEBUTTONDOWN if self._hold else pygame.MOUSEBUTTONUP
        self._event_triggers.append(EventTrigger(self._function, event_type=function_call_event_type, hitbox=self._hitbox))
        
        for event_trigger in self._event_triggers:
            add_event_trigger_explicit(event_trigger)

    def _set_button_state(self, button_state: ButtonState):
        old_button_state = self.button_state
        if old_button_state != button_state:
            self.button_state = button_state
            self.flag_for_buffer_update()

            # Play the appropriate sfx
            if button_state == ButtonState.PRESSED:
                self._press_sfx.play()
            elif old_button_state == ButtonState.PRESSED:
                self._release_sfx.play()

    def _untouched(self):
        self._set_button_state(ButtonState.UNTOUCHED)
    def _hovered(self):
        self._set_button_state(ButtonState.HOVERED)
    def _pressed(self):
        self._set_button_state(ButtonState.PRESSED)

    def _check_texture_constraints(self):
        if self._show_button_texture:
            if self._hitbox.width < BUTTON_TEXTURE_MIN_WIDTH:
                raise ValueError(f"Button width too small for displaying texture: {self._hitbox.width} < {BUTTON_TEXTURE_MIN_WIDTH}.")
            if self._hitbox.height != BUTTON_TEXTURE_HEIGHT:
                raise ValueError(f"Button height must be {BUTTON_TEXTURE_HEIGHT} to display texture.")
            
    def _get_texture_y_offset(self) -> int:
        return BUTTON_PRESSED_Y_OFFSET if self.button_state == ButtonState.PRESSED else 0

    def _render_button_texture_to(self, root: pygame.Surface):
        if self._show_button_texture:
            button_state_name = self.button_state.name.lower()
            button_subfolder = f"button\\{button_state_name}"

            left = load_texture(f"{button_subfolder}\\button_{button_state_name}_left")
            center = load_texture(f"{button_subfolder}\\button_{button_state_name}_center")
            right = load_texture(f"{button_subfolder}\\button_{button_state_name}_right")

            [texture.fill(self._button_color, special_flags=pygame.BLEND_MULT) 
             for texture in (left, right, center)]

            y = self._hitbox.top + self._get_texture_y_offset()
            left_pos = (self._hitbox.left, y)
            center_pos = (self._hitbox.left + left.width, y)
            right_pos = (self._hitbox.right - right.width, y)
            center_area = pygame.Rect(0, 0, self._hitbox.width - (left.width + right.width), 
                                      center.height)

            root.blit(left, left_pos)
            root.blit(center, center_pos, center_area)
            root.blit(right, right_pos)

    def _render_text_to(self, root: pygame.Surface):
        if self._text:
            rendered_text = DEFAULT_FONT.render(self._text, False, self._text_color)
            text_pos = (self._hitbox.left + self._hitbox.width/2 - rendered_text.width/2,
                        self._hitbox.top + 2 + self._get_texture_y_offset())
            root.blit(rendered_text, text_pos)
    
    def _render_icon_to(self, root: pygame.Surface):
        if self._icon_id:
            raise NotImplementedError()
    
    def _render_to(self, root: pygame.Surface):
        self._render_button_texture_to(root)
        self._render_text_to(root)
        self._render_icon_to(root)

_ui_elements: list[UIElement] = []

def add_ui_element(ui_element: UIElement):
    global _ui_elements
    _ui_elements.append(ui_element)

def render_ui_elements_to(root: pygame.Surface):
    global _ui_elements
    for ui_element in _ui_elements:
        ui_element.render_to(root)

def load_texture(texture_name: str) -> pygame.Surface:
    return pygame.image.load(f"{state.TEXTURES_FP}\\{texture_name}.png").convert_alpha()