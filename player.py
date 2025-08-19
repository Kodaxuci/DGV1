"""
Advanced Player class for Zombie Dungeon Escape
Supports equipment system, inventory management, and stat calculations
"""

import pygame
from settings import *
from items import Inventory, Item

class Player:
    def __init__(self, x, y):
        """Initialize the player with position, stats, and equipment system"""
        self.x = x
        self.y = y
        
        # Base stats (without equipment)
        self.base_max_hp = PLAYER_MAX_HP
        self.base_attack = PLAYER_BASE_ATTACK
        self.base_defense = 0
        
        # Equipment and inventory system
        self.inventory = Inventory(max_size=20)
        self.gold = 50  # Starting gold
        
        # Calculate current stats based on equipment
        self._update_stats()
        self.hp = self.max_hp  # Start with full HP
        
        # Add starting items
        self.add_to_inventory(Item('potion'))
        self.add_to_inventory(Item('sword'))
    
    def _update_stats(self):
        """Update player stats based on equipped items"""
        equipment_stats = self.inventory.get_equipment_stats()
        
        self.max_hp = self.base_max_hp + equipment_stats.get('health', 0)
        self.attack = self.base_attack + equipment_stats.get('attack', 0)
        self.defense = self.base_defense + equipment_stats.get('defense', 0)
    
    def move(self, dx, dy, maze):
        """Move player if the target position is valid"""
        new_x = self.x + dx
        new_y = self.y + dy
        
        # Check bounds and walls
        if (0 <= new_x < len(maze[0]) and 
            0 <= new_y < len(maze) and 
            maze[new_y][new_x] == 0):
            self.x = new_x
            self.y = new_y
            return True
        return False
    
    def get_attack_power(self):
        """Calculate total attack power including equipment"""
        return self.attack
    
    def get_defense_power(self):
        """Calculate defense power from equipment"""
        return self.defense
    
    def take_damage(self, damage):
        """Take damage, considering defense"""
        actual_damage = max(1, damage - self.defense)  # Minimum 1 damage
        self.hp = max(0, self.hp - actual_damage)
        return actual_damage
    
    def heal(self, amount):
        """Heal player by specified amount"""
        old_hp = self.hp
        self.hp = min(self.hp + amount, self.max_hp)
        return self.hp - old_hp
    
    def is_alive(self):
        """Check if player is still alive"""
        return self.hp > 0
    
    def add_to_inventory(self, item):
        """Add item to inventory"""
        success = self.inventory.add_item(item)
        if success:
            self._update_stats()  # Update stats in case it's equipment
        return success
    
    def use_item(self, item_index):
        """Use item from inventory"""
        if 0 <= item_index < len(self.inventory.items):
            item = self.inventory.items[item_index]
            
            if item.type == 'potion':
                healed = self.heal(item.stats.get('heal', 30))
                self.inventory.remove_item(item_index)
                return f"Used {item.name}! Healed {healed} HP."
            elif item.type == 'gold':
                gold_amount = item.stats.get('gold', 10)
                self.gold += gold_amount
                self.inventory.remove_item(item_index)
                return f"Gained {gold_amount} gold!"
            elif item.is_equipment:
                return "Right-click to equip this item"
        
        return "Cannot use this item"
    
    def equip_item(self, item_index):
        """Equip an item from inventory"""
        success = self.inventory.equip_item(item_index)
        if success:
            old_max_hp = self.max_hp
            self._update_stats()
            
            # If max HP increased and we're at full health, stay at full
            if self.hp == old_max_hp and self.max_hp > old_max_hp:
                self.hp = self.max_hp
            # If max HP decreased, adjust current HP accordingly
            elif self.hp > self.max_hp:
                self.hp = self.max_hp
                
            return True
        return False
    
    def unequip_item(self, slot):
        """Unequip an item and put it back in inventory"""
        if not self.inventory.is_full():
            success = self.inventory.unequip_item(slot)
            if success:
                old_max_hp = self.max_hp
                self._update_stats()
                # Adjust current HP if max HP decreased
                if self.hp > self.max_hp:
                    self.hp = self.max_hp
                return True
        return False
    
    def get_equipped_item(self, slot):
        """Get equipped item in specific slot"""
        return self.inventory.equipped.get(slot)
    
    def pickup_item(self, item):
        """Pickup an item and add to inventory"""
        if self.add_to_inventory(item):
            return f"Picked up {item.name}"
        else:
            return "Inventory is full!"
    
    def get_inventory_grid(self):
        """Get inventory items in grid format for UI"""
        grid = [[None for _ in range(4)] for _ in range(5)]
        
        for i, item in enumerate(self.inventory.items):
            if i < 20:  # 4x5 grid
                row = i // 4
                col = i % 4
                grid[row][col] = item
        
        return grid
    
    def get_item_at_grid_position(self, row, col):
        """Get item at specific grid position"""
        index = row * 4 + col
        if 0 <= index < len(self.inventory.items):
            return self.inventory.items[index], index
        return None, -1