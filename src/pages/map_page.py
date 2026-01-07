from page import Page
import pygame
import ui
from event_handler import EventTrigger, add_event_trigger_explicit, get_relative_mouse_position
import state
from audio_handler import AudioBuffer
from lesson import LESSONS
from user import USER

LESSON_UNLOCK_SFX = AudioBuffer("lesson_unlock")
class MapPage(Page):
    def __init__(self):
        self._lesson_buttons: list[ui.Button] = []
        super().__init__()
        self.unlock_new_lessons()

    def _construct(self):
        jungle_ambience = AudioBuffer("jungle_ambience")
        jungle_ambience.play(loops=-1, fade_ms=1000)

        map = ui.StaticTexture("jungle_roof", (-100, 0))
        lesson_buttons: list[ui.Button] = []
        for lesson in LESSONS:
            lesson_button_hitbox = pygame.Rect(*lesson.map_position, 15, 17)
            lesson_disabled = lesson.index not in USER.unlocked_lesson_indices
            lesson_button = ui.Button(test_function, lesson_button_hitbox, 
                                                button_color=lesson.map_color, 
                                                icon_name=lesson.icon_name, 
                                                disabled=lesson_disabled)
            lesson_buttons.append(lesson_button)
        self._lesson_buttons = lesson_buttons

        map_buffer = ui.LayerBuffer([map] + lesson_buttons) # type: ignore

        self._layer_buffers = [map_buffer]

    def unlock_new_lessons(self):
        for lesson in LESSONS:
            if lesson.is_unlocked() and lesson.index not in USER.unlocked_lesson_indices:
                self.unlock_new_lesson(lesson.index)

    def unlock_new_lesson(self, lesson_index: int):
        self._lesson_buttons[lesson_index].enable()
        LESSON_UNLOCK_SFX.play()
        # TODO: Fancy unlock animation
        USER.unlocked_lesson_indices.append(lesson_index)
        USER.save_data()

def test_function():
    print("test")