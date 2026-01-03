import pygame
from sys import exit
from maze import draw_smooth_map
from pacman import Pacman
from ghost import Ghost

# Initialize pygame
pygame.init()
clock = pygame.time.Clock()

# Create Pacman
pacman = Pacman()

# Create Red Ghost (chasing)
red_ghost = Ghost(color=(255, 0, 0), pacman=pacman, speed=2)

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
    
    # Draw everything
    draw_smooth_map()
    pacman.draw()
    red_ghost.draw()
    
    # Update display
    pygame.display.flip()
    
    # Limit frame rate to 60 FPS
    clock.tick(60)