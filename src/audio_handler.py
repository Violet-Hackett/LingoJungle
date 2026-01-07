import pygame
import state

pygame.init()

NUM_CHANNELS = 8
CHANNELS = [pygame.mixer.Channel(i) for i in range(NUM_CHANNELS)]

class AudioBuffer:
    def __init__(self, audio_file_name: str):
        self._audio_file_name = audio_file_name
        self.sound = pygame.mixer.Sound(f"{state.AUDIO_FP}\\{audio_file_name}.wav")
        self._current_channel: pygame.mixer.Channel|None = None
    
    def play(self, volume: float = 1, loops: int = 0, fade_ms: int = 0):
        for channel in CHANNELS:
            if not channel.get_busy():
                self.sound.set_volume(volume)
                channel.play(self.sound, loops, fade_ms=fade_ms)
                self._current_channel = channel
                return
        print(f"WARNING: All {NUM_CHANNELS} audio channels occupied: cannot play {self._audio_file_name}.")

    def stop(self, fadeout_ms: int = 0):
        if self._current_channel:
            self._current_channel.fadeout(fadeout_ms)

def get_num_occupied_channels() -> int:
    return len(list(filter(pygame.mixer.Channel.get_busy, CHANNELS)))
