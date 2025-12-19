import pygame
import json
import os
import sys

# --- Configuration ---
TILE_SIZE = 30

# Map with string
# Define the Map Array: 1=Wall, 2=Normal Pill, 3=Special Pill, 0=Empty Path

# Get the directory of the current file and construct the path to maze.json
try:
    maze_file_path = os.path.normpath(
        os.path.join(os.path.dirname(__file__), "..", "data", "maze.json")
    )
    with open(maze_file_path, "r", encoding="utf-8") as f:
        y = json.load(f)
    map01 = y["1"]["map"]
except FileNotFoundError as e:
    print(f"Map file not found: {e.filename}")
    sys.exit(1)
except json.JSONDecodeError as e:
    print(f"Invalid JSON in maze file at line {e.lineno}, col {e.colno}: {e.msg}")
    sys.exit(1)
except KeyError as e:
    print(f"Missing expected key in maze file: {e}")
    sys.exit(1)
except Exception as e:
    print(f"Unexpected error loading maze: {e}")
    sys.exit(1)
    

# Convart STRING TO LIST
MAP_DATA = [[int(j) for j in i] for i in map01]

MAP_WIDTH = len(MAP_DATA[0])
MAP_HEIGHT = len(MAP_DATA)

SCREEN_WIDTH = MAP_WIDTH * TILE_SIZE
SCREEN_HEIGHT = MAP_HEIGHT * TILE_SIZE

# --- Pygame Initialization ---

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Pacman')

# --- Functions ---

def draw_smooth_map():
    # --- Color Definitions ---
    WALL_BORDER_COLOR = (0, 0, 255) # Blue (The border color)
    WALL_BODY_COLOR = (216, 216, 230) # Light Blue (The wall interior color)
    PATH_COLOR = (0, 0, 0) # Black
    NORMAL_PILL_COLOR = (255, 255, 0) # Yellow
    SPECIAL_PILL_COLOR = (255, 165, 0) # Orange/Power

    # 1. Fill the entire screen with the WALL_BORDER_COLOR. 
    # This acts as the *base layer* for both the walls' border and the path's background.
    screen.fill(WALL_BORDER_COLOR)

    # Define the thickness of the border (e.g., 2 pixels on each side)
    BORDER_THICKNESS = 4 

    for row_index, row in enumerate(MAP_DATA):
        for col_index, tile_value in enumerate(row):
            x = col_index * TILE_SIZE
            y = row_index * TILE_SIZE
            center_x = x + TILE_SIZE // 2
            center_y = y + TILE_SIZE // 2

            if tile_value == 1:
                # --- WALL TILE DRAWING (Bordered) ---
                # Draw the Light Blue wall body *inside* the Blue border area
                
                # New rectangle is shifted inward by BORDER_THICKNESS/2 
                # and reduced in size by BORDER_THICKNESS to create the border effect.
                wall_rect = pygame.Rect(
                    x + BORDER_THICKNESS // 2, 
                    y + BORDER_THICKNESS // 2, 
                    TILE_SIZE - BORDER_THICKNESS, 
                    TILE_SIZE - BORDER_THICKNESS
                )
                pygame.draw.rect(screen, WALL_BODY_COLOR, wall_rect)

            elif tile_value in [0, 2, 3, 5, 6, 7, 8, 9]:
                # --- PATH TILE DRAWING ---
                # Draw a black rectangle that covers the tile space entirely
                # (You used TILE_SIZE+4 previously, TILE_SIZE should be fine 
                # unless you want overlapping paths)
                path_rect = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)
                pygame.draw.rect(screen, PATH_COLOR, path_rect) 
                
                # Now, draw the pills on the black path
                if tile_value == 2:
                    PILL_RADIUS = 4
                    pygame.draw.circle(screen, NORMAL_PILL_COLOR, (center_x, center_y), PILL_RADIUS)
                
                elif tile_value == 3:
                    POWER_RADIUS = 8
                    pygame.draw.circle(screen, SPECIAL_PILL_COLOR, (center_x, center_y), POWER_RADIUS)# --- Main Game Loop ---
    return screen


