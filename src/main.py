import pygame
import sys
import state
import event_handler
from page import Page
from pages.map_page import MapPage
from audio_handler import get_num_occupied_channels, NUM_CHANNELS

# Window setup
pygame.init()
fpsClock = pygame.time.Clock()
window = pygame.display.set_mode(state.window_size())
pygame.display.set_caption('LingoJungle')

# Sets the app state to not running and terminates the pygame window & program
def quit():
    state.RUNNING = False
    pygame.quit()
    sys.exit()
event_handler.add_event_trigger(quit, event_type = pygame.QUIT)
event_handler.add_event_trigger(quit, event_key = pygame.K_ESCAPE)

def print_debug_info():
    print(f"Tick {state.tick_count}: ", end="")
    print(f"{round(fpsClock.get_fps())}/{state.FPS} fps, ", end="")
    print(f"{get_num_occupied_channels()}/{NUM_CHANNELS} audio channels busy")

state.CURRENT_PAGE = MapPage()

# Main app loop
def main():
    
    while state.RUNNING:

        event_handler.apply_event_triggers()

        frame_surface = pygame.Surface(state.ROOT_SIZE)

        state.CURRENT_PAGE.render_to(frame_surface)

        window.blit(pygame.transform.scale_by(frame_surface, state.SCALE))

        pygame.display.update()
        fpsClock.tick(state.FPS)
        state.tick_count += 1

        if state.DEBUG and state.tick_count % state.DEBUG_PRINT_INFO_FREQUENCY == 0:
            print_debug_info()
 
main()