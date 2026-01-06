import pygame
import state
import event_handler

# Window setup
pygame.init()
fpsClock = pygame.time.Clock()
root = pygame.display.set_mode(state.WINDOW_SIZE)
pygame.display.set_caption('LingoJungle')

# Sets the app state to not running and terminates the pygame window
def quit():
    pygame.quit()
    state.RUNNING = False
event_handler.add_event_trigger(quit, event_type = pygame.QUIT)
event_handler.add_event_trigger(quit, event_key = pygame.K_ESCAPE)

# Main app loop
def main():
    
    while state.RUNNING:

        root.fill((0, 0, 0))
        pygame.display.update()
        fpsClock.tick(state.FPS)

        event_handler.apply_event_triggers()
 
main()