import pygame
import math
from settings import *

class FogOfWar:
    def __init__(self, maze_width, maze_height):
        """Initialize fog of war system"""
        self.width = maze_width
        self.height = maze_height
        
        # Track explored areas
        self.explored = [[False for _ in range(maze_width)] for _ in range(maze_height)]
        
        # Track currently visible areas
        self.visible = [[False for _ in range(maze_width)] for _ in range(maze_height)]
        
        # Create fog overlay surface
        self.fog_overlay = pygame.Surface((maze_width * CELL_SIZE, maze_height * CELL_SIZE))
        self.fog_overlay.set_alpha(FOG_ALPHA)
        
        # Create shadow overlay surface for explored but not visible areas
        self.shadow_overlay = pygame.Surface((maze_width * CELL_SIZE, maze_height * CELL_SIZE))
        self.shadow_overlay.set_alpha(SHADOW_ALPHA)
    
    def update_visibility(self, player_x, player_y, maze):
        """Update visibility based on player position"""
        # Clear current visibility
        for y in range(self.height):
            for x in range(self.width):
                self.visible[y][x] = False
        
        # Calculate visible tiles using simple distance check
        player_tile_x = int(player_x)
        player_tile_y = int(player_y)
        
        for y in range(max(0, player_tile_y - VISION_RADIUS), 
                      min(self.height, player_tile_y + VISION_RADIUS + 1)):
            for x in range(max(0, player_tile_x - VISION_RADIUS), 
                          min(self.width, player_tile_x + VISION_RADIUS + 1)):
                
                # Check if within vision radius
                distance = math.sqrt((x - player_x)**2 + (y - player_y)**2)
                if distance <= VISION_RADIUS:
                    # Simple line of sight check (can be improved with raycasting)
                    if self.has_line_of_sight(player_x, player_y, x, y, maze):
                        self.visible[y][x] = True
                        self.explored[y][x] = True
    
    def has_line_of_sight(self, x1, y1, x2, y2, maze):
        """Simple line of sight check - can be improved with proper raycasting"""
        # For simplicity, we'll use a basic distance check
        # In a more advanced version, you would implement Bresenham's line algorithm
        # to check for walls blocking the view
        
        dx = abs(x2 - x1)
        dy = abs(y2 - y1)
        steps = max(dx, dy)
        
        if steps == 0:
            return True
        
        x_step = (x2 - x1) / steps
        y_step = (y2 - y1) / steps
        
        for i in range(int(steps) + 1):
            check_x = int(x1 + x_step * i)
            check_y = int(y1 + y_step * i)
            
            # Check bounds
            if (check_x < 0 or check_x >= self.width or 
                check_y < 0 or check_y >= self.height):
                return False
            
            # If we hit a wall, line of sight is blocked
            if maze[check_y][check_x] == 1:
                # Allow seeing the wall itself, but not beyond it
                return i == steps
        
        return True
    
    def is_visible(self, x, y):
        """Check if a tile is currently visible"""
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.visible[y][x]
        return False
    
    def is_explored(self, x, y):
        """Check if a tile has been explored"""
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.explored[y][x]
        return False
    
    def should_show_entity(self, x, y):
        """Check if an entity should be visible (enemies only show if in current vision)"""
        return self.is_visible(x, y)
    
    def draw_fog(self, screen, offset_x, offset_y):
        """Draw fog of war overlay"""
        # Clear fog overlay
        self.fog_overlay.fill((0, 0, 0))
        self.shadow_overlay.fill((0, 0, 0))
        
        for y in range(self.height):
            for x in range(self.width):
                tile_x = x * CELL_SIZE
                tile_y = y * CELL_SIZE
                tile_rect = pygame.Rect(tile_x, tile_y, CELL_SIZE, CELL_SIZE)
                
                if not self.explored[y][x]:
                    # Completely unexplored - full fog
                    pygame.draw.rect(self.fog_overlay, (0, 0, 0), tile_rect)
                elif not self.visible[y][x]:
                    # Explored but not currently visible - shadow
                    pygame.draw.rect(self.shadow_overlay, (0, 0, 0), tile_rect)
        
        # Blit fog overlays to screen
        screen.blit(self.fog_overlay, (offset_x, offset_y))
        screen.blit(self.shadow_overlay, (offset_x, offset_y))
    
    def reset(self, new_width, new_height):
        """Reset fog of war for new level"""
        self.width = new_width
        self.height = new_height
        self.explored = [[False for _ in range(new_width)] for _ in range(new_height)]
        self.visible = [[False for _ in range(new_width)] for _ in range(new_height)]
        
        # Recreate overlay surfaces
        self.fog_overlay = pygame.Surface((new_width * CELL_SIZE, new_height * CELL_SIZE))
        self.fog_overlay.set_alpha(FOG_ALPHA)
        self.shadow_overlay = pygame.Surface((new_width * CELL_SIZE, new_height * CELL_SIZE))
        self.shadow_overlay.set_alpha(SHADOW_ALPHA)
    
    def get_minimap_data(self):
        """Get explored and visible data for minimap rendering"""
        return {
            'explored': self.explored,
            'visible': self.visible,
            'width': self.width,
            'height': self.height
        }