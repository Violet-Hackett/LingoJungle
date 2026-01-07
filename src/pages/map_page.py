from page import Page
import pygame
import ui
from event_handler import EventTrigger, add_event_trigger_explicit, get_relative_mouse_position
import state

class MapPage(Page):
    def __init__(self):
        super().__init__()

    def _construct(self):
        map = ScrollableTexture("jungle_roof", (0, 0), scroll_y=False)
        map_buffer = ui.LayerBuffer([map])
        self._layer_buffers = [map_buffer]
    
SCROLL_VELOCITY_MULTIPLIER = 0.66
class ScrollableTexture(ui.UIElement):
    def __init__(self, texture_name: str, initial_position: tuple[int, int], 
                 scroll_x: bool = True, scroll_y: bool = True):
        super().__init__()

        self.texture_name = texture_name
        self._scroll_x = scroll_x
        self._scroll_y = scroll_y

        texture_size = ui.load_texture(texture_name).size
        self._rect = pygame.Rect(*initial_position, *texture_size)

        self._initial_mouse_click_position: tuple[float, float] = (0.0, 0.0)
        self._initial_click_position: tuple[int, int] = initial_position

        self._init_event_triggers()

    def _init_event_triggers(self):

        # Initial click trigger
        self._event_triggers.append(EventTrigger(self._clicked, event_type=pygame.MOUSEBUTTONDOWN, 
                                                 hitbox=self._rect))
        # Drag trigger
        self._event_triggers.append(EventTrigger(self._scroll, event_type=pygame.MOUSEMOTION, 
                                                 hitbox=self._rect))
        
        for event_trigger in self._event_triggers:
            add_event_trigger_explicit(event_trigger)

    def _check_in_bounds(self, rect: pygame.Rect) -> bool:
        if max(*rect.topleft) > 0:
            return False
        if rect.right < state.root_width():
            return False
        if rect.bottom < state.root_height():
            return False
        return True

    def _clicked(self):
        self._initial_mouse_click_position = get_relative_mouse_position()
        self._initial_click_position = self._rect.topleft

    def _scroll(self):
        if any(pygame.mouse.get_pressed()):
            initial_mouse_x, initial_mouse_y = self._initial_mouse_click_position
            initial_x, initial_y = self._initial_click_position
            mouse_x, mouse_y = get_relative_mouse_position()
            new_x, new_y = (initial_x + (mouse_x - initial_mouse_x)*SCROLL_VELOCITY_MULTIPLIER,
                            initial_y + (mouse_y - initial_mouse_y)*SCROLL_VELOCITY_MULTIPLIER)
            if self._scroll_x and self._check_in_bounds(pygame.Rect(new_x, initial_y, *self._rect.size)):
                self._rect.left = new_x
            if self._scroll_y and self._check_in_bounds(pygame.Rect(initial_x, new_y, *self._rect.size)):
                self._rect.top = new_y
            self.flag_for_buffer_update()

    def _render_to(self, root: pygame.Surface, position: tuple[int, int] = (0, 0)):
        root.blit(ui.load_texture(self.texture_name), self._rect)