from settings import *
from collections import deque

def find_bfs_path(self, player, map):
    start = (self.rect.x // TEXTURE_SIZE, self.rect.y // TEXTURE_SIZE)
    goal = (player.rect.x // TEXTURE_SIZE, player.rect.y // TEXTURE_SIZE)

    queue = deque([(start, [start])])
    visited = set()

    while queue:
        current_node, path = queue.popleft()
        
        if current_node == goal:
            return path

        for neighbor in get_neighbors(current_node, map):
            if neighbor not in visited:
                queue.append((neighbor, path + [neighbor]))
                visited.add(neighbor)

    return []

def get_neighbors(node, map):
    x, y = node
    neighbors = []
    
    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (1, -1), (-1, 1), (1, 1)]:
        new_x, new_y = x + dx, y + dy
        
        if (0 <= new_x < 2 * WIDTH // TEXTURE_SIZE and 0 <= new_y < 2 * HEIGHT // TEXTURE_SIZE and not map.check_if_wall(new_y, new_x)):
            neighbors.append((new_x, new_y))

    return neighbors

# Embark on a mage's journey through treacherous tunnels. Cast spells, battle enemies, and unravel secrets.
# Shape the realm's destiny, solve puzzles, and become a legendary hero. The fate of the realm is in your hands.
