from page import Page
import pygame
import ui
from lesson import Lesson

class LessonPage(Page):
    def __init__(self, lesson: Lesson):
        self.lesson = lesson
        super().__init__()

    def _construct(self):
        rock_background = ui.StaticTexture("rock_background", (0, 0))

        test_button_default = ui.Button(test_function, pygame.Rect(10, 10, 50, 17), self.lesson.title)
        
        background_buffer = ui.LayerBuffer([rock_background])
        ui_buffer = ui.LayerBuffer([test_button_default])
        self._layer_buffers = [background_buffer, ui_buffer]

def test_function():
    print("Test")