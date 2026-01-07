import os
import state
import json
import pygame
from user import USER
from audio_handler import AudioBuffer

class Lesson:
    def __init__(self, index: int, title: str, icon_name: str, map_color: pygame.Color, 
                 map_position: tuple[int, int], required_knowledge: int):
        self.index = index
        self.title = title
        self.icon_name = icon_name
        self.map_color = map_color
        self.map_position = map_position
        self.required_knowledge = required_knowledge

    def is_unlocked(self) -> bool:
        return USER.knowledge >= self.required_knowledge

    @staticmethod
    def from_lesson_fp(lesson_fp: str) -> ...:
        with open(f"{state.LESSONS_FP}\\{lesson_fp}") as lesson_file:
            lesson_data = json.load(lesson_file)
        index = lesson_data['index']
        title = lesson_data['title']
        icon_name = lesson_data['icon_name']
        map_color = pygame.Color(lesson_data['map_color'])
        map_position = lesson_data['map_position']
        required_knowledge = lesson_data['required_knowledge']
        return Lesson(index, title, icon_name, map_color, map_position, required_knowledge)

def get_supported_lesson_fps() -> list[str]:
    return [file for file in os.listdir(state.LESSONS_FP) if file.endswith('.lesson')]

LESSONS: list[Lesson] = []
def load_lessons():
    global LESSONS
    LESSONS.clear()
    LESSONS = [Lesson.from_lesson_fp(fp) for fp in get_supported_lesson_fps()]
    LESSONS.sort(key=lambda lesson: lesson.index)
load_lessons()
