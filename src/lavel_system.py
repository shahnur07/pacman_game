import pygame
import os
from maze import TILE_SIZE, screen

class LevelSystem:
    def __init__(self, initial_lives: int = 3):
        self.lives = initial_lives
        self.life_icon = None
        # Load life icon (Pacman head)
        try:
            sprite_path = os.path.normpath(
                os.path.join(os.path.dirname(__file__), "..", "assets", "sprites", "pacman.png")
            )
            img = pygame.image.load(sprite_path).convert_alpha()
            size = max(16, TILE_SIZE - 6)
            self.life_icon = pygame.transform.smoothscale(img, (size, size))
        except Exception as e:
            print("Failed to load life icon:", e)

    def draw_lives(self):
        if self.life_icon is None or self.lives <= 0:
            return
        spacing = self.life_icon.get_width() + 6
        screen_w = screen.get_width()
        for i in range(self.lives):
            rect = self.life_icon.get_rect()
            # Place icons anchored from the top-right, extending leftwards
            rect.topright = (screen_w - i * spacing, 0)
            screen.blit(self.life_icon, rect)

    def check_collision_and_reset(self, pacman, ghost):
        # Simple circular collision check
        dx = pacman.px - ghost.px
        dy = pacman.py - ghost.py
        dist_sq = dx * dx + dy * dy
        # Threshold based on radii
        pr = getattr(pacman, 'radius', TILE_SIZE // 2)
        gr = getattr(ghost, 'radius', TILE_SIZE // 2)
        threshold = (pr + gr) * 0.8
        if dist_sq <= threshold * threshold:
            if self.lives > 0:
                self.lives -= 1
            pacman.reset_position()
            # Ghost must support reset_to_spawn()
            if hasattr(ghost, 'reset_to_spawn'):
                ghost.reset_to_spawn()

    def get_lives(self) -> int:
        return self.lives
