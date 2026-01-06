from page import Page
import pygame
import ui

class DebugPage(Page):
    def __init__(self):
        super().__init__()

    def _construct(self):
        
        test_button = ui.Button(test_function, pygame.Rect(10, 10, 50, 17), "Test")
        
        ui_layer_buffer = ui.LayerBuffer([test_button])
        self._layer_buffers = [ui_layer_buffer]

def test_function():
    print("Test button pressed")