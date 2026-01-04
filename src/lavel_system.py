import pygame
import os
from maze import TILE_SIZE, screen

class LevelSystem:
	def __init__(self, initial_lives: int = 3):
		self.lives = initial_lives
		self.life_icon = None
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
			rect.topright = (screen_w - i * spacing, 0)
			screen.blit(self.life_icon, rect)

	def check_collision_and_reset(self, pacman, ghost):
		dx = pacman.px - ghost.px
		dy = pacman.py - ghost.py
		dist_sq = dx * dx + dy * dy
		pr = getattr(pacman, 'radius', TILE_SIZE // 2)
		gr = getattr(ghost, 'radius', TILE_SIZE // 2)
		threshold = (pr + gr) * 0.8
		if dist_sq <= threshold * threshold:
			# First: if ghost is already returning to base, ignore collisions
			if getattr(ghost, 'returning_to_base', False):
				return
			# Next: if ghost is in scatter, take it down once and start return
			if getattr(ghost, 'scatter_active', False):
				if hasattr(ghost, 'take_down_and_return_to_base'):
					ghost.take_down_and_return_to_base()
				return
			# Normal collision: lose life and reset
			if self.lives > 0:
				self.lives -= 1
			pacman.reset_position()
			if hasattr(ghost, 'reset_to_spawn'):
				ghost.reset_to_spawn()

	def get_lives(self) -> int:
		return self.lives
