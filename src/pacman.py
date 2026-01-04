import pygame
import time
import math
from maze import MAP_DATA, TILE_SIZE, MAP_WIDTH, MAP_HEIGHT, screen

# Defer font/text creation until pygame font is initialized
font = None
text_surface = None
text_rect = None

class Pacman:
    def __init__(self):
        # Find Pacman's starting position (tile with value 9 in maze)
        self.start_pos = self.find_start_position()
        self.reset_position()
        
        # Pallet count variable
        self.pallet_count = 0

        # Movement speed (constant 2 as requested)
        self.speed = 2
        
        # Current movement direction
        self.dx = 0  # -1 left, 0 none, 1 right
        self.dy = 0  # -1 up, 0 none, 1 down
        
        # Next queued direction (for responsive controls)
        self.next_dx = 0
        self.next_dy = 0
        
        # Pacman's radius for drawing
        self.radius = TILE_SIZE // 2 - 2
        
        # Mouth animation
        self.mouth_phase = 0
        self.animation_speed = 0.25
        
        # Track if we're in a tunnel for teleportation
        self.in_tunnel = False
        # Power pellet flag (set true for a single frame when eaten)
        self.last_ate_power = False
        
        print(f"Pacman starting at tile: {self.start_pos}")

    def find_start_position(self):
        """Find Pacman's starting position (tile with value 9)"""
        for y in range(MAP_HEIGHT):
            for x in range(MAP_WIDTH):
                if MAP_DATA[y][x] == 9:  # 9 indicates Pacman starting position
                    # Clear the starting marker
                    MAP_DATA[y][x] = 0
                    return x, y
        
        # Fallback if no 9 found
        print("Warning: Pacman start position (9) not found, using default")
        return 9, 1

    def reset_position(self):
        """Reset Pacman to starting position"""
        self.px = self.start_pos[0] * TILE_SIZE + TILE_SIZE // 2
        self.py = self.start_pos[1] * TILE_SIZE + TILE_SIZE // 2
        
        # Reset movement
        self.dx = 0
        self.dy = 0
        self.next_dx = 0
        self.next_dy = 0
        self.in_tunnel = False

    def current_tile(self):
        """Get current tile coordinates"""
        return int(self.px // TILE_SIZE), int(self.py // TILE_SIZE)

    def get_tile_at(self, x, y):
        """Get tile value at coordinates"""
        if 0 <= x < MAP_WIDTH and 0 <= y < MAP_HEIGHT:
            return MAP_DATA[y][x]
        return 1  # Treat out of bounds as wall

    def is_wall(self, x, y):
        """Check if tile is a wall"""
        return self.get_tile_at(x, y) == 1

    def can_move_in_direction(self, dx, dy):
        """Check if Pacman can move in a given direction"""
        if dx == 0 and dy == 0:
            return False
        
        current_x, current_y = self.current_tile()
        next_x = current_x + dx
        next_y = current_y + dy
        
        # Special case: tunnels (row 9)
        if next_y == 9:  # Tunnel row
            if next_x < 0 or next_x >= MAP_WIDTH:
                return True
        
        # Check if next tile is within bounds
        if 0 <= next_x < MAP_WIDTH and 0 <= next_y < MAP_HEIGHT:
            return not self.is_wall(next_x, next_y)
        
        return False

    def handle_input(self, event):
        """Handle keyboard input for movement"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.next_dx, self.next_dy = 0, -1
            elif event.key == pygame.K_DOWN:
                self.next_dx, self.next_dy = 0, 1
            elif event.key == pygame.K_LEFT:
                self.next_dx, self.next_dy = -1, 0
            elif event.key == pygame.K_RIGHT:
                self.next_dx, self.next_dy = 1, 0

    def update(self):
        """Update Pacman's position - SIMPLE AND RELIABLE"""
        # Update mouth animation
        if self.dx != 0 or self.dy != 0:
            self.mouth_phase = (self.mouth_phase + self.animation_speed) % (2 * math.pi)
        
        # Get current position
        current_x, current_y = self.current_tile()
        offset_x = self.px % TILE_SIZE
        offset_y = self.py % TILE_SIZE
        
        # Check if we're exactly at the center of a tile (with tolerance)
        center_x = TILE_SIZE // 2
        center_y = TILE_SIZE // 2
        tolerance = 1
        
        is_at_center = (abs(offset_x - center_x) <= tolerance and 
                       abs(offset_y - center_y) <= tolerance)
        
        # If we're at center of tile
        if is_at_center:
            # Snap to exact center
            self.px = current_x * TILE_SIZE + center_x
            self.py = current_y * TILE_SIZE + center_y
            
            # Eat pellet at current position and count it
            if 0 <= current_x < MAP_WIDTH and 0 <= current_y < MAP_HEIGHT:
                tile_value = MAP_DATA[current_y][current_x]
                if tile_value == 2 or tile_value == 3:
                    MAP_DATA[current_y][current_x] = 0
                    if tile_value == 2:
                        self.pallet_count += 10
                    else:
                        self.pallet_count += 50
                        self.last_ate_power = True
                    # screen.blit()
            
            # Try to change to queued direction if it's valid
            if self.can_move_in_direction(self.next_dx, self.next_dy):
                self.dx, self.dy = self.next_dx, self.next_dy
                # Clear queued direction
                self.next_dx = 0
                self.next_dy = 0
        
        # Handle tunnel teleportation
        self.handle_tunnel()
        
        # Check if we can continue moving in current direction
        if self.can_move_in_direction(self.dx, self.dy):
            self.px += self.dx * self.speed
            self.py += self.dy * self.speed
        else:
            # If we can't move, stop and snap to center
            if is_at_center:
                self.dx = 0
                self.dy = 0
            else:
                # Move to center first, then stop
                if self.dx > 0:
                    if self.px < current_x * TILE_SIZE + center_x:
                        self.px += self.speed
                    else:
                        self.px = current_x * TILE_SIZE + center_x
                        self.dx = 0
                elif self.dx < 0:
                    if self.px > current_x * TILE_SIZE + center_x:
                        self.px -= self.speed
                    else:
                        self.px = current_x * TILE_SIZE + center_x
                        self.dx = 0
                elif self.dy > 0:
                    if self.py < current_y * TILE_SIZE + center_y:
                        self.py += self.speed
                    else:
                        self.py = current_y * TILE_SIZE + center_y
                        self.dy = 0
                elif self.dy < 0:
                    if self.py > current_y * TILE_SIZE + center_y:
                        self.py -= self.speed
                    else:
                        self.py = current_y * TILE_SIZE + center_y
                        self.dy = 0

    def handle_tunnel(self):
        """Handle tunnel teleportation - SIMPLE VERSION"""
        # Check if we're in the tunnel row (row 9)
        current_x, current_y = self.current_tile()
        
        if current_y != 9:
            self.in_tunnel = False
            return
        
        # Get pixel position within tile
        pixel_in_tile = self.px % TILE_SIZE
        
        # Check if at left tunnel entrance and moving left
        if current_x == 0 and self.dx < 0:
            # When we reach the left side of the tile
            if pixel_in_tile < TILE_SIZE // 2:
                # Teleport to right side
                self.px = (MAP_WIDTH - 1) * TILE_SIZE + TILE_SIZE // 2
        
        # Check if at right tunnel entrance and moving right
        elif current_x == MAP_WIDTH - 1 and self.dx > 0:
            # When we reach the right side of the tile
            if pixel_in_tile > TILE_SIZE // 2:
                # Teleport to left side
                self.px = TILE_SIZE+10 // 2

    def draw(self):
        """Draw Pacman and pallet_count text in the top tile"""
        # Lazily initialize font once
        global font
        if font is None:
            try:
                if not pygame.font.get_init():
                    pygame.font.init()
                font = pygame.font.Font("src/fonts/CascadiaCode-VariableFont_wght.ttf", 22)
            except Exception as e:
                print("Font init failed:", e)
        # Calculate mouth opening
        if self.dx == 0 and self.dy == 0:
            # Closed mouth when stationary
            mouth_angle = 0
        else:
            # Animated mouth (0-60 degrees)
            mouth_angle = 30 + 30 * math.sin(self.mouth_phase)

        center_x = int(self.px)
        center_y = int(self.py)

        # Determine direction for mouth
        if self.dx == 1:  # Right
            direction_angle = 0
        elif self.dx == -1:  # Left
            direction_angle = 180
        elif self.dy == -1:  # Up
            direction_angle = 90
        elif self.dy == 1:  # Down
            direction_angle = 270
        else:
            # Stationary - draw full circle
            pygame.draw.circle(screen, (255, 255, 0), (center_x, center_y), self.radius)
            # Render dynamic pallet_count in the top-left tile
            if font:
                title_surface = font.render(str(self.pallet_count), True, (0, 255, 0))
                screen.blit(title_surface, (0, 0))
            return

        # Draw Pacman as a filled arc (pie slice)
        points = []
        num_points = 30

        # Start at center
        points.append((center_x, center_y))

        # Calculate the large arc (the Pacman body, not the mouth)
        start_angle = direction_angle + mouth_angle / 2
        end_angle = direction_angle - mouth_angle / 2 + 360

        # Convert to radians
        start_rad = math.radians(start_angle)
        end_rad = math.radians(end_angle)

        # Generate points along the arc
        for i in range(num_points + 1):
            t = i / num_points
            angle = start_rad + (end_rad - start_rad) * t

            x = center_x + self.radius * math.cos(angle)
            y = center_y - self.radius * math.sin(angle)  # Negative because pygame y increases downward

            points.append((x, y))

        # Draw the filled polygon
        pygame.draw.polygon(screen, (255, 255, 0), points)

        # Render dynamic pallet_count in the top-left tile each frame
        if font:
            title_surface = font.render(str(self.pallet_count), True, (0, 255, 0))
            screen.blit(title_surface, (0, 0))
