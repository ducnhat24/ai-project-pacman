import heapq

from utils.pathfinding_utils import is_valid, reconstruct_path  # Import from pathfinding_utils

class AStar:
    @staticmethod
    def find_path(game_map, start, goal):
        def heuristic(a, b):
            return abs(a[0] - b[0]) + abs(a[1] - b[1])  # Manhattan distance

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
                new_cost = cost_so_far[current] + 1  

                if next_pos not in cost_so_far or new_cost < cost_so_far[next_pos]:
                    cost_so_far[next_pos] = new_cost
                    priority = new_cost + heuristic(goal, next_pos)
                    heapq.heappush(pq, (priority, next_pos))
                    came_from[next_pos] = current

        return reconstruct_path(came_from, start, goal)
