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
                
            for neighbor in BFS.get_neighbors(current):
                if neighbor not in came_from and is_valid(game_map, neighbor):
                    queue.append(neighbor)
                    came_from[neighbor] = current
        
        # Dựng lại đường đi từ start đến goal
        path = reconstruct_path(came_from, start, goal)
        
        print("path", path)
        print("nodes expanded", expanded_nodes)

        current, peak_memory = tracemalloc.get_traced_memory()
        peak_memory_kb = peak_memory / (1024)  
        print("current ", current)
        print("peak_memory_kb ", peak_memory_kb)

       
        tracemalloc.stop()
        return path, expanded_nodes, peak_memory_kb

    @staticmethod
    def get_neighbors(pos):
        x, y = pos
        return [
            (x, y - 1),  # Trên
            (x, y + 1),  # Dưới
            (x - 1, y),  # Trái
            (x + 1, y)   # Phải         
        ]