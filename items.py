"""
Advanced Item and Equipment system for Zombie Dungeon Escape
Handles consumables, weapons, equipment, loot drops, and inventory management
"""

import random
from settings import *

class Item:
    """Represents an item in the game with rarity and equipment capabilities"""
    
    def __init__(self, item_type, rarity='common'):
        self.type = item_type
        self.rarity = rarity
        self.is_equipment = item_type in ['sword', 'shield', 'armor', 'helmet']
        self.equipment_slot = self._get_equipment_slot()
        self.stats = self._get_stats()
        self.name = self._get_name()
        self.description = self._get_description()
        self.value = self._get_value()
        
    def _get_name(self):
        """Get item name based on type and rarity"""
        base_names = {
            'potion': 'Health Potion',
            'sword': 'Sword',
            'shield': 'Shield',
            'armor': 'Armor',
            'helmet': 'Helmet',
            'gold': 'Gold Coins'
        }
        
        rarity_prefixes = {
            'common': '',
            'uncommon': 'Fine ',
            'rare': 'Superior ',
            'epic': 'Masterwork ',
            'legendary': 'Legendary '
        }
        
        base_name = base_names.get(self.type, 'Unknown Item')
        prefix = rarity_prefixes.get(self.rarity, '')
        
        return f"{prefix}{base_name}".strip()
    
    def _get_description(self):
        """Get item description with stats"""
        if self.type == 'potion':
            return f"Restores {self.stats.get('heal', 30)} HP"
        elif self.type == 'gold':
            return f"Worth {self.stats.get('gold', 10)} coins"
        elif self.is_equipment:
            stat_text = []
            if 'attack' in self.stats:
                stat_text.append(f"+{self.stats['attack']} Attack")
            if 'defense' in self.stats:
                stat_text.append(f"+{self.stats['defense']} Defense")
            if 'health' in self.stats:
                stat_text.append(f"+{self.stats['health']} Health")
            return ', '.join(stat_text) if stat_text else 'No bonus stats'
        
        return 'No description'
    
    def _get_stats(self):
        """Get item stat bonuses based on type and rarity"""
        rarity_multiplier = {
            'common': 1.0,
            'uncommon': 1.5,
            'rare': 2.0,
            'epic': 2.5,
            'legendary': 3.0
        }
        
        multiplier = rarity_multiplier.get(self.rarity, 1.0)
        
        base_stats = {
            'potion': {'heal': int(30 * multiplier)},
            'sword': {'attack': int(5 * multiplier)},
            'shield': {'defense': int(3 * multiplier)},
            'armor': {'defense': int(4 * multiplier), 'health': int(10 * multiplier)},
            'helmet': {'defense': int(2 * multiplier), 'health': int(5 * multiplier)},
            'gold': {'gold': random.randint(5, 20)}
        }
        
        return base_stats.get(self.type, {})
    
    def _get_value(self):
        """Get item gold value"""
        base_values = {
            'potion': 10,
            'sword': 25,
            'shield': 20,
            'armor': 30,
            'helmet': 15,
            'gold': self.stats.get('gold', 10)
        }
        
        rarity_multiplier = {
            'common': 1.0,
            'uncommon': 2.0,
            'rare': 4.0,
            'epic': 8.0,
            'legendary': 15.0
        }
        
        base_value = base_values.get(self.type, 1)
        multiplier = rarity_multiplier.get(self.rarity, 1.0)
        
        return int(base_value * multiplier)
    
    def _get_equipment_slot(self):
        """Get which equipment slot this item goes in"""
        slots = {
            'sword': 'weapon',
            'shield': 'shield',
            'armor': 'body',
            'helmet': 'head'
        }
        return slots.get(self.type, None)
    
    def use(self, player):
        """Use the item on the player (for consumables)"""
        if self.type == "potion":
            old_hp = player.hp
            player.heal(self.stats.get('heal', 30))
            healed = player.hp - old_hp
            return f"Healed {healed} HP!"
        elif self.type == "gold":
            player.gold += self.stats.get('gold', 10)
            return f"Gained {self.stats.get('gold', 10)} gold!"
        
        return "This item cannot be used directly."

class LootDrop:
    """Represents a loot drop on the ground"""
    
    def __init__(self, x, y, item):
        self.x = x
        self.y = y
        self.item = item
        self.glow_timer = 0
        self.bounce_timer = 0
    
    def update(self, dt):
        """Update loot drop animation"""
        self.glow_timer += dt * 3
        self.bounce_timer += dt * 4
    
    def can_pickup(self, player_x, player_y):
        """Check if player is close enough to pick up"""
        distance = ((self.x - player_x) ** 2 + (self.y - player_y) ** 2) ** 0.5
        return distance < 1.0

class Inventory:
    """Advanced inventory system with equipment management"""
    
    def __init__(self, max_size=20):
        self.items = []
        self.max_size = max_size
        self.grid_width = 4
        self.grid_height = 5
        
        # Equipment slots
        self.equipped = {
            'weapon': None,
            'shield': None,
            'head': None,
            'body': None
        }
    
    def add_item(self, item):
        """Add item to inventory if there's space"""
        if len(self.items) < self.max_size:
            self.items.append(item)
            return True
        return False
    
    def remove_item(self, index):
        """Remove item at specified index"""
        if 0 <= index < len(self.items):
            return self.items.pop(index)
        return None
    
    def get_item(self, index):
        """Get item at specified index without removing it"""
        if 0 <= index < len(self.items):
            return self.items[index]
        return None
    
    def equip_item(self, item_index):
        """Equip an item from inventory"""
        if 0 <= item_index < len(self.items):
            item = self.items[item_index]
            if item.is_equipment and item.equipment_slot:
                # Unequip current item in that slot
                old_item = self.equipped.get(item.equipment_slot)
                if old_item:
                    self.add_item(old_item)
                
                # Equip new item
                self.equipped[item.equipment_slot] = item
                self.remove_item(item_index)
                return True
        return False
    
    def unequip_item(self, slot):
        """Unequip an item and put it back in inventory"""
        if slot in self.equipped and self.equipped[slot]:
            item = self.equipped[slot]
            if self.add_item(item):
                self.equipped[slot] = None
                return True
        return False
    
    def get_equipment_stats(self):
        """Get total stats from all equipped items"""
        total_stats = {
            'attack': 0,
            'defense': 0,
            'health': 0
        }
        
        for item in self.equipped.values():
            if item and hasattr(item, 'stats') and item.stats:
                for stat, value in item.stats.items():
                    if stat in total_stats:
                        total_stats[stat] += value
        
        return total_stats
    
    def is_full(self):
        """Check if inventory is full"""
        return len(self.items) >= self.max_size

def generate_random_item():
    """Generate a random item with random rarity"""
    item_types = ['potion', 'sword', 'shield', 'armor', 'helmet', 'gold']
    rarities = ['common', 'common', 'common', 'uncommon', 'uncommon', 'rare', 'epic', 'legendary']
    
    item_type = random.choice(item_types)
    rarity = random.choice(rarities)
    
    return Item(item_type, rarity)

def generate_zombie_loot():
    """Generate loot that zombies can drop"""
    if random.random() < 0.3:  # 30% chance to drop something
        if random.random() < 0.6:  # 60% chance for common items
            item_types = ['potion', 'gold']
        else:  # 40% chance for equipment
            item_types = ['sword', 'shield', 'armor', 'helmet']
        
        item_type = random.choice(item_types)
        rarity = random.choices(['common', 'uncommon', 'rare', 'epic', 'legendary'], 
                               weights=[60, 25, 10, 4, 1])[0]
        
        return Item(item_type, rarity)
    
    return None