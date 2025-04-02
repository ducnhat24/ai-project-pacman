from entities.ghost import Ghost


class OrangeGhost(Ghost):
    def __init__(self, x, y, game_map):
        # Khởi tạo Ghost với loại là orange và tên màu là "orange"
        super().__init__(x, y, game_map, "UCS", "orange")