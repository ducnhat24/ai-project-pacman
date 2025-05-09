# Cấu hình cho mỗi level trong game
LEVELS = {
    1: {
        "name": "BFS Algorithm",
        "ghosts": [
            {"type": "BFS", "color": "blue", "pos": (57, 2)}
        ],
        "show_test_buttons": True,
        "description": "Ma di chuyển bằng thuật toán BFS (Breadth-First Search)"
    },
    2: {
        "name": "DFS Algorithm",
        "ghosts": [
            {"type": "DFS", "color": "pink", "pos": (57, 2)}
        ],
        "show_test_buttons": True,
        "description": "Ma di chuyển bằng thuật toán DFS (Depth-First Search)"
    },
    3: {
        "name": "UCS Algorithm",
        "ghosts": [
            {"type": "UCS", "color": "orange", "pos": (57, 2)}
        ],
        "show_test_buttons": True,
        "description": "Ma di chuyển bằng thuật toán UCS (Uniform Cost Search)"
    },
    4: {
        "name": "A* Algorithm",
        "ghosts": [
            {"type": "A*", "color": "red", "pos": (57, 2)}
        ],
        "show_test_buttons": True,
        "description": "Ma di chuyển bằng thuật toán A* (A-Star)"
    },
    5: {
        "name": "All Algorithms",
        "ghosts": [
            {"type": "BFS", "color": "blue", "pos": (57, 2)},
            {"type": "DFS", "color": "pink", "pos": (57, 13)},
            {"type": "UCS", "color": "orange", "pos": (57, 21)},
            {"type": "A*", "color": "red", "pos": (57, 30)}
        ],
        "show_test_buttons": False,
        "description": "So sánh tất cả các thuật toán tìm đường đi"
    },
    6: {
        "name": "Custom Level",
        "ghosts": [
            {"type": "BFS", "color": "blue", "pos": (13, 15)},
            {"type": "DFS", "color": "pink", "pos": (16, 15)},
            {"type": "UCS", "color": "orange", "pos": (41, 15)},
            {"type": "A*", "color": "red", "pos": (44, 15)}
        ],
        "show_test_buttons": False,
        "description": "Pacman di chuyển tự do"
    }
}

# Các cấu hình test case cho mỗi level
TEST_CASES = {
    "test1": {
        "ghost_pos": (57, 2),
    },
    "test2": {
        "ghost_pos": (57, 30),
    },
    "test3": {
        "ghost_pos": (2,30),
    },
    "test4": {
        "ghost_pos": (30, 15),
    },
    "test5": {
        "ghost_pos": (45, 21),
    }
}