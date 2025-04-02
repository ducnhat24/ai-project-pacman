from entities.ghost import Ghost


class RedGhost(Ghost):
    def __init__(self, x, y, game_map):
        # Khởi tạo Ghost với loại là red và tên màu là "red"
        super().__init__(x, y, game_map, "A*", "red")