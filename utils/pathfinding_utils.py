# In pathfinding_utils.py
# def is_valid(game_map, position):
#     x, y = position
#     if 0 <= x < len(game_map) and 0 <= y < len(game_map[0]):  # Check bounds
#         return game_map[x][y] == 0  # Check if the cell is not a wall (assuming 0 is walkable)
#     return False

# def reconstruct_path(came_from, start, goal):
#     path = []
#     current = goal
#     while current != start:
#         path.append(current)
#         current = came_from[current]
#     path.append(start)  # Add start to the path
#     path.reverse()  # Reverse the path to get it from start to goal
#     return path


def reconstruct_path(came_from, start, goal):
    path = []
    current = goal

    
    # Handle the case where no path exists
    if goal not in came_from:
        return [start]  # Return just the start position
        
    while current != start:
        path.append(current)
        current = came_from[current]
    # path.append(start)  # Add start to the path
    path.reverse()  # Reverse the path to get it from start to goal
    print(path)
    return path



# def is_valid(game_map, position):
#     new_x, new_y = position
#     """ Kiểm tra xem có thể di chuyển đến vị trí mới không """
#     # Kiểm tra nếu vị trí mới không ra ngoài màn hình và có thể di chuyển
#     if 0 <= new_x < len(game_map) and 0 <= new_y < len(game_map[0]):
#         #in giá trị của ô mới
#         return game_map[new_x][new_y] in [0, 1, 2] # Pac-Man có thể đi qua ô có giá trị 0 hoặc 2
#     return False
#     # x, y = position
#     # if 0 <= x < len(game_map) and 0 <= y < len(game_map[0]):  # Check bounds
#     #     # Allow movement through cells with 0 (empty), 1 (dots), etc.
#     #     return game_map[x][y] in [0, 1, 2]  # Adjust this set based on your game
#     # return False

def is_valid(game_map, pos):
    x, y = pos
    return 0 <= x < len(game_map[0]) and 0 <= y < len(game_map) and game_map[y][x] in [0, 1, 2]
