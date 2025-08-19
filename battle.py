import pygame
import random
from settings import *

class BattleSystem:
    def __init__(self):
        """Initialize the modern battle system with UI integration"""
        self.in_battle = False
        self.player = None
        self.zombie_info = {
            'hp': 0,
            'max_hp': 0,
            'attack': 0,
            'name': '',
            'id': None
        }
        self.turn = "player"
        self.battle_log = []
        self.waiting_for_input = True
        self.player_defending = False
        self.battle_result = None
        
        # Skill system
        self.skills = {
            'Q': {'name': 'Attack', 'cooldown': 0, 'description': 'Roll dice to attack'},
            'W': {'name': 'Defend', 'cooldown': 0, 'description': 'Reduce next damage'},
            'E': {'name': 'Heal', 'cooldown': 0, 'description': 'Use health potion'},
            'R': {'name': 'Special', 'cooldown': 0, 'description': 'Special ability'}
        }
        
        # UI references
        self.ui = None
        
    def start_battle(self, player, zombie_hp, zombie_attack, zombie_name, zombie_id=None):
        """Start a battle with modern UI system"""
        self.in_battle = True
        self.player = player
        self.zombie_info = {
            'hp': zombie_hp,
            'max_hp': zombie_hp,
            'attack': zombie_attack,
            'name': zombie_name,
            'id': zombie_id
        }
        self.turn = "player"
        self.battle_log = [f"Battle started with {zombie_name}!"]
        self.waiting_for_input = True
        self.player_defending = False
        self.battle_result = None
        
        # Reset skill cooldowns
        for skill in self.skills.values():
            skill['cooldown'] = 0
    
    def handle_skill_input(self, key):
        """Handle QWER skill inputs"""
        if not self.waiting_for_input or self.turn != "player":
            return False
        
        skill_mapping = {
            pygame.K_q: 'Q',
            pygame.K_w: 'W', 
            pygame.K_e: 'E',
            pygame.K_r: 'R'
        }
        
        if key in skill_mapping:
            skill_key = skill_mapping[key]
            return self.use_skill(skill_key)
        
        # Handle number keys for items (1-3)
        if pygame.K_1 <= key <= pygame.K_3:
            item_index = key - pygame.K_1
            return self.use_item(item_index)
            
        return False
    
    def use_skill(self, skill_key):
        """Execute a skill action"""
        if skill_key not in self.skills:
            return False
        
        skill = self.skills[skill_key]
        if skill['cooldown'] > 0:
            self.battle_log.append(f"{skill['name']} is on cooldown!")
            return False
        
        if skill_key == 'Q':  # Attack
            self.attack_action()
        elif skill_key == 'W':  # Defend
            self.defend_action()
        elif skill_key == 'E':  # Heal
            self.heal_action()
        elif skill_key == 'R':  # Special
            self.special_action()
        
        self.waiting_for_input = False
        return True
    
    def attack_action(self):
        """Execute attack with dice roll"""
        if not self.player:
            return
            
        attack_roll = random.randint(DICE_MIN, DICE_MAX)
        base_damage = self.player.get_attack_power()
        total_damage = base_damage + attack_roll
        
        self.zombie_info['hp'] -= total_damage
        self.zombie_info['hp'] = max(0, self.zombie_info['hp'])
        
        self.battle_log.append(f"Player attacks! (Roll: {attack_roll}) Damage: {total_damage}")
        
        # Trigger damage flash animation
        if self.ui:
            self.ui.flash_damage(f'zombie_{self.zombie_info["id"]}')
    
    def defend_action(self):
        """Execute defend action"""
        self.player_defending = True
        self.battle_log.append("Player defends! (Damage reduction next turn)")
    
    def heal_action(self):
        """Execute heal action using potion"""
        if not self.player:
            return
            
        # Find a potion in inventory
        potion_found = False
        for i, item in enumerate(self.player.inventory):
            if item.item_type == 'potion':
                result = self.player.use_item(i)
                self.battle_log.append(result)
                potion_found = True
                
                # Trigger heal flash animation
                if self.ui:
                    self.ui.flash_heal('player')
                break
        
        if not potion_found:
            self.battle_log.append("No potions available!")
    
    def special_action(self):
        """Execute special ability"""
        if not self.player:
            return
            
        # Special: Buff attack for next turn or find item
        if random.random() < 0.5:
            # Attack buff
            self.battle_log.append("Player focuses! Next attack deals extra damage!")
            # This would be implemented with a buff system
        else:
            # Find item
            from items import Item
            item_type = random.choice(['potion', 'sword', 'shield'])
            item = Item(item_type)
            if self.player.add_to_inventory(item):
                self.battle_log.append(f"Found {item.name}!")
            else:
                self.battle_log.append("Inventory full!")
    
    def use_item(self, item_index):
        """Use item from inventory slot"""
        if not self.player:
            return False
            
        if 0 <= item_index < len(self.player.inventory):
            item = self.player.inventory[item_index]
            result = self.player.use_item(item_index)
            self.battle_log.append(result)
            
            # Trigger appropriate animation
            if self.ui and item.item_type == 'potion':
                self.ui.flash_heal('player')
            
            self.waiting_for_input = False
            return True
        
        return False
    
    def update(self):
        """Update battle state and return result"""
        if not self.in_battle:
            return None
        
        # Process player turn completion
        if self.turn == "player" and not self.waiting_for_input:
            # Check if zombie is defeated
            if self.zombie_info['hp'] <= 0:
                self.battle_log.append(f"{self.zombie_info['name']} defeated!")
                self.battle_result = "player_won"
                return "player_won"
            
            # Switch to zombie turn
            self.turn = "zombie"
            self.process_zombie_turn()
        
        # Process zombie turn
        elif self.turn == "zombie":
            # Check if player is defeated
            if not self.player or self.player.hp <= 0:
                self.battle_log.append("Player defeated!")
                self.battle_result = "player_lost"
                return "player_lost"
            
            # Switch back to player turn
            self.turn = "player"
            self.waiting_for_input = True
        
        # Manage battle log size
        if len(self.battle_log) > 8:
            self.battle_log.pop(0)
        
        return None
    
    def process_zombie_turn(self):
        """Process zombie's turn"""
        if not self.player:
            return
            
        # Zombie attacks
        attack_roll = random.randint(DICE_MIN, DICE_MAX)
        base_damage = self.zombie_info['attack'] + attack_roll
        
        # Apply defense if player was defending
        defense_bonus = 5 if self.player_defending else 0
        self.player_defending = False
        
        # Calculate actual damage
        total_defense = self.player.get_defense_power() + defense_bonus
        final_damage = max(1, base_damage - total_defense)
        
        self.player.hp -= final_damage
        self.player.hp = max(0, self.player.hp)
        
        if defense_bonus > 0:
            self.battle_log.append(f"{self.zombie_info['name']} attacks! (Roll: {attack_roll}) Blocked some damage!")
        else:
            self.battle_log.append(f"{self.zombie_info['name']} attacks! (Roll: {attack_roll}) Damage: {final_damage}")
    
    def end_battle(self):
        """End the current battle"""
        self.in_battle = False
        self.player = None
        self.zombie_info = {'hp': 0, 'max_hp': 0, 'attack': 0, 'name': '', 'id': None}
        self.battle_log = []
        self.waiting_for_input = True
        self.player_defending = False
        self.battle_result = None
    
    def get_zombie_info(self):
        """Get zombie information for UI display"""
        return self.zombie_info if self.in_battle else None
    
    def set_ui_reference(self, ui):
        """Set reference to UI system for animations"""
        self.ui = ui