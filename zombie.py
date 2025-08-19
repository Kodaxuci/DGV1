import pygame
import math
import random
from settings import *
from items import generate_zombie_loot

class Zombie:
    def __init__(self, x, y, speed, level=1):
        """Initialize zombie with position, speed, and level-based stats"""
        self.x = x
        self.y = y
        self.speed = speed
        self.level = level
        self.last_move_time = 0
        self.move_cooldown = 0.5  # Seconds between moves
        
        # Level-based stats
        self.max_hp = ZOMBIE_BASE_HP + (level * 5)
        self.hp = self.max_hp
        self.attack = ZOMBIE_BASE_ATTACK + (level * 2)
        self.defense = max(0, level - 1)
        
        # Loot generation
        self.can_drop_loot = True
        
    def update(self, player_x, player_y, maze, dt):
        """Update zombie AI - chase player through maze"""
        self.last_move_time += dt
        
        if self.last_move_time >= self.move_cooldown:
            self.chase_player(player_x, player_y, maze)
            self.last_move_time = 0
    
    def chase_player(self, player_x, player_y, maze):
        """Simple AI to chase player through the maze"""
        # Calculate distance to player
        dx = player_x - self.x
        dy = player_y - self.y
        
        # Determine preferred movement direction
        moves = []
        
        if abs(dx) > abs(dy):
            # Prefer horizontal movement
            if dx > 0:
                moves.append((1, 0))  # Right
            else:
                moves.append((-1, 0))  # Left
            
            if dy > 0:
                moves.append((0, 1))  # Down
            else:
                moves.append((0, -1))  # Up
        else:
            # Prefer vertical movement
            if dy > 0:
                moves.append((0, 1))  # Down
            else:
                moves.append((0, -1))  # Up
            
            if dx > 0:
                moves.append((1, 0))  # Right
            else:
                moves.append((-1, 0))  # Left
        
        # Try moves in order of preference
        for move_dx, move_dy in moves:
            new_x = self.x + move_dx
            new_y = self.y + move_dy
            
            # Check if move is valid
            if self.is_valid_move(new_x, new_y, maze):
                self.x = new_x
                self.y = new_y
                return
        
        # If no preferred move works, try random movement
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        random.shuffle(directions)
        
        for move_dx, move_dy in directions:
            new_x = self.x + move_dx
            new_y = self.y + move_dy
            
            if self.is_valid_move(new_x, new_y, maze):
                self.x = new_x
                self.y = new_y
                return
    
    def is_valid_move(self, x, y, maze):
        """Check if the zombie can move to this position"""
        # Check bounds
        if x < 0 or x >= len(maze[0]) or y < 0 or y >= len(maze):
            return False
        
        # Check for walls
        if maze[y][x] == 1:
            return False
        
        return True
    
    def draw(self, screen):
        """Draw the zombie on screen"""
        # Calculate screen position
        maze_pixel_width = MAZE_WIDTH * CELL_SIZE
        maze_pixel_height = MAZE_HEIGHT * CELL_SIZE
        offset_x = (SCREEN_WIDTH - maze_pixel_width) // 2
        offset_y = (SCREEN_HEIGHT - maze_pixel_height) // 2
        
        screen_x = offset_x + self.x * CELL_SIZE
        screen_y = offset_y + self.y * CELL_SIZE
        
        # Draw zombie as red rectangle with animation
        zombie_rect = pygame.Rect(screen_x + 3, screen_y + 3, CELL_SIZE - 6, CELL_SIZE - 6)
        pygame.draw.rect(screen, RED, zombie_rect)
        
        # Draw eyes as small white squares
        eye_size = 2
        left_eye = pygame.Rect(screen_x + 6, screen_y + 6, eye_size, eye_size)
        right_eye = pygame.Rect(screen_x + CELL_SIZE - 8, screen_y + 6, eye_size, eye_size)
        pygame.draw.rect(screen, WHITE, left_eye)
        pygame.draw.rect(screen, WHITE, right_eye)
    
    def get_distance_to_player(self, player_x, player_y):
        """Calculate distance to player"""
        return math.sqrt((self.x - player_x)**2 + (self.y - player_y)**2)
    
    def drop_loot(self):
        """Generate loot when zombie is killed"""
        if self.can_drop_loot:
            self.can_drop_loot = False  # Prevent multiple drops
            return generate_zombie_loot()
        return None
    
    def take_damage(self, damage):
        """Take damage and return True if zombie dies"""
        actual_damage = max(1, damage - self.defense)
        self.hp = max(0, self.hp - actual_damage)
        return self.hp <= 0
    
    def is_alive(self):
        """Check if zombie is still alive"""
        return self.hp > 0
