"""
Chest system for Zombie Dungeon Escape
Handles treasure chests that spawn in the dungeon
"""

import random
from items import Item

class Chest:
    """Treasure chest that contains loot"""
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.is_open = False
        self.animation_timer = 0
        self.contents = self._generate_contents()
    
    def _generate_contents(self):
        """Generate random contents for the chest"""
        contents = []
        
        # Always has at least one item
        item_types = ['potion', 'sword', 'shield', 'armor', 'gold']
        num_items = random.randint(1, 3)
        
        for _ in range(num_items):
            item_type = random.choice(item_types)
            item = Item(item_type)
            contents.append(item)
        
        return contents
    
    def open_chest(self):
        """Open the chest and return its contents"""
        if not self.is_open:
            self.is_open = True
            return self.contents
        return []
    
    def update(self, dt):
        """Update chest animation"""
        if self.is_open:
            self.animation_timer += dt
    
    def can_interact(self, player_x, player_y):
        """Check if player is close enough to interact"""
        distance = ((self.x - player_x) ** 2 + (self.y - player_y) ** 2) ** 0.5
        return distance < 1.2