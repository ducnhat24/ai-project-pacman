import copy
import pygame
from math import pi
from settings import Config, Color
from board_info import BoardInfo
from settings import Config, Color

class MazeDrawing:
    TILE_WIDTH = Config.TILE_WIDTH
    TILE_HEIGHT = Config.TILE_HEIGHT

    def __init__(self, screen):
        self.board = BoardInfo()  # Khởi tạo BoardInfo
        self.map = copy.deepcopy(self.board.game_map)  # Initialize the maze from Board
        self.screen = screen
        # Check xem map có rỗng không
        if not self.map: # Kiểm tra xem map có rỗng không
            return
        self.num_rows = len(self.map)
        if self.num_rows == 0 or not self.map[0]: 
            return
        self.num_cols = len(self.map[0])
        
        total_map_width_px = self.num_cols * self.TILE_WIDTH
        total_map_height_px = self.num_rows * self.TILE_HEIGHT

        screen_width = Config.SCREEN_WIDTH
        screen_height = Config.SCREEN_HEIGHT

        self.offset_x = (screen_width - total_map_width_px) // 2
        self.offset_y = 10


    def draw(self):
        # # Check xem map có rỗng không
        # if not self.map: # Kiểm tra xem map có rỗng không
        #     return
        # num_rows = len(self.map)
        # if num_rows == 0 or not self.map[0]: 
        #     return
        # num_cols = len(self.map[0])

        # total_map_width_px = num_cols * self.TILE_WIDTH
        # total_map_height_px = num_rows * self.TILE_HEIGHT

        # screen_width = Config.SCREEN_WIDTH
        # screen_height = Config.SCREEN_HEIGHT

        # # Tính toán vị trí bắt đầu vẽ (offset) để căn giữa
        # offset_x = (screen_width - total_map_width_px) // 2 
        # # offset_y = (screen_height - total_map_height_px) // 2
        # offset_y = 10


        # --- Vòng lặp vẽ từng ô, áp dụng offset ---
        for i in range(self.num_rows):
            for j in range(self.num_cols):
                cell = self.map[i][j]

                # Tọa độ góc trên-trái của ô hiện tại (đã cộng offset)
                draw_base_x = j * self.TILE_WIDTH + self.offset_x
                draw_base_y = i * self.TILE_HEIGHT + self.offset_y

                # Tọa độ tâm của ô hiện tại (đã cộng offset)
                draw_center_x = draw_base_x + (self.TILE_WIDTH / 2)
                draw_center_y = draw_base_y + (self.TILE_HEIGHT / 2)

                # Chuyển đổi tọa độ sang số nguyên vì pygame.draw thường yêu cầu int
                int_base_x = int(draw_base_x)
                int_base_y = int(draw_base_y)
                int_center_x = int(draw_center_x)
                int_center_y = int(draw_center_y)
                int_TILE_WIDTH = int(self.TILE_WIDTH)
                int_TILE_HEIGHT = int(self.TILE_HEIGHT)

                # --- Vẽ các loại ô ---
                if cell == 1: # normal food
                    pygame.draw.circle(self.screen, Color.color_food, (int_center_x, int_center_y), 4)

                elif cell == 2: # power food
                    pygame.draw.circle(self.screen, Color.color_power_food, (int_center_x, int_center_y), 10)

                elif cell == 3: # vertical wall (vẽ đường thẳng đứng giữa ô)
                    pygame.draw.line(self.screen, Color.color_wall,
                                    (int_center_x, int_base_y), # Điểm bắt đầu (trên)
                                    (int_center_x, int_base_y + int_TILE_HEIGHT), # Điểm kết thúc (dưới)
                                    4)

                elif cell == 4: # horizontal wall (vẽ đường ngang giữa ô)
                    pygame.draw.line(self.screen, Color.color_wall,
                                    (int_base_x, int_center_y), # Điểm bắt đầu (trái)
                                    (int_base_x + int_TILE_WIDTH, int_center_y), # Điểm kết thúc (phải)
                                    4)

                # --- Vẽ các cung tròn (góc tường) ---
                # Lưu ý: Vẽ cung tròn trong pygame hơi phức tạp.
                # Nó yêu cầu một hình chữ nhật bao quanh (bounding rectangle) [left, top, width, height]
                # và góc bắt đầu, góc kết thúc (bằng radian).
                # Các tính toán gốc của bạn có vẻ hơi phức tạp, có thể cần điều chỉnh lại
                # dựa trên cách bạn muốn góc tường hiển thị chính xác.
                # Dưới đây là áp dụng offset vào các tính toán gốc đó, nhưng bạn có thể cần xem lại logic vẽ arc.

                elif cell == 5: # Góc dưới-trái
                    # Tính toán gốc: [(j * self.TILE_WIDTH - (self.TILE_WIDTH * 0.4)) - 2, cy, self.TILE_WIDTH, self.TILE_HEIGHT]
                    # Áp dụng offset:
                    rect_left = int(draw_base_x - int_TILE_WIDTH * 0.4 - 2) # Tọa độ left của rect
                    rect_top = int(draw_center_y) # Tọa độ top của rect (dựa trên cy gốc)
                    arc_rect = pygame.Rect(rect_left, rect_top, int_TILE_WIDTH, int_TILE_HEIGHT)
                    try:
                        pygame.draw.arc(self.screen, Color.color_wall, arc_rect, 0, pi / 2, 4)
                    except ValueError: # Bắt lỗi nếu width/height của rect < 0
                        print(f"Warning: Invalid rect for arc cell 5 at ({i},{j}): {arc_rect}")


                elif cell == 6: # Góc dưới-phải
                    # Tính toán gốc: [(j * self.TILE_WIDTH + (self.TILE_WIDTH * 0.5)), cy, self.TILE_WIDTH, self.TILE_HEIGHT]
                    # Áp dụng offset:
                    rect_left = int(draw_base_x + int_TILE_WIDTH * 0.5)
                    rect_top = int(draw_center_y)
                    arc_rect = pygame.Rect(rect_left, rect_top, int_TILE_WIDTH, int_TILE_HEIGHT)
                    try:
                        pygame.draw.arc(self.screen, Color.color_wall, arc_rect, pi / 2, pi, 4)
                    except ValueError:
                        print(f"Warning: Invalid rect for arc cell 6 at ({i},{j}): {arc_rect}")


                elif cell == 7: # Góc trên-phải
                    # Tính toán gốc: [(j * self.TILE_WIDTH + (self.TILE_WIDTH * 0.5)), (i * self.TILE_HEIGHT - (0.4 * self.TILE_HEIGHT)), self.TILE_WIDTH, self.TILE_HEIGHT]
                    # Áp dụng offset:
                    rect_left = int(draw_base_x + int_TILE_WIDTH * 0.5)
                    rect_top = int(draw_base_y - int_TILE_HEIGHT * 0.4)
                    arc_rect = pygame.Rect(rect_left, rect_top, int_TILE_WIDTH, int_TILE_HEIGHT)
                    try:
                        pygame.draw.arc(self.screen, Color.color_wall, arc_rect, pi, 3 * pi / 2, 4)
                    except ValueError:
                        print(f"Warning: Invalid rect for arc cell 7 at ({i},{j}): {arc_rect}")


                elif cell == 8: # Góc trên-trái
                    # Tính toán gốc: [(j * self.TILE_WIDTH - (self.TILE_WIDTH * 0.4)) - 2, (i * self.TILE_HEIGHT - (0.4 * self.TILE_HEIGHT)), self.TILE_WIDTH, self.TILE_HEIGHT]
                    # Áp dụng offset:
                    rect_left = int(draw_base_x - int_TILE_WIDTH * 0.4 - 2)
                    rect_top = int(draw_base_y - int_TILE_HEIGHT * 0.4)
                    arc_rect = pygame.Rect(rect_left, rect_top, int_TILE_WIDTH, int_TILE_HEIGHT)
                    try:
                        pygame.draw.arc(self.screen, Color.color_wall, arc_rect, 3 * pi / 2, 2 * pi, 4)
                    except ValueError:
                        print(f"Warning: Invalid rect for arc cell 8 at ({i},{j}): {arc_rect}")


                elif cell == 9: # fence (hàng rào - vẽ đường ngang giữa ô)
                    pygame.draw.line(self.screen, Color.color_fence,
                                    (int_base_x, int_center_y),
                                    (int_base_x + int_TILE_WIDTH, int_center_y),
                                    4)
