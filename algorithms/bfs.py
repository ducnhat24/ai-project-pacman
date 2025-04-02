# In bfs.py
from collections import deque
from utils.pathfinding_utils import is_valid, reconstruct_path  # Import from pathfinding_utils

class BFS:
    @staticmethod
    def find_path(game_map, start, goal):
        queue = deque([start])
        came_from = {start: None}

        while queue:
            current = queue.popleft()
            if current == goal:
                break
            x, y = current
            for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                next_pos = (x + dx, y + dy)
                if next_pos not in came_from and is_valid(game_map, next_pos):
                    queue.append(next_pos)
                    came_from[next_pos] = current
          
        # Check if goal was reached
        if goal not in came_from:
            # No path found - return a path containing just the start position
            return [start]
        
        return reconstruct_path(came_from, start, goal)
