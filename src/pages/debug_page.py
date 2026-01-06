from page import Page
import pygame
import ui

class DebugPage(Page):
    def __init__(self):
        super().__init__()

    def _construct(self):
        
        rock_background = ui.StaticTexture("rock_background", (0, 0))
        test_button = ui.Button(test_function, pygame.Rect(10, 10, 50, 17), "Test")
        
        background_buffer = ui.LayerBuffer([rock_background])
        ui_buffer = ui.LayerBuffer([test_button])
        self._layer_buffers = [background_buffer, ui_buffer]

def test_function():
    print("Test button pressed")