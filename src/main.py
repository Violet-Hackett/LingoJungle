import pygame
import sys
import state
import event_handler
import ui

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

def test_function():
    print("Test button pressed")
test_button = ui.Button(test_function, pygame.Rect(10, 10, 50, 9), "Test")
ui.add_ui_element(test_button)

# Main app loop
def main():
    
    while state.RUNNING:

        event_handler.apply_event_triggers()

        frame_surface = pygame.Surface(state.ROOT_SIZE)

        ui.render_ui_elements_to(frame_surface)

        window.blit(pygame.transform.scale_by(frame_surface, state.SCALE))

        pygame.display.update()
        fpsClock.tick(state.FPS)
 
main()