import copy
import pygame
from math import pi
from settings import Config, Color
from maze.board_info import BoardInfo
from settings import Config, Color

class MazeDrawing:
    TILE_WIDTH = Config.TILE_WIDTH
    TILE_HEIGHT = Config.TILE_HEIGHT
    _shared_map = None  # singleton map
    _offset_x = (Config.SCREEN_WIDTH - 60 * TILE_WIDTH) // 2
    _offset_y = 10


    def __init__(self, screen):
        self.screen = screen
        self.board = BoardInfo()
        if MazeDrawing._shared_map is None:
            MazeDrawing._shared_map = copy.deepcopy(self.board.game_map)
        self.map = MazeDrawing._shared_map
        
        # Define shadow color
        self.shadow_color = (50, 50, 50, 128)
        
        # Check xem map có rỗng không
        if not self.map:
            return
        self.num_rows = len(self.map)
        if self.num_rows == 0 or not self.map[0]: 
            return
        self.num_cols = len(self.map[0])
        
        total_map_width_px = self.num_cols * self.TILE_WIDTH
        total_map_height_px = self.num_rows * self.TILE_HEIGHT

        screen_width = Config.SCREEN_WIDTH
        screen_height = Config.SCREEN_HEIGHT

        self.offset_x = (Config.SCREEN_WIDTH - 60 * self.TILE_WIDTH) // 2
        self.offset_y = 10

    def draw_rounded_line(self, surface, color, start_pos, end_pos, width, shadow=False):
        if shadow:
            # Draw shadow first
            shadow_color = self.shadow_color
            shadow_offset = 2
            pygame.draw.line(surface, shadow_color, 
                           (start_pos[0] + shadow_offset, start_pos[1] + shadow_offset),
                           (end_pos[0] + shadow_offset, end_pos[1] + shadow_offset),
                           width)
        
        # Draw main line
        pygame.draw.line(surface, color, start_pos, end_pos, width)
        
        # Draw rounded caps
        pygame.draw.circle(surface, color, start_pos, width//2)
        pygame.draw.circle(surface, color, end_pos, width//2)

    def draw_rounded_arc(self, surface, color, rect, start_angle, end_angle, width, shadow=False):
        if shadow:
            # Draw shadow first
            shadow_color = self.shadow_color
            shadow_offset = 2
            shadow_rect = pygame.Rect(rect.x + shadow_offset, rect.y + shadow_offset, 
                                    rect.width, rect.height)
            pygame.draw.arc(surface, shadow_color, shadow_rect, start_angle, end_angle, width)
        
        # Draw main arc
        pygame.draw.arc(surface, color, rect, start_angle, end_angle, width)

    def draw(self):
        # --- Vòng lặp vẽ từng ô, áp dụng offset ---
        for i in range(self.num_rows):
            for j in range(self.num_cols):
                cell = MazeDrawing._shared_map[i][j]

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
                    # Draw glow effect
                    for radius in range(3, 1, -1):  # Giảm kích thước glow effect
                        alpha = int(255 * (1 - (radius - 1) / 2))  # Điều chỉnh alpha cho glow effect nhỏ hơn
                        color = (*Color.color_food[:3], alpha)
                        pygame.draw.circle(self.screen, color, (int_center_x, int_center_y), radius)
                    # Draw main dot
                    pygame.draw.circle(self.screen, Color.color_food, (int_center_x, int_center_y), 1)  # Giảm kích thước dot chính

                elif cell == 2: # power food
                    # Draw glow effect
                    for radius in range(6, 4, -1):  # Giảm kích thước glow effect
                        alpha = int(255 * (1 - (radius - 4) / 2))  # Điều chỉnh alpha cho glow effect nhỏ hơn
                        color = (*Color.color_power_food[:3], alpha)
                        pygame.draw.circle(self.screen, color, (int_center_x, int_center_y), radius)
                    # Draw main dot
                    pygame.draw.circle(self.screen, Color.color_power_food, (int_center_x, int_center_y), 4)  # Giảm kích thước dot chính

                elif cell == 3: # vertical wall
                    self.draw_rounded_line(self.screen, Color.color_wall,
                                        (int_center_x, int_base_y),
                                        (int_center_x, int_base_y + int_TILE_HEIGHT),
                                        6, shadow=True)

                elif cell == 4: # horizontal wall
                    self.draw_rounded_line(self.screen, Color.color_wall,
                                        (int_base_x, int_center_y),
                                        (int_base_x + int_TILE_WIDTH, int_center_y),
                                        6, shadow=True)

                elif cell == 5: # Góc trên-phải
                    rect_left = int(draw_base_x - int_TILE_WIDTH * 0.4 - 2)
                    rect_top = int(draw_center_y)
                    arc_rect = pygame.Rect(rect_left, rect_top, int_TILE_WIDTH, int_TILE_HEIGHT)
                    try:
                        self.draw_rounded_arc(self.screen, Color.color_wall, arc_rect, 0, pi / 2, 6, shadow=True)
                    except ValueError:
                        print(f"Warning: Invalid rect for arc cell 5 at ({i},{j}): {arc_rect}")

                elif cell == 6: # Góc trên-trái
                    rect_left = int(draw_base_x + int_TILE_WIDTH * 0.5)
                    rect_top = int(draw_center_y)
                    arc_rect = pygame.Rect(rect_left, rect_top, int_TILE_WIDTH, int_TILE_HEIGHT)
                    try:
                        self.draw_rounded_arc(self.screen, Color.color_wall, arc_rect, pi / 2, pi, 6, shadow=True)
                    except ValueError:
                        print(f"Warning: Invalid rect for arc cell 6 at ({i},{j}): {arc_rect}")

                elif cell == 7: # Góc dưới-trái
                    rect_left = int(draw_base_x + int_TILE_WIDTH * 0.5)
                    rect_top = int(draw_base_y - int_TILE_HEIGHT * 0.4)
                    arc_rect = pygame.Rect(rect_left, rect_top, int_TILE_WIDTH, int_TILE_HEIGHT)
                    try:
                        self.draw_rounded_arc(self.screen, Color.color_wall, arc_rect, pi, 3 * pi / 2, 6, shadow=True)
                    except ValueError:
                        print(f"Warning: Invalid rect for arc cell 7 at ({i},{j}): {arc_rect}")

                elif cell == 8: # Góc dưới-phải
                    rect_left = int(draw_base_x - int_TILE_WIDTH * 0.4 - 2)
                    rect_top = int(draw_base_y - int_TILE_HEIGHT * 0.4)
                    arc_rect = pygame.Rect(rect_left, rect_top, int_TILE_WIDTH, int_TILE_HEIGHT)
                    try:
                        self.draw_rounded_arc(self.screen, Color.color_wall, arc_rect, 3 * pi / 2, 2 * pi, 6, shadow=True)
                    except ValueError:
                        print(f"Warning: Invalid rect for arc cell 8 at ({i},{j}): {arc_rect}")

                elif cell == 9: # fence
                    self.draw_rounded_line(self.screen, Color.color_fence,
                                        (int_base_x, int_center_y),
                                        (int_base_x + int_TILE_WIDTH, int_center_y),
                                        4, shadow=True)
