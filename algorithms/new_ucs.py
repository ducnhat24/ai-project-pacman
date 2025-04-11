import heapq
import math
import tracemalloc
from utils.pathfinding_utils import is_valid  
from board_info import BoardInfo 

class NewUCS:
    @staticmethod
    def find_path(game_map, start, goal):
        tracemalloc.start()
        
        # Pre-compute red nodes including goal
        red_nodes = set(BoardInfo.red_nodes)
        if goal not in red_nodes:
            red_nodes.add(goal)
        
        # Track expanded nodes with their costs
        expanded_nodes = {}
        expanded_nodes_count = 0
        
        # Priority queue: (cost_so_far, node, path_to_node)
        heap = [(0, start, [])]
        
        directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]  # up, down, left, right

        while heap:
            cost_so_far, current, current_path = heapq.heappop(heap)
            
            # Skip if we've found a better path to this node already
            if current in expanded_nodes and expanded_nodes[current] <= cost_so_far:
                continue
                
            expanded_nodes[current] = cost_so_far
            
            # Count node expansion for red nodes only
            if current in red_nodes:
                expanded_nodes_count += 1
                
            # Check goal
            if current == goal:
                path = current_path
                break
                
            # Explore in four directions
            for dx, dy in directions:
                next_pos = current
                path_segment = []
                
                # Move in this direction until hitting a red node or invalid position
                while True:
                    next_pos = (next_pos[0] + dx, next_pos[1] + dy)
                    
                    if not is_valid(game_map, next_pos):
                        break
                        
                    path_segment.append(next_pos)
                    
                    if next_pos in red_nodes:
                        # Calculate Euclidean distance
                        step_cost = math.sqrt((current[0] - next_pos[0])**2 + (current[1] - next_pos[1])**2)
                        new_cost = cost_so_far + step_cost
                        
                        if next_pos not in expanded_nodes:
                            new_path = current_path + path_segment
                            heapq.heappush(heap, (new_cost, next_pos, new_path))
                        break
        
        # In case we didn't find a path
        if 'path' not in locals():
            path = []
        
        print("path:", path)
        print("nodes expanded:", expanded_nodes_count)
        
        # Get memory usage statistics
        current, peak_memory = tracemalloc.get_traced_memory()
        print("current:", current)
        print("peak_memory:", peak_memory)
        
        peak_memory_kb = peak_memory / 1024
        tracemalloc.stop()
        
        return path, expanded_nodes_count, peak_memory_kb
