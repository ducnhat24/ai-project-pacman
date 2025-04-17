from time import sleep
import time
import pygame
from entities.entity import Entity
from maze_drawing import MazeDrawing
from utils.pathfinding import PathFinding
import threading
import tracemalloc


class Ghost(Entity):
    def __init__(self, x, y, game_map, ghost_type, color, target_pacman_x, target_pacman_y, map, level_id = 1):
        # Gọi constructor của Entity
        super().__init__(x, y, game_map)
        self.level_id = level_id  # ID của level hiện tại
        self.id = None
        self.total_time = 0
        self.memory = 0
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
        self.pathfinding_thread = None
        self.path_ready = False

        self.expanded_nodes = 0

        self.initial_position = (x, y)  # Lưu lại vị trí ban đầu của Ghost
        self.direction = "FACE"  # Hướng di chuyển mặc định
        self.steps_since_last_path_update = 0
        self.path_update_interval = 40  # Cập nhật lại sau mỗi path_update_interval bước
        self.total_expanded_nodes = 0

        self.target_pacman_x = target_pacman_x
        self.target_pacman_y = target_pacman_y

        # Đánh dấu ghost ở trên map
        map[y][x] = 10


    def move(self, pacman_x, pacman_y):
        if self.pathfinding_thread is None or not self.pathfinding_thread.is_alive():
            self.path_ready = False
            self.pathfinding_thread = threading.Thread(
                target=self.async_find_path, args=(pacman_y, pacman_x)
            )
            self.pathfinding_thread.start()


    def async_find_path(self, target_y, target_x):
        start_time = time.time()
        path, expanded_nodes, memory = PathFinding.find_path(
            self.game_map, (self.x, self.y), (target_x, target_y), self.ghost_type
        )
        # self.path = path
        # self.expanded_nodes += expanded_nodes
        # self.path_ready = True
        end_time = time.time()
        total_time = end_time - start_time

        print("total_time ", total_time)
        print(self.ghost_type, " use memory ", memory)

        self.total_expanded_nodes += expanded_nodes
        self.memory += memory
        self.total_time += total_time
        self.path = path
        self.expanded_nodes = expanded_nodes  # Cập nhật expanded_nodes với giá trị của lần tìm đường hiện tại
        self.path_ready = True



    def follow_path(self, pacman_x, pacman_y, map): 
        # print(map)
        """ Di chuyển theo đường tìm được và tự cập nhật lại đường đi nếu cần """
        if self.path_ready and self.path:
            next_pos = self.path[0]
            new_x, new_y = next_pos
            if (map[new_y][new_x] != 10):
                self.path.pop(0)
                map[self.y][self.x] = 1
                self.update_direction(new_x, new_y)
                self.x, self.y = new_x, new_y
                self.update_image()
                map[self.y][self.x] = 10

                self.steps_since_last_path_update += 1

                if self.level_id == 6 and self.steps_since_last_path_update >= self.path_update_interval and self.target_pacman_x != pacman_x and self.target_pacman_y != pacman_y:
                    self.move(pacman_x, pacman_y)
                    self.steps_since_last_path_update = 0

                # sleep(0.01)
        else:
            # Nếu chưa có đường hoặc path chưa sẵn sàng => bắt đầu tìm
            self.move(pacman_x, pacman_y)

    def update_direction(self, new_x, new_y):
        """ Cập nhật hướng di chuyển của Ghost """
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
        offset_x = MazeDrawing._offset_x
        offset_y = MazeDrawing._offset_y

        scaled_image = pygame.transform.scale(self.current_image, (tile_size, tile_size))
        
        draw_x = self.x * tile_size + offset_x  
        draw_y = self.y * tile_size + offset_y  
        
        screen.blit(scaled_image, (draw_x, draw_y))
