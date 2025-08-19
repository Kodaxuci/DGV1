import pygame
import math
from settings import *
from assets import AssetManager

class UI:
    def __init__(self):
        """Initialize the modern UI system with asset manager"""
        self.font = pygame.font.Font(None, 24)
        self.small_font = pygame.font.Font(None, 18)
        self.large_font = pygame.font.Font(None, 36)
        
        # Initialize asset manager
        self.assets = AssetManager()
        
        # Skill icons are now handled by the asset manager
        
        # Animation states
        self.damage_flash = {}
        self.heal_flash = {}
        
    def draw_skill_toolbar(self, screen, player, in_battle=False):
        """Draw the MOBA-style skill toolbar at bottom of screen"""
        toolbar_height = 80
        toolbar_y = SCREEN_HEIGHT - toolbar_height
        
        # Toolbar background
        toolbar_rect = pygame.Rect(0, toolbar_y, SCREEN_WIDTH, toolbar_height)
        pygame.draw.rect(screen, (40, 40, 40), toolbar_rect)
        pygame.draw.rect(screen, WHITE, toolbar_rect, 2)
        
        # Skill slots
        skill_start_x = 100
        skills = ['Q', 'W', 'E', 'R']
        skill_descriptions = ['Attack', 'Defend', 'Heal Potion', 'Special']
        
        for i, (skill, desc) in enumerate(zip(skills, skill_descriptions)):
            x = skill_start_x + i * 60
            y = toolbar_y + 20
            
            # Draw skill slot background from assets
            slot_bg = self.assets.get_ui_element('skill_slot')
            if slot_bg:
                screen.blit(slot_bg, (x - 5, y - 5))
            
            # Skill icon from asset manager
            skill_icon = self.assets.get_skill_icon(skill)
            icon_rect = pygame.Rect(x, y, SKILL_ICON_SIZE, SKILL_ICON_SIZE)
            screen.blit(skill_icon, icon_rect)
            
            # Key binding
            key_text = self.small_font.render(skill, True, WHITE)
            screen.blit(key_text, (x + 18, y - 15))
            
            # Description (only show in battle)
            if in_battle:
                desc_text = self.small_font.render(desc, True, WHITE)
                screen.blit(desc_text, (x - 5, y + 50))
        
        # Item slots
        item_start_x = skill_start_x + 300
        for i in range(3):
            x = item_start_x + i * 60
            y = toolbar_y + 20
            
            # Item slot background
            slot_rect = pygame.Rect(x, y, 45, 45)
            pygame.draw.rect(screen, (60, 60, 60), slot_rect)
            pygame.draw.rect(screen, WHITE, slot_rect, 1)
            
            # Show item if available
            if i < len(player.inventory.items):
                item = player.inventory.items[i]
                if item.type == 'potion':
                    pygame.draw.rect(screen, GREEN, pygame.Rect(x + 5, y + 5, 35, 35))
                elif item.type == 'sword':
                    pygame.draw.rect(screen, RED, pygame.Rect(x + 5, y + 5, 35, 35))
                elif item.type == 'shield':
                    pygame.draw.rect(screen, GRAY, pygame.Rect(x + 5, y + 5, 35, 35))
                
                # Item name
                item_text = self.small_font.render(item.name[:8], True, WHITE)
                screen.blit(item_text, (x - 10, y + 50))
            
            # Key binding
            key_text = self.small_font.render(str(i + 1), True, WHITE)
            screen.blit(key_text, (x + 18, y - 15))
    
    def draw_health_bars(self, screen, player, zombie=None):
        """Draw health bars for player and zombie"""
        # Player health bar
        player_hp_width = 200
        player_hp_height = 20
        player_hp_x = 20
        player_hp_y = 20
        
        # Background
        bg_rect = pygame.Rect(player_hp_x, player_hp_y, player_hp_width, player_hp_height)
        pygame.draw.rect(screen, (60, 60, 60), bg_rect)
        pygame.draw.rect(screen, WHITE, bg_rect, 2)
        
        # Health fill
        hp_ratio = player.hp / player.max_hp
        fill_width = int(player_hp_width * hp_ratio)
        fill_rect = pygame.Rect(player_hp_x, player_hp_y, fill_width, player_hp_height)
        
        # Color based on health
        if hp_ratio > 0.6:
            hp_color = GREEN
        elif hp_ratio > 0.3:
            hp_color = YELLOW
        else:
            hp_color = RED
        
        pygame.draw.rect(screen, hp_color, fill_rect)
        
        # HP text
        hp_text = self.font.render(f"HP: {player.hp}/{player.max_hp}", True, WHITE)
        screen.blit(hp_text, (player_hp_x + 5, player_hp_y + 2))
        
        # Zombie health bar (in battle)
        if zombie:
            zombie_hp_width = 200
            zombie_hp_height = 20
            zombie_hp_x = SCREEN_WIDTH - zombie_hp_width - 20
            zombie_hp_y = 20
            
            # Background
            bg_rect = pygame.Rect(zombie_hp_x, zombie_hp_y, zombie_hp_width, zombie_hp_height)
            pygame.draw.rect(screen, (60, 60, 60), bg_rect)
            pygame.draw.rect(screen, WHITE, bg_rect, 2)
            
            # Health fill
            zombie_hp_ratio = zombie['hp'] / zombie['max_hp']
            fill_width = int(zombie_hp_width * zombie_hp_ratio)
            fill_rect = pygame.Rect(zombie_hp_x, zombie_hp_y, fill_width, zombie_hp_height)
            pygame.draw.rect(screen, RED, fill_rect)
            
            # HP text
            hp_text = self.font.render(f"{zombie['name']}: {zombie['hp']}/{zombie['max_hp']}", True, WHITE)
            screen.blit(hp_text, (zombie_hp_x + 5, zombie_hp_y + 2))
    
    def draw_minimap(self, screen, labyrinth, player, zombies, fog_of_war=None):
        """Draw minimap with fog of war support"""
        minimap_size = 150
        minimap_x = SCREEN_WIDTH - minimap_size - 20
        minimap_y = 60
        
        # Minimap background
        minimap_rect = pygame.Rect(minimap_x, minimap_y, minimap_size, minimap_size)
        pygame.draw.rect(screen, (20, 20, 20), minimap_rect)
        pygame.draw.rect(screen, WHITE, minimap_rect, 2)
        
        # Calculate scale
        scale_x = minimap_size / labyrinth.width
        scale_y = minimap_size / labyrinth.height
        
        # Draw maze on minimap (only explored areas)
        for y in range(labyrinth.height):
            for x in range(labyrinth.width):
                mini_x = minimap_x + int(x * scale_x)
                mini_y = minimap_y + int(y * scale_y)
                mini_w = max(1, int(scale_x))
                mini_h = max(1, int(scale_y))
                
                # Only draw if explored (fog of war)
                if fog_of_war and not fog_of_war.is_explored(x, y):
                    continue
                
                if labyrinth.maze[y][x] == 1:  # Wall
                    color = (100, 100, 100)
                    if fog_of_war and not fog_of_war.is_visible(x, y):
                        color = (60, 60, 60)  # Darker for explored but not visible
                    pygame.draw.rect(screen, color, 
                                   pygame.Rect(mini_x, mini_y, mini_w, mini_h))
                else:  # Floor
                    color = (150, 150, 150)
                    if fog_of_war and not fog_of_war.is_visible(x, y):
                        color = (100, 100, 100)  # Darker for explored but not visible
                    pygame.draw.rect(screen, color, 
                                   pygame.Rect(mini_x, mini_y, mini_w, mini_h))
        
        # Draw exit (only if explored)
        exit_x, exit_y = labyrinth.exit_pos
        if not fog_of_war or fog_of_war.is_explored(exit_x, exit_y):
            exit_mini_x = minimap_x + int(exit_x * scale_x)
            exit_mini_y = minimap_y + int(exit_y * scale_y)
            color = GREEN
            if fog_of_war and not fog_of_war.is_visible(exit_x, exit_y):
                color = DARK_GREEN  # Darker if not currently visible
            pygame.draw.rect(screen, color, 
                            pygame.Rect(exit_mini_x, exit_mini_y, max(2, int(scale_x)), max(2, int(scale_y))))
        
        # Draw player (always visible)
        player_mini_x = minimap_x + int(player.x * scale_x)
        player_mini_y = minimap_y + int(player.y * scale_y)
        pygame.draw.rect(screen, BLUE, 
                        pygame.Rect(player_mini_x, player_mini_y, max(3, int(scale_x)), max(3, int(scale_y))))
        
        # Draw zombies (only if currently visible)
        for zombie in zombies:
            if not fog_of_war or fog_of_war.should_show_entity(int(zombie.x), int(zombie.y)):
                zombie_mini_x = minimap_x + int(zombie.x * scale_x)
                zombie_mini_y = minimap_y + int(zombie.y * scale_y)
                pygame.draw.rect(screen, RED, 
                                pygame.Rect(zombie_mini_x, zombie_mini_y, max(2, int(scale_x)), max(2, int(scale_y))))
        
        # Minimap title
        title_text = self.small_font.render("Map", True, WHITE)
        screen.blit(title_text, (minimap_x + 5, minimap_y - 20))
    
    def draw_timer(self, screen, time_left):
        """Draw digital-style timer at top center"""
        minutes = int(time_left // 60)
        seconds = int(time_left % 60)
        time_str = f"{minutes:02d}:{seconds:02d}"
        
        # Timer background
        timer_text = self.large_font.render(time_str, True, WHITE)
        timer_rect = timer_text.get_rect(center=(SCREEN_WIDTH // 2, 30))
        
        bg_rect = timer_rect.copy()
        bg_rect.inflate_ip(20, 10)
        pygame.draw.rect(screen, (40, 40, 40), bg_rect)
        pygame.draw.rect(screen, WHITE, bg_rect, 2)
        
        # Color based on time left
        if time_left > 60:
            color = WHITE
        elif time_left > 30:
            color = YELLOW
        else:
            color = RED
        
        timer_text = self.large_font.render(time_str, True, color)
        screen.blit(timer_text, timer_rect)
    
    def draw_level_info(self, screen, level):
        """Draw level information"""
        level_text = self.font.render(f"Level: {level}", True, WHITE)
        level_rect = pygame.Rect(20, 50, 100, 25)
        pygame.draw.rect(screen, (40, 40, 40), level_rect)
        pygame.draw.rect(screen, WHITE, level_rect, 1)
        screen.blit(level_text, (25, 55))
    
    def draw_battle_overlay(self, screen, battle_log, current_turn):
        """Draw battle information overlay"""
        overlay_height = 200
        overlay_y = SCREEN_HEIGHT // 2 - 100
        overlay_rect = pygame.Rect(50, overlay_y, SCREEN_WIDTH - 100, overlay_height)
        
        # Semi-transparent background
        overlay_surface = pygame.Surface((overlay_rect.width, overlay_rect.height))
        overlay_surface.set_alpha(180)
        overlay_surface.fill((20, 20, 20))
        screen.blit(overlay_surface, overlay_rect)
        pygame.draw.rect(screen, WHITE, overlay_rect, 2)
        
        # Battle title
        title_text = self.large_font.render("BATTLE MODE", True, RED)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, overlay_y + 30))
        screen.blit(title_text, title_rect)
        
        # Turn indicator
        turn_text = self.font.render(f"Turn: {current_turn.capitalize()}", True, YELLOW)
        screen.blit(turn_text, (overlay_rect.x + 20, overlay_y + 60))
        
        # Battle log
        log_y = overlay_y + 90
        for line in battle_log[-4:]:  # Show last 4 lines
            log_text = self.small_font.render(line, True, WHITE)
            screen.blit(log_text, (overlay_rect.x + 20, log_y))
            log_y += 20
    
    def flash_damage(self, entity_id, duration=500):
        """Start damage flash animation"""
        self.damage_flash[entity_id] = pygame.time.get_ticks() + duration
    
    def flash_heal(self, entity_id, duration=500):
        """Start heal flash animation"""
        self.heal_flash[entity_id] = pygame.time.get_ticks() + duration
    
    def get_flash_alpha(self, entity_id, flash_type='damage'):
        """Get flash alpha value for animations"""
        current_time = pygame.time.get_ticks()
        flash_dict = self.damage_flash if flash_type == 'damage' else self.heal_flash
        
        if entity_id in flash_dict and current_time < flash_dict[entity_id]:
            remaining = flash_dict[entity_id] - current_time
            return int(100 * (remaining / 500))  # Fade out
        return 0
    
    def draw_sprites(self, screen, labyrinth, player, zombies, fog_of_war=None):
        """Draw sprites with texture assets and fog of war support"""
        # Calculate maze offset
        maze_pixel_width = labyrinth.width * CELL_SIZE
        maze_pixel_height = labyrinth.height * CELL_SIZE
        offset_x = (SCREEN_WIDTH - maze_pixel_width) // 2
        offset_y = (SCREEN_HEIGHT - maze_pixel_height) // 2
        
        # Draw player (always visible)
        player_x = offset_x + player.x * CELL_SIZE
        player_y = offset_y + player.y * CELL_SIZE
        
        # Use player sprite from asset manager
        player_sprite = self.assets.get_sprite('player')
        screen.blit(player_sprite, (player_x, player_y))
        
        # Equipment indicators
        weapon = player.get_equipped_item('weapon')
        shield = player.get_equipped_item('shield')
        if weapon:
            pygame.draw.circle(screen, RED, (player_x + CELL_SIZE - 6, player_y + 6), 4)
        if shield:
            pygame.draw.circle(screen, GRAY, (player_x + 6, player_y + 6), 4)
        
        # Heal flash animation
        heal_alpha = self.get_flash_alpha('player', 'heal')
        if heal_alpha > 0:
            heal_surface = pygame.Surface((CELL_SIZE, CELL_SIZE))
            heal_surface.set_alpha(heal_alpha)
            heal_surface.fill(GREEN)
            screen.blit(heal_surface, (player_x, player_y))
        
        # Draw zombies (only if visible through fog of war)
        for i, zombie in enumerate(zombies):
            zombie_tile_x = int(zombie.x)
            zombie_tile_y = int(zombie.y)
            
            # Check fog of war visibility
            if fog_of_war and not fog_of_war.should_show_entity(zombie_tile_x, zombie_tile_y):
                continue
            
            zombie_x = offset_x + zombie.x * CELL_SIZE
            zombie_y = offset_y + zombie.y * CELL_SIZE
            
            # Choose appropriate zombie sprite
            is_boss = hasattr(zombie, 'is_boss') and zombie.is_boss
            zombie_sprite = self.assets.get_sprite('boss' if is_boss else 'zombie')
            screen.blit(zombie_sprite, (int(zombie_x), int(zombie_y)))
            
            # Damage flash animation
            damage_alpha = self.get_flash_alpha(f'zombie_{i}', 'damage')
            if damage_alpha > 0:
                damage_surface = pygame.Surface((CELL_SIZE, CELL_SIZE))
                damage_surface.set_alpha(damage_alpha)
                damage_surface.fill(WHITE)
                screen.blit(damage_surface, (int(zombie_x), int(zombie_y)))
    
    def draw_tilemap(self, screen, labyrinth, fog_of_war=None):
        """Draw tilemap with textures and fog of war support"""
        maze_pixel_width = labyrinth.width * CELL_SIZE
        maze_pixel_height = labyrinth.height * CELL_SIZE
        offset_x = (SCREEN_WIDTH - maze_pixel_width) // 2
        offset_y = (SCREEN_HEIGHT - maze_pixel_height) // 2
        
        for y in range(labyrinth.height):
            for x in range(labyrinth.width):
                # Only draw explored tiles
                if fog_of_war and not fog_of_war.is_explored(x, y):
                    continue
                
                tile_x = offset_x + x * CELL_SIZE
                tile_y = offset_y + y * CELL_SIZE
                
                # Choose texture based on tile type
                if labyrinth.maze[y][x] == 1:
                    texture = self.assets.get_texture('wall')
                else:
                    texture = self.assets.get_texture('floor')
                
                # Draw the texture
                screen.blit(texture, (tile_x, tile_y))
        
        # Draw exit with animated texture (only if explored)
        exit_x, exit_y = labyrinth.exit_pos
        if not fog_of_war or fog_of_war.is_explored(exit_x, exit_y):
            exit_tile_x = offset_x + exit_x * CELL_SIZE
            exit_tile_y = offset_y + exit_y * CELL_SIZE
            
            # Use exit texture
            exit_texture = self.assets.get_texture('exit')
            screen.blit(exit_texture, (exit_tile_x, exit_tile_y))
            
            # Add pulsing glow effect
            time_factor = pygame.time.get_ticks() / 500
            pulse = int(64 + 63 * math.sin(time_factor))
            glow_surface = pygame.Surface((CELL_SIZE, CELL_SIZE))
            glow_surface.set_alpha(pulse)
            glow_surface.fill((0, 255, 0))
            screen.blit(glow_surface, (exit_tile_x, exit_tile_y))
        
        # Draw fog of war overlay
        if fog_of_war:
            fog_of_war.draw_fog(screen, offset_x, offset_y)