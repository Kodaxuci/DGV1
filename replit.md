# Zombie Dungeon Escape

## Overview

Zombie Dungeon Escape is a roguelike survival game that combines labyrinth exploration with turn-based combat mechanics. Players navigate through procedurally generated mazes while avoiding zombies that spawn from the edges. When caught, players engage in dice-based turn-based battles. The game features progressive difficulty through levels, an inventory system with consumables and equipment, and boss battles at certain milestones.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Game Engine and Framework
- **PyGame-based architecture**: Uses PyGame for rendering, input handling, and game loop management
- **Object-oriented design**: Modular classes for Player, Zombie, Battle, Labyrinth, and Items
- **Game state management**: Central Game class coordinates between different game modes (PLAYING, BATTLE, GAME_OVER, VICTORY)

### Core Game Systems

#### Maze Generation System
- **Algorithm**: Recursive backtracking for procedural maze generation
- **Structure**: 2D grid system with walls (1) and paths (0)
- **Rendering**: Cell-based drawing with configurable cell size

#### Combat System
- **Turn-based mechanics**: Player and zombie alternate turns
- **Dice-based calculations**: Attack and defense values determined by dice rolls
- **Equipment integration**: Weapons and shields modify base stats
- **Battle log**: Text-based feedback system for combat actions

#### Inventory Management
- **Item types**: Consumables (potions), weapons (swords), and defensive gear (shields)
- **Equipment slots**: Separate slots for weapons and shields with stat bonuses
- **Usage system**: Items can be consumed during battle or exploration

#### AI and Movement
- **Zombie AI**: Simple pathfinding that chases player position
- **Movement validation**: Grid-based movement with collision detection
- **Spawn system**: Edge-based zombie spawning with progressive difficulty

#### Level Progression
- **Timer-based levels**: Each level has a time limit for maze completion
- **Scaling difficulty**: Zombie count and stats increase with level progression
- **Boss encounters**: Special high-HP enemies at milestone levels

### Data Management
- **Configuration system**: Centralized settings file for game parameters
- **Game state persistence**: In-memory state management during gameplay
- **Utility functions**: Helper functions for distance calculation, dice rolling, and pathfinding

## External Dependencies

### Core Libraries
- **PyGame**: Primary game framework for graphics, sound, input handling, and display management
- **Python Standard Library**: 
  - `random` module for procedural generation and dice mechanics
  - `math` module for distance calculations and AI pathfinding
  - `time` module for level timing and game loop management
  - `sys` module for application lifecycle management

### Asset Requirements
- **Fonts**: PyGame's default font system for UI text rendering
- **Colors**: RGB color definitions for game graphics (no external image assets)

The game is designed as a self-contained Python application with minimal external dependencies, relying primarily on PyGame and standard library modules.