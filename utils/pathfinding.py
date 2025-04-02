# In pathfinding.py
from algorithms.bfs import BFS
from algorithms.dfs import DFS
from algorithms.ucs import UCS
from algorithms.astar import AStar
from utils.pathfinding_utils import is_valid, reconstruct_path  # Import from pathfinding_utils

class PathFinding:
    @staticmethod
    def find_path(game_map, start, goal, ghost_type):
        """ Chọn thuật toán tùy theo loại Ghost """
        if ghost_type == "A*":
            return AStar.find_path(game_map, start, goal)
        elif ghost_type == "DFS":
            return DFS.find_path(game_map, start, goal)
        elif ghost_type == "BFS":
            return BFS.find_path(game_map, start, goal)
        elif ghost_type == "UCS":
            return UCS.find_path(game_map, start, goal)
        else:
            raise ValueError("Unknown ghost type")
