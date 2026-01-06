from page import Page
import pygame
import ui

RED = pygame.Color(245, 40, 40)
GREEN = pygame.Color(40, 245, 40)
BLUE = pygame.Color(40, 40, 245)
BLACK = pygame.Color(0, 0, 0)
class DebugPage(Page):
    def __init__(self):
        super().__init__()

    def _construct(self):
        
        rock_background = ui.StaticTexture("rock_background", (0, 0))

        test_button_default = ui.Button(test_function, pygame.Rect(10, 10, 50, 17), "Test")
        test_button_red = ui.Button(test_function, pygame.Rect(10, 30, 50, 17), "Test (red)", 
                                    button_color=RED, text_color=BLACK)
        test_button_green = ui.Button(test_function, pygame.Rect(10, 50, 50, 17), "Test (green)", 
                                      button_color=GREEN, text_color=BLACK)
        test_button_blue = ui.Button(test_function, pygame.Rect(10, 70, 50, 17), "Test (blue)", 
                                     button_color=BLUE, text_color=BLACK)
        
        background_buffer = ui.LayerBuffer([rock_background])
        ui_buffer = ui.LayerBuffer([test_button_default, test_button_red, test_button_green, test_button_blue])
        self._layer_buffers = [background_buffer, ui_buffer]

def test_function():
    print("Test button pressed")