class Entity:
    def __init__(self, x, y, game_map):
        self.x = x  # Hàng
        self.y = y  # Cột
        self.game_map = game_map
        self.target = None  # Đặt mục tiêu cho các Ghost

    def move(self, dx, dy):
        """ Di chuyển theo hướng được chỉ định nếu hợp lệ """
        if self.is_valid_move(dx, dy):
            self.x += dx
            self.y += dy

    def update_position(self):
        """ Cập nhật vị trí thực tế của Entity dựa trên ma trận (x, y) """
        pass

    def set_target(self, target_x, target_y):
        """ Đặt mục tiêu cho Entity để di chuyển theo """
        self.target = (target_x, target_y)

    def get_valid_moves(self):
        """ Trả về danh sách các hướng di chuyển hợp lệ dựa trên ma trận """
        valid_moves = []
        # Kiểm tra các hướng di chuyển và thêm vào valid_moves nếu hợp lệ
        return valid_moves

    def is_valid_move(self, dx, dy):
        """Kiểm tra xem có thể di chuyển theo hướng dx, dy không"""
        new_x = dx
        new_y = dy
        return self.can_move(new_x, new_y)

    def distance_to_target(self):
        """ Tính khoảng cách từ vị trí hiện tại đến mục tiêu """
        target_x, target_y = self.target
        return abs(self.x - target_x) + abs(self.y - target_y)

    def respawn(self, start_x, start_y):
        """ Đưa entity về vị trí ban đầu khi chết """
        self.x = start_x
        self.y = start_y
    def can_move(self, new_x, new_y):
        """ Kiểm tra xem có thể di chuyển đến vị trí mới không """
        # Kiểm tra nếu vị trí mới không ra ngoài màn hình và có thể di chuyển
        if 0 <= new_x < len(self.game_map) and 0 <= new_y < len(self.game_map[0]):
            #in giá trị của ô mới
            # print(f"Giá trị ô mới: {self.game_map[new_x][new_y]}")
            return self.game_map[new_x][new_y] in [0, 1, 2] # Pac-Man có thể đi qua ô có giá trị 0 hoặc 2
        return False