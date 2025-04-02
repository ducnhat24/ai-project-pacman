# Mô tả hàm này

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
    #print(path)
    return path

def is_valid(game_map, pos):
    x, y = pos
    return 0 <= x < len(game_map[0]) and 0 <= y < len(game_map) and game_map[y][x] in [0, 1, 2]
