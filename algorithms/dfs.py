from utils.pathfinding_utils import is_valid, reconstruct_path  # Import from pathfinding_utils


class DFS:
    @staticmethod
    def find_path(game_map, start, goal):
        stack = [start]
        came_from = {start: None}

        while stack:
            current = stack.pop()
            if current == goal:
                break
            x, y = current
            for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                next_pos = (x + dx, y + dy)
                if next_pos not in came_from and is_valid(game_map, next_pos):
                    stack.append(next_pos)
                    came_from[next_pos] = current

        return reconstruct_path(came_from, start, goal)
