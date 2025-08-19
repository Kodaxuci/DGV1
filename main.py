import pygame
import sys
from settings import *
from player import Player
from labyrinth import Labyrinth
from zombie import Zombie
from battle import BattleSystem
from items import Item, LootDrop, generate_random_item
from ui import UI
from fog_of_war import FogOfWar
from chest import Chest
from utils import *
import random
import time

class Game:
    def __init__(self):
        """Initialize the game with pygame and game state variables"""
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Zombie Dungeon Escape")
        self.clock = pygame.time.Clock()
        
        # Game state
        self.running = True
        self.game_state = "PLAYING"  # PLAYING, BATTLE, GAME_OVER, VICTORY
        self.level = 1
        self.level_timer = LEVEL_TIME
        self.last_time = time.time()
        
        # Initialize game objects
        self.labyrinth = Labyrinth(MAZE_WIDTH, MAZE_HEIGHT)
        self.player = Player(1, 1)  # Start position in maze
        self.zombies = []
        self.battle = BattleSystem()
        self.ui = UI()
        self.fog_of_war = FogOfWar(MAZE_WIDTH, MAZE_HEIGHT)
        self.loot_drops = []  # Items dropped on the ground
        self.popup_messages = []  # Pickup and notification messages
        self.inventory_open = False  # Inventory panel state
        
        # Connect UI to battle system for animations
        self.battle.set_ui_reference(self.ui)
        
        # Spawn initial zombies
        self.spawn_zombies()
        
        # Font for UI (keeping for compatibility)
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        
    def spawn_zombies(self):
        """Spawn zombies from the edges of the maze"""
        self.zombies = []
        zombie_count = min(3 + self.level, 10)  # Increase zombies per level, max 10
        
        for _ in range(zombie_count):
            # Spawn from edges
            edge = random.choice(['top', 'bottom', 'left', 'right'])
            if edge == 'top':
                x, y = random.randint(1, self.labyrinth.width-2), 1
            elif edge == 'bottom':
                x, y = random.randint(1, self.labyrinth.width-2), self.labyrinth.height-2
            elif edge == 'left':
                x, y = 1, random.randint(1, self.labyrinth.height-2)
            else:  # right
                x, y = self.labyrinth.width-2, random.randint(1, self.labyrinth.height-2)
            
            # Make sure spawn position is not a wall
            if self.labyrinth.maze[y][x] == 0:
                zombie_speed = min(ZOMBIE_BASE_SPEED + (self.level * 0.1), 2.0)
                self.zombies.append(Zombie(x, y, zombie_speed))
    
    def handle_events(self):
        """Handle pygame events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            elif event.type == pygame.KEYDOWN:
                if self.game_state == "PLAYING":
                    self.handle_movement(event.key)
                elif self.game_state == "BATTLE":
                    self.battle.handle_skill_input(event.key)
                elif self.game_state in ["GAME_OVER", "VICTORY"]:
                    if event.key == pygame.K_r:
                        self.restart_game()
                    elif event.key == pygame.K_q:
                        self.running = False
    
    def handle_movement(self, key):
        """Handle player movement"""
        dx, dy = 0, 0
        if key in [pygame.K_w, pygame.K_UP]:
            dy = -1
        elif key in [pygame.K_s, pygame.K_DOWN]:
            dy = 1
        elif key in [pygame.K_a, pygame.K_LEFT]:
            dx = -1
        elif key in [pygame.K_d, pygame.K_RIGHT]:
            dx = 1
        
        if dx != 0 or dy != 0:
            self.player.move(dx, dy, self.labyrinth.maze)
    
    def update(self):
        """Update game state"""
        if self.game_state == "PLAYING":
            self.update_playing()
        elif self.game_state == "BATTLE":
            self.update_battle()
    
    def update_playing(self):
        """Update game state during playing mode"""
        current_time = time.time()
        dt = current_time - self.last_time
        self.last_time = current_time
        
        # Update fog of war based on player position
        self.fog_of_war.update_visibility(self.player.x, self.player.y, self.labyrinth.maze)
        
        # Update timer
        self.level_timer -= dt
        if self.level_timer <= 0:
            self.game_state = "GAME_OVER"
            return
        
        # Update zombies
        for zombie in self.zombies:
            zombie.update(self.player.x, self.player.y, self.labyrinth.maze, dt)
            
            # Check collision with player
            if abs(zombie.x - self.player.x) < 0.8 and abs(zombie.y - self.player.y) < 0.8:
                self.start_battle(zombie, self.zombies.index(zombie))
                return
        
        # Check if player reached exit
        exit_x, exit_y = self.labyrinth.exit_pos
        if abs(self.player.x - exit_x) < 0.8 and abs(self.player.y - exit_y) < 0.8:
            self.next_level()
    
    def start_battle(self, zombie, zombie_index):
        """Start battle mode with a zombie"""
        self.game_state = "BATTLE"
        
        # Determine if this is a boss battle
        is_boss = (self.level % 5 == 0)
        if is_boss:
            zombie_hp = BOSS_HP + (self.level // 5) * 20
            zombie_attack = ZOMBIE_BASE_ATTACK + (self.level // 5) * 2
            zombie_name = f"Boss Zombie (Lv.{self.level})"
        else:
            zombie_hp = ZOMBIE_BASE_HP + (self.level * 2)
            zombie_attack = ZOMBIE_BASE_ATTACK + (self.level // 2)
            zombie_name = f"Zombie (Lv.{self.level})"
        
        self.battle.start_battle(self.player, zombie_hp, zombie_attack, zombie_name, zombie_index)
        self.current_battle_zombie = zombie
    
    def update_battle(self):
        """Update battle state"""
        battle_result = self.battle.update()
        
        if battle_result == "player_won":
            # Remove the defeated zombie
            if self.current_battle_zombie in self.zombies:
                self.zombies.remove(self.current_battle_zombie)
            self.game_state = "PLAYING"
            self.battle.end_battle()
            
        elif battle_result == "player_lost":
            self.game_state = "GAME_OVER"
            self.battle.end_battle()
    
    def next_level(self):
        """Progress to the next level"""
        self.level += 1
        self.level_timer = LEVEL_TIME - (self.level * 5)  # Decrease time each level
        self.level_timer = max(self.level_timer, 30)  # Minimum 30 seconds
        
        # Generate new maze (bigger every few levels)
        maze_width = MAZE_WIDTH
        maze_height = MAZE_HEIGHT
        if self.level % 3 == 0:
            maze_width = min(MAZE_WIDTH + 2, 30)
            maze_height = min(MAZE_HEIGHT + 2, 20)
        
        self.labyrinth = Labyrinth(maze_width, maze_height)
        self.fog_of_war.reset(maze_width, maze_height)  # Reset fog of war for new level
        self.player.x, self.player.y = 1, 1  # Reset player position
        self.spawn_zombies()
        
        # Add level completion reward
        if random.random() < 0.7:  # 70% chance for item
            item_type = random.choice(['potion', 'sword', 'shield'])
            item = Item(item_type)
            self.player.add_to_inventory(item)
    
    def restart_game(self):
        """Restart the game"""
        self.level = 1
        self.level_timer = LEVEL_TIME
        self.game_state = "PLAYING"
        self.labyrinth = Labyrinth(MAZE_WIDTH, MAZE_HEIGHT)
        self.fog_of_war.reset(MAZE_WIDTH, MAZE_HEIGHT)  # Reset fog of war
        self.player = Player(1, 1)
        self.spawn_zombies()
        self.last_time = time.time()
    
    def draw(self):
        """Draw everything on the screen"""
        self.screen.fill(BLACK)
        
        if self.game_state == "PLAYING":
            self.draw_playing()
        elif self.game_state == "BATTLE":
            self.draw_battle()
        elif self.game_state == "GAME_OVER":
            self.draw_game_over()
        elif self.game_state == "VICTORY":
            self.draw_victory()
        
        pygame.display.flip()
    
    def draw_playing(self):
        """Draw the playing state with modern UI and fog of war"""
        # Draw improved tilemap with fog of war
        self.ui.draw_tilemap(self.screen, self.labyrinth, self.fog_of_war)
        
        # Draw entities with better sprites and fog of war
        self.ui.draw_sprites(self.screen, self.labyrinth, self.player, self.zombies, self.fog_of_war)
        
        # Draw modern UI elements
        self.ui.draw_health_bars(self.screen, self.player)
        self.ui.draw_timer(self.screen, self.level_timer)
        self.ui.draw_level_info(self.screen, self.level)
        self.ui.draw_minimap(self.screen, self.labyrinth, self.player, self.zombies, self.fog_of_war)
        self.ui.draw_skill_toolbar(self.screen, self.player, in_battle=False)
    
    def draw_battle(self):
        """Draw the battle state with modern UI and fog of war"""
        # Draw background maze with fog of war (dimmed)
        self.ui.draw_tilemap(self.screen, self.labyrinth, self.fog_of_war)
        
        # Draw entities with fog of war
        self.ui.draw_sprites(self.screen, self.labyrinth, self.player, self.zombies, self.fog_of_war)
        
        # Draw battle UI
        zombie_info = self.battle.get_zombie_info()
        self.ui.draw_health_bars(self.screen, self.player, zombie_info)
        self.ui.draw_battle_overlay(self.screen, self.battle.battle_log, self.battle.turn)
        self.ui.draw_skill_toolbar(self.screen, self.player, in_battle=True)
    

    
    def draw_game_over(self):
        """Draw game over screen"""
        # Semi-transparent overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(128)
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0, 0))
        
        # Game over text
        game_over_text = self.font.render("GAME OVER!", True, RED)
        text_rect = game_over_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 50))
        self.screen.blit(game_over_text, text_rect)
        
        # Instructions
        restart_text = self.small_font.render("Press R to Restart or Q to Quit", True, WHITE)
        text_rect = restart_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 20))
        self.screen.blit(restart_text, text_rect)
        
        # Final level
        level_text = self.small_font.render(f"Reached Level: {self.level}", True, WHITE)
        text_rect = level_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 50))
        self.screen.blit(level_text, text_rect)
    
    def draw_victory(self):
        """Draw victory screen"""
        # Semi-transparent overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(128)
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0, 0))
        
        victory_text = self.font.render("VICTORY!", True, GREEN)
        text_rect = victory_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
        self.screen.blit(victory_text, text_rect)
    
    def run(self):
        """Main game loop"""
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        
        pygame.quit()
        sys.exit()

def main():
    """Entry point of the game"""
    game = Game()
    game.run()

if __name__ == "__main__":
    main()
