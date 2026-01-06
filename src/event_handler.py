import pygame
from typing import Callable
import state

class EventTrigger:
    def __init__(self, triggered_function: Callable, untriggered_function: Callable|None = None,
                 event_key: int|None = None, event_type: int|None = None,
                 hitbox: pygame.Rect|None = None):
        self._triggered_function = triggered_function
        self._untriggered_function = untriggered_function

        self._event_type = event_type
        self._event_key = event_key
        self._hitbox = hitbox
        if event_type == None and event_key != None:
            self.event_type = pygame.KEYDOWN
        elif event_key == None and event_type == None and hitbox == None:
            raise Exception("Error initializing EventTrigger: event_key, event_type, and hitbox cannot all be None.")

    def apply(self, event: pygame.Event):

        call = False
        if self._event_type == event.type or self._event_type == None:
            if self._hitbox:
                mouse_pos = get_relative_mouse_position()
                if self._hitbox.collidepoint(mouse_pos):
                    call = True
            elif self._event_key != None and hasattr(event, 'key'):
                if self._event_key == event.key:
                    call = True
            elif self._event_type == event.type:
                call = True

        if call: 
            self._triggered_function.__call__()
        elif self._untriggered_function:
            self._untriggered_function.__call__()

_event_triggers: list[EventTrigger] = []

def clear_event_triggers():
    global _event_triggers
    _event_triggers.clear()

def add_event_trigger(triggered_function: Callable, untriggered_function: Callable|None = None,
                 event_key: int|None = None, event_type: int|None = None,
                 hitbox: pygame.Rect|None = None):
    global _event_triggers
    add_event_trigger_explicit(EventTrigger(triggered_function, untriggered_function, event_key, 
                                        event_type, hitbox))
    
def add_event_trigger_explicit(event_trigger: EventTrigger):
    global _event_triggers
    _event_triggers.append(event_trigger)

def remove_event_trigger(event_trigger: EventTrigger):
    global _event_triggers
    _event_triggers.remove(event_trigger)

def apply_event_triggers():
    global _event_triggers
    for event in pygame.event.get():
        for event_trigger in _event_triggers:
            event_trigger.apply(event)

# Converts window coordinates into root surface position
def relative_position(window_coordinates: tuple[float, float]) -> tuple[float, float]:
    return (window_coordinates[0] / state.SCALE, window_coordinates[1] / state.SCALE)

# Gets the mouse position in relative coordinates on the root surface
def get_relative_mouse_position() -> tuple[float, float]:
    window_mouse_pos = pygame.mouse.get_pos()
    return relative_position(window_mouse_pos)