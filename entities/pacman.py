
import pygame
from entities.entity import Entity
from maze.maze_drawing import MazeDrawing
from scene_manager import SceneManager
from settings import Config
from utils.sounds import Sounds
class Pacman(Entity):
    _score = 0  # Điểm số của pacman
    def __init__(self, x, y, game_map):
        # Gọi constructor của Entity
        super().__init__(x, y, game_map)
        
        self.real_x = y * Config.TILE_WIDTH  # pixel, lưu ý y trước vì là cột
        self.real_y = x * Config.TILE_HEIGHT  # pixel
        self.moving = False
        self.move_progress = 0.0
        self.move_duration = 120  # thời gian để di chuyển một ô, tính bằng milliseconds
        self.start_pos = (x, y)
        self.end_pos = (x, y)
        
        self.current_dx = 0 # Hướng đi hiện tại của pacman dx
        self.current_dy = 1 # Hướng đi hiện tại của pacman dy
        self.next_direction = (0, 0)  # Hướng tiếp theo được người chơi nhấn
        self.scene_manager = SceneManager()

        def scale_image(image):
            return pygame.transform.scale(image, (Config.TILE_HEIGHT, Config.TILE_WIDTH)).convert_alpha()

        self.images = {
            "LEFT": scale_image(pygame.image.load("assets/images/ingame/pacman-left.png")),
            "RIGHT": scale_image(pygame.image.load("assets/images/ingame/pacman-right.png")),
            "UP": scale_image(pygame.image.load("assets/images/ingame/pacman-back.png")),
            "DOWN": scale_image(pygame.image.load("assets/images/ingame/pacman-face.png")),
            "EAT_LEFT": scale_image(pygame.image.load("assets/images/ingame/pacman-eat-left.png")),
            "EAT_RIGHT": scale_image(pygame.image.load("assets/images/ingame/pacman-eat-right.png"))
        }

        self.current_image = self.images["RIGHT"]
        self.direction = "RIGHT"

        self.sounds = Sounds()

    def set_next_direction(self, dx, dy):
        self.next_direction = (dx, dy)

    def continue_moving(self):
        """Tiếp tục di chuyển nếu không gặp tường"""
        new_x = self.x + self.current_dx
        new_y = self.y + self.current_dy
        if self.can_move(new_x, new_y):
            self.move(self.current_dx, self.current_dy)


    def move(self, dx, dy):
        """ Di chuyển Pac-Man nếu không va vào tường """
        new_x = self.x + dx
        new_y = self.y + dy
        if self.can_move(new_x, new_y):  # Kiểm tra va chạm
            self.start_pos = (self.x, self.y)
            self.end_pos = (new_x, new_y)

            self.x = new_x
            self.y = new_y
            self.moving = True  # Đánh dấu là đang di chuyển
            self.move_progress = 0.0
            self.last_move_time = pygame.time.get_ticks()
        

            self.current_dx = dx  # Cập nhật hướng
            self.current_dy = dy
            self.update_direction(dx, dy)
            self.update_image()  # Cập nhật hình ảnh theo hướng di chuyển

    def update(self):
        """ Xử lý di chuyển mỗi frame, ưu tiên hướng tiếp theo """
        current_time = pygame.time.get_ticks()
        if self.moving:
            elapsed = current_time - self.last_move_time
            self.move_progress = min(1.0, elapsed / self.move_duration)  # Tăng tiến độ di chuyển
            old_x, old_y = self.start_pos

            if self.move_progress == 1.0:
                self.moving = False
                # self.move_progress = 0.0  # Reset tiến độ di chuyển
                self.real_x = self.end_pos[1] * Config.TILE_WIDTH  # Cập nhật vị trí thực tế
                self.real_y = self.end_pos[0] * Config.TILE_HEIGHT  # Cập nhật vị trí thực tế
            
            elif 0 < self.move_progress < 1 and MazeDrawing._shared_map[old_x][old_y] == 1:
                MazeDrawing._shared_map[old_x][old_y] = 0  # Đặt lại ô cũ thành tường
                self._score += 1  # Tăng điểm số
                self.sounds.play_sound("pacman_eat")

        else:
            next_dx, next_dy = self.next_direction
            new_x = self.x + next_dx
            new_y = self.y + next_dy
            if self.can_move(new_x, new_y):
                self.move(next_dx, next_dy)
            else:
                self.continue_moving()

    def update_direction(self, dx, dy):
        """ Cập nhật hướng di chuyển """
        if dx == -1:
            self.direction = "UP"
        elif dx == 1:
            self.direction = "DOWN"
        elif dy == -1:
            self.direction = "LEFT"
        elif dy == 1:
            self.direction = "RIGHT"

    def update_image(self):
        """ Cập nhật hình ảnh của Pacman theo hướng di chuyển """
        if self.direction == "LEFT":
            self.current_image = self.images["LEFT"]
        elif self.direction == "RIGHT":
            self.current_image = self.images["RIGHT"]
        elif self.direction == "UP":
            self.current_image = self.images["UP"]
        elif self.direction == "DOWN":
            self.current_image = self.images["DOWN"]

    def draw(self, screen, tile_size):
        """ Vẽ Pacman lên màn hình """
        offset_x = MazeDrawing._offset_x
        offset_y = MazeDrawing._offset_y

        tile_width = Config.TILE_WIDTH
        tile_height = Config.TILE_HEIGHT

        start_px = self.start_pos[1] * tile_width
        start_py = self.start_pos[0] * tile_height
        end_px = self.end_pos[1] * tile_width
        end_py = self.end_pos[0] * tile_height

        
        # draw_x = self.y * tile_size + offset_x
        # draw_y = self.x * tile_size + offset_y

        draw_x = start_px + (end_px - start_px) * self.move_progress + offset_x
        draw_y = start_py + (end_py - start_py) * self.move_progress + offset_y
        
        
        scaled_image = pygame.transform.scale(self.current_image, (tile_height, tile_width))
        screen.blit(scaled_image, (draw_x, draw_y))