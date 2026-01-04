import pygame
from sys import exit
from maze import draw_smooth_map
from pacman import Pacman
from ghost import Ghost
from lavel_system import LevelSystem

# Config variables
GHOST_SPEED = 2
INITIAL_LIVES = 3

# Initialize pygame
pygame.init()
clock = pygame.time.Clock()

# Create Pacman
pacman = Pacman()

# Create Red Ghost (chasing)
red_ghost = Ghost(color=(255, 0, 0), pacman=pacman, speed=GHOST_SPEED)

# Level/Lives system
level = LevelSystem(initial_lives=INITIAL_LIVES)

# Main game loop
while True:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        
        # Handle Pacman input
        pacman.handle_input(event)
    
    # Update entities
    pacman.update()
    red_ghost.update()
    level.check_collision_and_reset(pacman, red_ghost)
    
    # Draw everything
    draw_smooth_map()
    pacman.draw()
    red_ghost.draw()
    level.draw_lives()
    
    # Update display
    pygame.display.flip()
    
    # Limit frame rate to 60 FPS
    clock.tick(60)
