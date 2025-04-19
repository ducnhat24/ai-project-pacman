from time import sleep
import time
import pygame
from entities.entity import Entity
from maze_drawing import MazeDrawing
from settings import Config
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
        self.path_update_interval = 20  # Cập nhật lại sau mỗi path_update_interval bước
        self.total_expanded_nodes = 0

        self.target_pacman_x = target_pacman_x
        self.target_pacman_y = target_pacman_y

        # Đánh dấu ghost ở trên map
        map[y][x] = 10
        self.time_out = 5
        self.random_direction = False

        

        self.real_x = x * Config.TILE_WIDTH
        self.real_y = y * Config.TILE_HEIGHT
        self.start_pos = (x, y)
        self.end_pos = (x, y)
        self.moving = False
        self.move_progress = 0.0
        self.move_duration = 120  # hoặc giống pacman
        self.last_move_time = pygame.time.get_ticks()



    def move(self, pacman_x, pacman_y):
        self.target_pacman_x = pacman_x
        self.target_pacman_y = pacman_y
        if self.pathfinding_thread is None or not self.pathfinding_thread.is_alive():
            self.path_ready = False
            self.pathfinding_thread = threading.Thread(
                target=self.async_find_path, args=(pacman_y, pacman_x)
            )
            self.pathfinding_thread.start()


    def async_find_path(self, target_y, target_x):
        start_time = time.time()
        path, expanded_nodes, memory = PathFinding.find_path(
            self.game_map, (self.x, self.y), (target_x, target_y), self.ghost_type, self.random_direction
        )
        # self.path = path
        # self.expanded_nodes += expanded_nodes
        # self.path_ready = True
        end_time = time.time()
        time_algorithm = end_time - start_time

        print("time_algorithm ", time_algorithm)
        print(self.ghost_type, " use memory ", memory)

        self.total_expanded_nodes += expanded_nodes
        self.memory += memory
        self.total_time += time_algorithm
        self.path = path
        self.expanded_nodes = expanded_nodes  # Cập nhật expanded_nodes với giá trị của lần tìm đường hiện tại
        self.path_ready = True
        self.random_direction = False

    def follow_path(self, pacman_x, pacman_y, map, lock): 
        # Kiểm tra xem pacman đã di chuyển chưa và cập nhật đường đi nếu cần
        if (self.level_id == 6 and 
            (self.target_pacman_x != pacman_x or self.target_pacman_y != pacman_y) and
            self.steps_since_last_path_update >= self.path_update_interval):
            print(f"Pacman moved from ({self.target_pacman_x}, {self.target_pacman_y}) to ({pacman_x}, {pacman_y}). Finding new path...")
            self.move(pacman_x, pacman_y)
            self.steps_since_last_path_update = 0
            return  # Đợi đường đi mới được tính toán

        if self.path_ready and self.path and len(self.path) > 0 and not self.moving:
            next_pos = self.path[0]
            new_x, new_y = next_pos
            with lock:
                if map[new_y][new_x] != 10:
                    self.path.pop(0)
                    map[self.y][self.x] = 1  

                    # Update direction based on where we're going
                    self.update_direction(new_x, new_y)
                    self.update_image()

                    # Mark the starting position for animation
                    self.start_pos = (self.x, self.y)
                    # Set the destination
                    self.end_pos = (new_x, new_y) 
                    
                    # Update map with new position
                    map[new_y][new_x] = 10
                    
                    # Start movement animation
                    self.moving = True
                    self.move_progress = 0.0
                    self.last_move_time = pygame.time.get_ticks()

                    self.time_out = 5
                else:
                    self.time_out -= 1
        elif not self.moving and (not self.path_ready or not self.path or len(self.path) == 0):
            self.move(pacman_x, pacman_y)
        if self.time_out < 0:
            self.random_direction = True
            self.move(pacman_x, pacman_y)

    # def follow_path(self, pacman_x, pacman_y, map, lock): 
    #     if self.path_ready and self.path and len(self.path) > 0 and not self.moving:
    #         next_pos = self.path[0]
    #         new_x, new_y = next_pos
    #         with lock:
    #             if map[new_y][new_x] != 10:
    #                 self.path.pop(0)
    #                 map[self.y][self.x] = 1  

    #                 # Update direction based on where we're going
    #                 self.update_direction(new_x, new_y)
    #                 self.update_image()

    #                 # Mark the starting position for animation
    #                 self.start_pos = (self.x, self.y)
    #                 # Set the destination
    #                 self.end_pos = (new_x, new_y) 
                    
    #                 # Update map with new position
    #                 map[new_y][new_x] = 10
                    
    #                 # Start movement animation
    #                 self.moving = True
    #                 self.move_progress = 0.0
    #                 self.last_move_time = pygame.time.get_ticks()

                    

    #                 if (
    #                     self.level_id == 6
    #                     and self.steps_since_last_path_update >= self.path_update_interval
    #                     and (self.target_pacman_x != pacman_x or self.target_pacman_y != pacman_y)
    #                 ):
    #                     self.move(pacman_x, pacman_y)
    #                     self.steps_since_last_path_update = 0
    #     elif not self.moving and (not self.path_ready or not self.path or len(self.path) == 0):
    #         self.move(pacman_x, pacman_y)

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


    def update(self):
        if self.moving:
            current_time = pygame.time.get_ticks()
            elapsed = current_time - self.last_move_time
            self.move_progress = min(1.0, elapsed / self.move_duration)

            start_x, start_y = self.start_pos
            end_x, end_y = self.end_pos

            # Calculate real pixel position for smooth movement
            self.real_x = (start_x + (end_x - start_x) * self.move_progress) * Config.TILE_WIDTH
            self.real_y = (start_y + (end_y - start_y) * self.move_progress) * Config.TILE_HEIGHT

            if self.move_progress >= 1.0:
                self.moving = False
                self.steps_since_last_path_update += 1

                self.x, self.y = self.end_pos  # Only update grid position after animation completes
                self.real_x = self.x * Config.TILE_WIDTH
                self.real_y = self.y * Config.TILE_HEIGHT


    def respawn(self):
        """ Đưa Ghost về vị trí ban đầu khi chết """
        self.x, self.y = self.initial_position

    def draw(self, screen, tile_size):
        """Vẽ Ghost lên màn hình"""
        offset_x = MazeDrawing._offset_x
        offset_y = MazeDrawing._offset_y

        scaled_image = pygame.transform.scale(self.current_image, (tile_size, tile_size))
        
        draw_x = self.real_x + offset_x  
        draw_y = self.real_y + offset_y  
        # Uncomment for debugging only when needed
        # print("Drawing ghost at: ", draw_x, draw_y)
        screen.blit(scaled_image, (draw_x, draw_y))