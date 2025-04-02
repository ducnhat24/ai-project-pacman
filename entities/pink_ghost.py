from entities.ghost import Ghost


class PinkGhost(Ghost):
    def __init__(self, x, y, game_map):
        # Khởi tạo Ghost với loại là pink và tên màu là "pink"
        super().__init__(x, y, game_map, "DFS", "pink")