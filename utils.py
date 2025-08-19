import pygame
import math
import random
from settings import *

def calculate_distance(x1, y1, x2, y2):
    """Calculate Euclidean distance between two points"""
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

def get_direction_to_target(from_x, from_y, to_x, to_y):
    """Get normalized direction vector from one point to another"""
    dx = to_x - from_x
    dy = to_y - from_y
    distance = calculate_distance(from_x, from_y, to_x, to_y)
    
    if distance == 0:
        return (0, 0)
    
    return (dx / distance, dy / distance)

def clamp(value, min_value, max_value):
    """Clamp a value between min and max"""
    return max(min_value, min(value, max_value))

def roll_dice(sides=6):
    """Roll a dice with specified number of sides"""
    return random.randint(1, sides)

def roll_multiple_dice(count, sides=6):
    """Roll multiple dice and return the sum"""
    return sum(roll_dice(sides) for _ in range(count))

def get_random_spawn_position(maze_width, maze_height, exclude_positions=None):
    """Get a random valid spawn position in the maze"""
    if exclude_positions is None:
        exclude_positions = []
    
    attempts = 0
    max_attempts = 100
    
    while attempts < max_attempts:
        x = random.randint(1, maze_width - 2)
        y = random.randint(1, maze_height - 2)
        
        # Check if position is not in exclude list
        if (x, y) not in exclude_positions:
            return (x, y)
        
        attempts += 1
    
    # Fallback to a corner if no position found
    return (1, 1)

def draw_text_with_background(screen, text, font, text_color, bg_color, position):
    """Draw text with a background rectangle"""
    text_surface = font.render(text, True, text_color)
    text_rect = text_surface.get_rect()
    text_rect.topleft = position
    
    # Create background rectangle
    bg_rect = text_rect.copy()
    bg_rect.inflate_ip(10, 5)  # Add padding
    
    pygame.draw.rect(screen, bg_color, bg_rect)
    screen.blit(text_surface, text_rect)
    
    return bg_rect

def create_button(screen, text, font, text_color, bg_color, position, padding=10):
    """Create a clickable button and return its rectangle"""
    text_surface = font.render(text, True, text_color)
    text_rect = text_surface.get_rect()
    text_rect.center = position
    
    # Create button rectangle
    button_rect = text_rect.copy()
    button_rect.inflate_ip(padding * 2, padding)
    
    pygame.draw.rect(screen, bg_color, button_rect)
    pygame.draw.rect(screen, WHITE, button_rect, 2)  # Border
    screen.blit(text_surface, text_rect)
    
    return button_rect

def is_point_in_rect(point, rect):
    """Check if a point is inside a rectangle"""
    x, y = point
    return (rect.left <= x <= rect.right and 
            rect.top <= y <= rect.bottom)

def generate_random_color():
    """Generate a random RGB color"""
    return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

def lerp(start, end, t):
    """Linear interpolation between start and end by factor t (0-1)"""
    return start + (end - start) * t

def ease_in_out(t):
    """Ease-in-out function for smooth animations"""
    return t * t * (3 - 2 * t)

def wrap_text(text, font, max_width):
    """Wrap text to fit within specified width"""
    words = text.split(' ')
    lines = []
    current_line = []
    
    for word in words:
        test_line = ' '.join(current_line + [word])
        if font.size(test_line)[0] <= max_width:
            current_line.append(word)
        else:
            if current_line:
                lines.append(' '.join(current_line))
                current_line = [word]
            else:
                lines.append(word)  # Single word is too long
    
    if current_line:
        lines.append(' '.join(current_line))
    
    return lines

def format_time(seconds):
    """Format seconds as MM:SS string"""
    minutes = int(seconds // 60)
    seconds = int(seconds % 60)
    return f"{minutes:02d}:{seconds:02d}"

def get_manhattan_distance(x1, y1, x2, y2):
    """Calculate Manhattan distance between two points"""
    return abs(x2 - x1) + abs(y2 - y1)

def get_neighbors(x, y, width, height, include_diagonal=False):
    """Get valid neighbors of a position within bounds"""
    neighbors = []
    
    if include_diagonal:
        directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    else:
        directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]  # Up, Down, Left, Right
    
    for dx, dy in directions:
        new_x, new_y = x + dx, y + dy
        if 0 <= new_x < width and 0 <= new_y < height:
            neighbors.append((new_x, new_y))
    
    return neighbors

def pathfind_simple(start_x, start_y, target_x, target_y, maze):
    """Simple A* pathfinding implementation"""
    # This is a simplified version - for full A* implementation,
    # you would need priority queues and more complex logic
    
    # For now, return the direct path preference
    dx = target_x - start_x
    dy = target_y - start_y
    
    moves = []
    if abs(dx) > abs(dy):
        moves.append((1 if dx > 0 else -1, 0))
        moves.append((0, 1 if dy > 0 else -1))
    else:
        moves.append((0, 1 if dy > 0 else -1))
        moves.append((1 if dx > 0 else -1, 0))
    
    return moves
