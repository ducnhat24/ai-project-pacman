import heapq

from utils.pathfinding_utils import is_valid, reconstruct_path  # Import from pathfinding_utils

class UCS:
    @staticmethod
    def find_path(game_map, start, goal):
        pq = [(0, start)]
        came_from = {start: None}
        cost_so_far = {start: 0}

        while pq:
            current_cost, current = heapq.heappop(pq)
            if current == goal:
                break
            x, y = current
            for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                next_pos = (x + dx, y + dy)
                new_cost = current_cost + 1  # Uniform cost

                if next_pos not in cost_so_far or new_cost < cost_so_far[next_pos]:
                    cost_so_far[next_pos] = new_cost
                    heapq.heappush(pq, (new_cost, next_pos))
                    came_from[next_pos] = current

        return reconstruct_path(came_from, start, goal)
