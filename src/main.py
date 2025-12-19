import pygame
from sys import exit
from maze import draw_smooth_map

pygame.init()


clock = pygame.time.Clock()
pygame.init()
while True:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    
    # Drawing
    # The smooth map function handles the background clear
    draw_smooth_map()
    
    # Update the display
    pygame.display.update()
    
    # Limit frame rate
    clock.tick(60)
