from time import sleep
import pygame
from entities.entity import Entity
from maze_drawing import MazeDrawing
from utils.pathfinding import PathFinding

class Ghost(Entity):
    def __init__(self, x, y, game_map, ghost_type, color):
        # Gọi constructor của Entity
        super().__init__(x, y, game_map)
        
        self.ghost_type = ghost_type
        self.color = color
        self.images = {
            "FACE": pygame.image.load(f"assets/images/ingame/{self.color}-ghost-face.png"),
            "BACK": pygame.image.load(f"assets/images/ingame/{self.color}-ghost-back.png"),
            "LEFT": pygame.image.load(f"assets/images/ingame/{self.color}-ghost-left.png"),
            "RIGHT": pygame.image.load(f"assets/images/ingame/{self.color}-ghost-right.png")
        }
        self.current_image = self.images["FACE"]  # Hình ảnh mặc định khi đứng yên
        self.path = []
        self.initial_position = (x, y)  # Lưu lại vị trí ban đầu của Ghost
        self.maze_drawing = MazeDrawing(self.game_map)
        self.direction = "FACE"  # Hướng di chuyển mặc định

    def move(self, pacman_x, pacman_y):
        """ Gọi PathFinding để tìm đường cho từng ghost """
        self.path = PathFinding.find_path(self.game_map, (self.x, self.y), (pacman_x, pacman_y), self.ghost_type)

    def follow_path(self):
        """ Di chuyển theo đường tìm được """
        if self.path:
            next_pos = self.path.pop(0)
            new_x, new_y = next_pos
            self.update_image()  # Cập nhật hình ảnh của Ghost theo hướng di chuyển
            self.update_direction(new_x, new_y)  # Cập nhật hướng di chuyển ngay sau khi di chuyển
            self.x, self.y = new_x, new_y

            sleep(0.3)  # Thời gian nghỉ giữa các bước di chuyển

    def update_direction(self, new_x, new_y):
        """ Cập nhật hướng di chuyển của Ghost """
        print(f"Update direction: ({self.x}, {self.y}) -> ({new_x}, {new_y})")  # Debug hướng di chuyển
        if new_x < self.x:
            self.direction = "LEFT"
        elif new_x > self.x:
            self.direction = "RIGHT"
        elif new_y < self.y:
            self.direction = "UP"
        elif new_y > self.y:
            self.direction = "DOWN"

    def update_image(self):
        """ Cập nhật hình ảnh của Ghost theo hướng di chuyển """
        if self.direction == "LEFT":
            self.current_image = self.images["LEFT"]
        elif self.direction == "RIGHT":
            self.current_image = self.images["RIGHT"]
        elif self.direction == "UP":
            self.current_image = self.images["BACK"]
        elif self.direction == "DOWN":
            self.current_image = self.images["FACE"]

    def respawn(self):
        """ Đưa Ghost về vị trí ban đầu khi chết """
        self.x, self.y = self.initial_position

    def draw(self, screen, tile_size):
        """ Vẽ Ghost lên màn hình """
        offset_x = self.maze_drawing.offset_x
        offset_y = self.maze_drawing.offset_y

        scaled_image = pygame.transform.scale(self.current_image, (tile_size, tile_size))
        
        draw_x = self.x * tile_size + offset_x  
        draw_y = self.y * tile_size + offset_y  
        
        screen.blit(scaled_image, (draw_x, draw_y))
