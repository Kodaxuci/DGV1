import pygame
import random
from settings import *
from chest import Chest

class Labyrinth:
    def __init__(self, width, height):
        """
        Initialize the labyrinth with specified dimensions
        Uses recursive backtracking algorithm to generate maze
        """
        self.width = width
        self.height = height
        self.maze = [[1 for _ in range(width)] for _ in range(height)]  # 1 = wall, 0 = path
        self.exit_pos = (width - 2, height - 2)  # Exit near bottom-right
        self.chests = []  # List of treasure chests
        
        # Generate the maze
        self.generate_maze()
        
        # Ensure exit is accessible
        self.maze[self.exit_pos[1]][self.exit_pos[0]] = 0
        
        # Spawn treasure chests
        self.spawn_chests()
    
    def generate_maze(self):
        """Generate maze using recursive backtracking algorithm"""
        # Start from top-left corner (1, 1)
        start_x, start_y = 1, 1
        self.maze[start_y][start_x] = 0
        
        # Stack for backtracking
        stack = [(start_x, start_y)]
        
        while stack:
            current_x, current_y = stack[-1]
            
            # Get unvisited neighbors
            neighbors = self.get_unvisited_neighbors(current_x, current_y)
            
            if neighbors:
                # Choose random neighbor
                next_x, next_y = random.choice(neighbors)
                
                # Remove wall between current cell and chosen neighbor
                wall_x = (current_x + next_x) // 2
                wall_y = (current_y + next_y) // 2
                self.maze[wall_y][wall_x] = 0
                self.maze[next_y][next_x] = 0
                
                # Add neighbor to stack
                stack.append((next_x, next_y))
            else:
                # No unvisited neighbors, backtrack
                stack.pop()
    
    def get_unvisited_neighbors(self, x, y):
        """Get list of unvisited neighbors that are 2 cells away"""
        neighbors = []
        directions = [(0, -2), (2, 0), (0, 2), (-2, 0)]  # Up, Right, Down, Left
        
        for dx, dy in directions:
            new_x, new_y = x + dx, y + dy
            
            # Check bounds
            if (0 < new_x < self.width - 1 and 
                0 < new_y < self.height - 1 and 
                self.maze[new_y][new_x] == 1):
                neighbors.append((new_x, new_y))
        
        return neighbors
    
    def is_valid_position(self, x, y):
        """Check if position is valid (not a wall and within bounds)"""
        if x < 0 or x >= self.width or y < 0 or y >= self.height:
            return False
        return self.maze[y][x] == 0
    
    def draw(self, screen):
        """Draw the labyrinth on the screen"""
        # Calculate offset to center the maze
        maze_pixel_width = self.width * CELL_SIZE
        maze_pixel_height = self.height * CELL_SIZE
        offset_x = (SCREEN_WIDTH - maze_pixel_width) // 2
        offset_y = (SCREEN_HEIGHT - maze_pixel_height) // 2
        
        for y in range(self.height):
            for x in range(self.width):
                rect = pygame.Rect(
                    offset_x + x * CELL_SIZE,
                    offset_y + y * CELL_SIZE,
                    CELL_SIZE,
                    CELL_SIZE
                )
                
                if self.maze[y][x] == 1:
                    # Draw wall
                    pygame.draw.rect(screen, BROWN, rect)
                else:
                    # Draw path
                    pygame.draw.rect(screen, WHITE, rect)
                
                # Draw border
                pygame.draw.rect(screen, BLACK, rect, 1)
        
        # Draw exit
        exit_rect = pygame.Rect(
            offset_x + self.exit_pos[0] * CELL_SIZE,
            offset_y + self.exit_pos[1] * CELL_SIZE,
            CELL_SIZE,
            CELL_SIZE
        )
        pygame.draw.rect(screen, GREEN, exit_rect)
        
    def spawn_chests(self):
        """Spawn treasure chests randomly in the maze"""
        chest_count = max(2, (self.width * self.height) // 50)  # 1 chest per ~50 cells
        attempts = 0
        max_attempts = 100
        
        while len(self.chests) < chest_count and attempts < max_attempts:
            x = random.randint(2, self.width - 3)
            y = random.randint(2, self.height - 3)
            
            # Check if position is valid (path, not exit, not near start)
            if (self.maze[y][x] == 0 and 
                (x, y) != self.exit_pos and 
                (x > 3 or y > 3)):  # Not too close to start
                
                # Check if there's already a chest nearby
                too_close = False
                for chest in self.chests:
                    if abs(chest.x - x) < 3 and abs(chest.y - y) < 3:
                        too_close = True
                        break
                
                if not too_close:
                    self.chests.append(Chest(x, y))
            
            attempts += 1
    
    def get_chest_at_position(self, x, y):
        """Get chest at specific position if exists"""
        for chest in self.chests:
            if chest.x == x and chest.y == y:
                return chest
        return None
    
    def remove_chest(self, chest):
        """Remove a chest from the maze"""
        if chest in self.chests:
            self.chests.remove(chest)
    
    def get_screen_position(self, x, y):
        """Convert maze coordinates to screen coordinates"""
        maze_pixel_width = self.width * CELL_SIZE
        maze_pixel_height = self.height * CELL_SIZE
        offset_x = (SCREEN_WIDTH - maze_pixel_width) // 2
        offset_y = (SCREEN_HEIGHT - maze_pixel_height) // 2
        
        return (offset_x + x * CELL_SIZE, offset_y + y * CELL_SIZE)
