import tracemalloc
import random

from utils.pathfinding_utils import is_valid, reconstruct_path  # Import from pathfinding_utils

class DFS:
    @staticmethod
    def find_path(game_map, start, goal):
        tracemalloc.start() 

        stack = [start]                
        came_from = {start: None}      
        expanded_nodes = 0             
        
        while stack:
            current = stack.pop()      
            expanded_nodes += 1        

            if current == goal:
                break                
        
            
            for neighbor in DFS.get_neighbors(current):
                if neighbor not in came_from and is_valid(game_map, neighbor):
                    stack.append(neighbor)
                    came_from[neighbor] = current
        
        # Dựng lại đường đi từ start đến goal
        path = reconstruct_path(came_from, start, goal)
        # print("path", path)
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
        neighbors = [
            (x, y - 1),  # Trên
            (x, y + 1),  # Dưới
            (x - 1, y),  # Trái
            (x + 1, y)   # Phải
        ]
        random.shuffle(neighbors)
        return neighbors
    