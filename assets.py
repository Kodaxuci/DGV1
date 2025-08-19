import pygame
from settings import *

class AssetManager:
    def __init__(self):
        """Initialize the asset manager with texture loading"""
        self.textures = {}
        self.sprites = {}
        self.skill_icons = {}
        self.ui_elements = {}
        
        # Load all assets
        self.create_textures()
        self.create_sprites()
        self.create_skill_icons()
        self.create_ui_elements()
    
    def create_textures(self):
        """Create dungeon-style textures (32x32 pixels)"""
        tile_size = TEXTURE_SIZE
        
        # Stone wall texture
        wall_texture = pygame.Surface((tile_size, tile_size))
        wall_texture.fill((80, 60, 40))  # Dark brown base
        # Add stone pattern
        for i in range(0, tile_size, 4):
            for j in range(0, tile_size, 4):
                if (i + j) % 8 == 0:
                    pygame.draw.rect(wall_texture, (100, 80, 60), 
                                   pygame.Rect(i, j, 3, 3))
        pygame.draw.rect(wall_texture, (60, 40, 20), 
                        pygame.Rect(0, 0, tile_size, tile_size), 1)
        self.textures['wall'] = wall_texture
        
        # Dungeon floor texture
        floor_texture = pygame.Surface((tile_size, tile_size))
        floor_texture.fill((160, 140, 120))  # Light stone
        # Add floor tiles pattern
        for i in range(0, tile_size, 16):
            for j in range(0, tile_size, 16):
                pygame.draw.rect(floor_texture, (140, 120, 100), 
                               pygame.Rect(i, j, 15, 15))
        pygame.draw.rect(floor_texture, (120, 100, 80), 
                        pygame.Rect(0, 0, tile_size, tile_size), 1)
        self.textures['floor'] = floor_texture
        
        # Iron door/exit texture
        exit_texture = pygame.Surface((tile_size, tile_size))
        exit_texture.fill((40, 80, 40))  # Dark green base
        # Add door pattern
        pygame.draw.rect(exit_texture, (60, 120, 60), 
                        pygame.Rect(4, 4, tile_size-8, tile_size-8))
        pygame.draw.rect(exit_texture, (80, 160, 80), 
                        pygame.Rect(8, 8, tile_size-16, tile_size-16))
        # Door handle
        pygame.draw.circle(exit_texture, (200, 200, 100), 
                          (tile_size-8, tile_size//2), 3)
        self.textures['exit'] = exit_texture
        
        # Fog texture
        fog_texture = pygame.Surface((tile_size, tile_size))
        fog_texture.fill((20, 20, 20))
        fog_texture.set_alpha(180)  # Semi-transparent
        self.textures['fog'] = fog_texture
        
        # Shadow texture
        shadow_texture = pygame.Surface((tile_size, tile_size))
        shadow_texture.fill((0, 0, 0))
        shadow_texture.set_alpha(120)  # Semi-transparent
        self.textures['shadow'] = shadow_texture
    
    def create_sprites(self):
        """Create character and entity sprites (32x32 pixels)"""
        sprite_size = TEXTURE_SIZE
        
        # Player sprite
        player_sprite = pygame.Surface((sprite_size, sprite_size))
        player_sprite.fill((0, 100, 200))  # Blue base
        # Player body
        pygame.draw.circle(player_sprite, (0, 80, 180), 
                          (sprite_size//2, sprite_size//2), sprite_size//3)
        # Player head
        pygame.draw.circle(player_sprite, (220, 180, 140), 
                          (sprite_size//2, sprite_size//3), sprite_size//5)
        # Eyes
        pygame.draw.circle(player_sprite, (0, 0, 0), 
                          (sprite_size//2-4, sprite_size//3-2), 2)
        pygame.draw.circle(player_sprite, (0, 0, 0), 
                          (sprite_size//2+4, sprite_size//3-2), 2)
        self.sprites['player'] = player_sprite
        
        # Zombie sprite
        zombie_sprite = pygame.Surface((sprite_size, sprite_size))
        zombie_sprite.fill((120, 0, 0))  # Dark red base
        # Zombie body
        pygame.draw.circle(zombie_sprite, (100, 0, 0), 
                          (sprite_size//2, sprite_size//2), sprite_size//3)
        # Zombie head
        pygame.draw.circle(zombie_sprite, (140, 120, 100), 
                          (sprite_size//2, sprite_size//3), sprite_size//5)
        # Glowing red eyes
        pygame.draw.circle(zombie_sprite, (255, 0, 0), 
                          (sprite_size//2-4, sprite_size//3-2), 3)
        pygame.draw.circle(zombie_sprite, (255, 0, 0), 
                          (sprite_size//2+4, sprite_size//3-2), 3)
        # Torn clothes effect
        for i in range(5):
            x = sprite_size//4 + i * 3
            y = sprite_size//2 + i * 2
            pygame.draw.rect(zombie_sprite, (80, 0, 0), 
                           pygame.Rect(x, y, 2, 4))
        self.sprites['zombie'] = zombie_sprite
        
        # Boss zombie sprite (larger and darker)
        boss_sprite = pygame.Surface((sprite_size, sprite_size))
        boss_sprite.fill((80, 0, 0))
        pygame.draw.circle(boss_sprite, (60, 0, 0), 
                          (sprite_size//2, sprite_size//2), sprite_size//2-2)
        pygame.draw.circle(boss_sprite, (100, 80, 60), 
                          (sprite_size//2, sprite_size//4), sprite_size//4)
        # Larger glowing eyes
        pygame.draw.circle(boss_sprite, (255, 50, 0), 
                          (sprite_size//2-6, sprite_size//4-2), 4)
        pygame.draw.circle(boss_sprite, (255, 50, 0), 
                          (sprite_size//2+6, sprite_size//4-2), 4)
        self.sprites['boss'] = boss_sprite
    
    def create_skill_icons(self):
        """Create skill icons for the MOBA-style UI"""
        icon_size = SKILL_ICON_SIZE
        
        # Attack skill (Q) - Sword icon
        attack_icon = pygame.Surface((icon_size, icon_size))
        attack_icon.fill((200, 50, 50))
        # Sword blade
        pygame.draw.rect(attack_icon, (220, 220, 220), 
                        pygame.Rect(icon_size//2-2, 5, 4, icon_size//2))
        # Sword handle
        pygame.draw.rect(attack_icon, (139, 69, 19), 
                        pygame.Rect(icon_size//2-3, icon_size//2+5, 6, icon_size//3))
        # Sword guard
        pygame.draw.rect(attack_icon, (180, 180, 180), 
                        pygame.Rect(icon_size//2-6, icon_size//2, 12, 3))
        self.skill_icons['Q'] = attack_icon
        
        # Defend skill (W) - Shield icon
        defend_icon = pygame.Surface((icon_size, icon_size))
        defend_icon.fill((50, 100, 200))
        # Shield shape
        pygame.draw.circle(defend_icon, (180, 180, 180), 
                          (icon_size//2, icon_size//2), icon_size//3)
        pygame.draw.circle(defend_icon, (160, 160, 160), 
                          (icon_size//2, icon_size//2), icon_size//4)
        # Shield cross
        pygame.draw.rect(defend_icon, (200, 200, 200), 
                        pygame.Rect(icon_size//2-1, icon_size//4, 2, icon_size//2))
        pygame.draw.rect(defend_icon, (200, 200, 200), 
                        pygame.Rect(icon_size//4, icon_size//2-1, icon_size//2, 2))
        self.skill_icons['W'] = defend_icon
        
        # Heal skill (E) - Potion icon
        heal_icon = pygame.Surface((icon_size, icon_size))
        heal_icon.fill((50, 200, 50))
        # Bottle shape
        pygame.draw.rect(heal_icon, (100, 255, 100), 
                        pygame.Rect(icon_size//3, icon_size//4, icon_size//3, icon_size//2))
        # Bottle neck
        pygame.draw.rect(heal_icon, (80, 200, 80), 
                        pygame.Rect(icon_size//2-2, icon_size//6, 4, icon_size//4))
        # Cork
        pygame.draw.rect(heal_icon, (139, 69, 19), 
                        pygame.Rect(icon_size//2-2, icon_size//8, 4, icon_size//8))
        # Liquid
        pygame.draw.rect(heal_icon, (150, 255, 150), 
                        pygame.Rect(icon_size//3+2, icon_size//3, icon_size//3-4, icon_size//3))
        self.skill_icons['E'] = heal_icon
        
        # Special skill (R) - Star icon
        special_icon = pygame.Surface((icon_size, icon_size))
        special_icon.fill((200, 100, 200))
        # Star shape (simplified)
        center = (icon_size//2, icon_size//2)
        points = []
        for i in range(10):
            angle = i * 36 * 3.14159 / 180
            if i % 2 == 0:
                radius = icon_size//3
            else:
                radius = icon_size//6
            x = center[0] + radius * pygame.math.Vector2(1, 0).rotate_rad(angle).x
            y = center[1] + radius * pygame.math.Vector2(1, 0).rotate_rad(angle).y
            points.append((x, y))
        pygame.draw.polygon(special_icon, (255, 255, 100), points)
        self.skill_icons['R'] = special_icon
    
    def create_ui_elements(self):
        """Create UI elements and textures"""
        # Health bar background
        health_bg = pygame.Surface((200, 20))
        health_bg.fill((60, 60, 60))
        pygame.draw.rect(health_bg, (40, 40, 40), 
                        pygame.Rect(0, 0, 200, 20), 2)
        self.ui_elements['health_bg'] = health_bg
        
        # Mana bar background (for future use)
        mana_bg = pygame.Surface((200, 15))
        mana_bg.fill((40, 40, 80))
        pygame.draw.rect(mana_bg, (20, 20, 60), 
                        pygame.Rect(0, 0, 200, 15), 2)
        self.ui_elements['mana_bg'] = mana_bg
        
        # Skill slot background
        skill_slot = pygame.Surface((SKILL_ICON_SIZE + 10, SKILL_ICON_SIZE + 10))
        skill_slot.fill((60, 60, 60))
        pygame.draw.rect(skill_slot, (80, 80, 80), 
                        pygame.Rect(2, 2, SKILL_ICON_SIZE + 6, SKILL_ICON_SIZE + 6))
        pygame.draw.rect(skill_slot, (40, 40, 40), 
                        pygame.Rect(0, 0, SKILL_ICON_SIZE + 10, SKILL_ICON_SIZE + 10), 2)
        self.ui_elements['skill_slot'] = skill_slot
        
        # Item slot background
        item_slot = pygame.Surface((40, 40))
        item_slot.fill((80, 60, 40))
        pygame.draw.rect(item_slot, (100, 80, 60), 
                        pygame.Rect(2, 2, 36, 36))
        pygame.draw.rect(item_slot, (60, 40, 20), 
                        pygame.Rect(0, 0, 40, 40), 2)
        self.ui_elements['item_slot'] = item_slot
    
    def get_texture(self, name):
        """Get texture by name"""
        return self.textures.get(name, self.textures.get('floor'))
    
    def get_sprite(self, name):
        """Get sprite by name"""
        return self.sprites.get(name, self.sprites.get('player'))
    
    def get_skill_icon(self, skill):
        """Get skill icon by skill key"""
        return self.skill_icons.get(skill, self.skill_icons.get('Q'))
    
    def get_ui_element(self, name):
        """Get UI element by name"""
        return self.ui_elements.get(name)