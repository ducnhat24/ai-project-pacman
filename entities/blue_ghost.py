from entities.ghost import Ghost


class BlueGhost(Ghost):
    def __init__(self, x, y, game_map):
        # Khởi tạo Ghost với loại là blue và tên màu là "blue"
        super().__init__(x, y, game_map, "BFS", "blue")