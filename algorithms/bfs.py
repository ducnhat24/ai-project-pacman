# In bfs.py
from collections import deque
import tracemalloc

from utils.pathfinding_utils import is_valid, reconstruct_path 

class BFS:
    @staticmethod
    def find_path(game_map, start, goal):
        tracemalloc.start()

        queue = deque([start])
        came_from = {start: None}
        expanded_nodes = 0 

        while queue:
            current = queue.popleft()
            expanded_nodes += 1
            
            if current == goal:
                break
                
            x, y = current

            # Duyệt 4 hướng: trên, dưới, trái, phải
            for dx, dy in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
                next_pos = (x + dx, y + dy)
                if next_pos not in came_from and is_valid(game_map, next_pos):
                    queue.append(next_pos)
                    came_from[next_pos] = current
        
        
    #    # Nếu không tìm được đường đi đến goal, trả về danh sách chỉ chứa start
    #     if goal not in came_from:
    #         return [start], expanded_nodes
        
        # Dựng lại đường đi từ start đến goal
        path = reconstruct_path(came_from, start, goal)
        
        print("path", path)
        print("nodes expanded", expanded_nodes)

        current, peak_memory = tracemalloc.get_traced_memory()
        print("current ", current)
        print("peak_memory ", peak_memory)

        peak_memory_kb = peak_memory / (1024)  
        tracemalloc.stop()

        return path, expanded_nodes, peak_memory_kb
