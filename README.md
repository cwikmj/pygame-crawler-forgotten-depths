# The Forgotten Depths
The MAZE GAME project is a top-down 2D isometric game where players take on the role of a mage character fighting skeleton enemies. The game includes various features such as player movement, enemy AI using pathfinding logic, firing projectiles, collision detection, usage of potions, and sound effects. It also includes a menu system allowing to start a new game, pause it or quit.

![menu](https://github.com/cwikmj/pygame-crawler-forgotten-depths/assets/88622607/5ab87d0c-a4e5-408a-97ee-4d25ae094a29)
## Acknowledgments
This game was created by the owner of this Github repo using Pygame. The game uses resources from OpenGameArt.org, a website that provides free and open-source game assets.
## License
This game is licensed under the MIT License. However, please mention me as the original creator in case your project goes public.

![game](https://github.com/cwikmj/pygame-crawler-forgotten-depths/assets/88622607/308876b7-8b24-4552-a31f-0259651901dd)
## Running the project
Follow the steps to run game locally
1. prerequirements: __python 3.x.x__
2. install __pygame__
```
pip install pygame
```
3. clone this repository
4. run from the root folder
```
python main.py
```
## Controls
- WASD: Player movement
- SPACE bar: Shoot spell
- ESC key: Pause/resume game
- H key: use health potion (must find one first)
- M key: use mana potion (must find one first)
- R key: Resume game (available during a paused game)
- Q key: Quit game (available during a paused game)

![shot](https://github.com/cwikmj/pygame-crawler-forgotten-depths/assets/88622607/4ff090a7-78b6-4275-a256-795f5ed3bc21)
## How to play
- Navigate character through the maze
- Burn skeletons before they get to you
- Collect potions stored in the chests
- Find the key to unlock the exit door, beware of its guardian!
- Pause the game at any time using the ESC key
- Resume gameplay by pressing R key
- Quit the game from the Paused Menu
## Pathfinding Algorithm
Implemented using Breadth-First Search (BFS), focuses on finding the shortest path between two points (player and NPC) by traversing through a grid. It uses a deque (double ended queue) to keep track of explored nodes and their corresponding paths, with the goal node being the destination. If an enemy finds the player within its attack range, it updates its current state to 'chase' and starts moving towards the player.

![pathfind](https://github.com/cwikmj/pygame-crawler-forgotten-depths/assets/88622607/45b32a76-452a-4436-a61f-6309eeeeb444)
## Map Generation
The map is generated procedurally using a 2D array representing a grid of maze cells. The Map class is responsible for creating the maze by initializing empty cells, defining walls and decorations based on predefined arrays. The game then renders these maze cells during each frame using their respective texture images. This results in the creation of a maze that is twice the width and height of the game window.
## Modules Breakdown
- [main.py](main.py) - serves as the main entry point of the project, initializes Pygame, sets up the game screen, loads assets, and handles the game loop
- [settings.py](settings.py) contains constants used throughout the project such as screen resolution, sizes of tiles, objects etc
- [menu.py](menu.py) handles creating the menus with buttons
- [sounds.py](sounds.py) contains functions for loading and playing various sound effects and background music.
- [map.py](map.py) defines the Map class and Chests class responsible for rendering the maze tiles, chest locations, checking wall collisions, and level completion once all enemies are defeated
- [levels.py](levels.py) arrays with map corresponding tiles
- [player.py](player.py) handles player character behavior like movement, shooting spells, and death animations
- [playerstats.py](playerstats.py) handles displaying and updating player statistics such as health bar, mana bar, potions
- [projectiles.py](projectiles.py) handles the rendering, animation, movement, and collision detection of projectiles fired by the mage
- [npc.py](npc.py) defines the NPC (enemy) class, responsible for enemy pathfinding towards the player, attacking the player upon collision with a projectile, and death animations
- [pathfinding.py](pathfinding.py) returns the shortest path from the NPC to the player with the use of Breadth-First Search algorithm
## Future Development Ideas
- Add more features to the game, such power-ups, more spells, 2nd and 3rd level
- Improve the game's graphics and sound effects
- Fix some bugs
