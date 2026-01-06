import pygame
from typing import Callable

class EventTrigger:
    def __init__(self, function: Callable, event_key: int|None = None, event_type: int|None = None):
        self.function = function

        self.event_type = event_type
        self.event_key = event_key
        if event_type == None and event_key != None:
            self.event_type = pygame.KEYDOWN
        elif event_key == None and event_type == None:
            raise Exception("Error initializing EventTrigger: event_key and event_type cannot both be None.")
        
    def call(self):
        self.function.__call__()

    def apply(self, event: pygame.Event):
        if self.event_type == event.type:
            if self.event_key == None:
                self.call()
            elif self.event_key == event.key:
                self.call()

event_triggers: list[EventTrigger] = []

def add_event_trigger(function: Callable, event_key: int|None = None, event_type: int|None = None):
    global event_triggers
    event_triggers.append(EventTrigger(function, event_key, event_type))

def apply_event_triggers():
    global event_triggers
    for event in pygame.event.get():
        for event_trigger in event_triggers:
            event_trigger.apply(event)