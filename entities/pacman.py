
import pygame
from entities.entity import Entity
from maze_drawing import MazeDrawing
from settings import Config

class Pacman(Entity):
    def __init__(self, x, y, game_map):
        # Gọi constructor của Entity
        super().__init__(x, y, game_map)
        self.images = {
            "LEFT": pygame.image.load("assets/images/ingame/pacman-left.png"),
            "RIGHT": pygame.image.load("assets/images/ingame/pacman-right.png"),
            "UP": pygame.image.load("assets/images/ingame/pacman-back.png"),
            "DOWN": pygame.image.load("assets/images/ingame/pacman-face.png"),
            "EAT_LEFT": pygame.image.load("assets/images/ingame/pacman-eat-left.png"),
            "EAT_RIGHT": pygame.image.load("assets/images/ingame/pacman-eat-right.png")
        }
        self.current_image = self.images["RIGHT"]
        self.direction = "RIGHT"
        self.maze_drawing = MazeDrawing(self.game_map)  # Khởi tạo đối tượng MazeDrawing
        self.current_dx = 0 # Hướng đi hiện tại của pacman dx
        self.current_dy = 1 # Hướng đi hiện tại của pacman dy
    
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
            self.x = new_x
            self.y = new_y
            self.current_dx = dx  # Cập nhật hướng
            self.current_dy = dy
            self.update_direction(dx, dy)
            self.update_image()  # Cập nhật hình ảnh theo hướng di chuyển

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
        offset_x = self.maze_drawing.offset_x
        offset_y = self.maze_drawing.offset_y

        tile_width = Config.TILE_WIDTH
        tile_height = Config.TILE_HEIGHT

        scaled_image = pygame.transform.scale(self.current_image, (tile_height, tile_width))
        
        draw_x = self.y * tile_size + offset_x
        draw_y = self.x * tile_size + offset_y
        
        # Render Pacman on the screen at the correct position
        screen.blit(scaled_image, (draw_x, draw_y))