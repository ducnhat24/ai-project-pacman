import heapq
import tracemalloc
import gc

from utils.pathfinding_utils import is_valid, reconstruct_path  # Import from pathfinding_utils

class AStar:
    @staticmethod
    # Hàm này yêu cầu trả về đường đi từ vị trí bắt đầu đến vị trí đích
    # theo dạng danh sách các tọa độ (x, y)
    # lưu ý là tọa độ bắt đầu và đích đều là tuple (x, y)
    # giá trị trả về là một danh sách chứa các tọa độ (x, y) từ vị trí bắt đầu đến vị trí đích (nhưng không lấy vị trí bắt đầu)

    # Hàm có thể bạn sẽ cần sử dụng trong các thuật toán tìm đường:

    # pathfinding_utils.is_valid(game_map, next_pos):  # Kiểm tra xem next_pos (x, y) có hợp lệ không 
    # pathfinding_utils.reconstruct_path(came_from, start, goal):  # Trả về đường đi từ start đến goal, 
    # với giá trị truyền vào là came_from:  ghi lại các điểm mà từ đó bạn đã di chuyển đến các điểm khác trong quá trình tìm đường.
    # start: tọa độ bắt đầu (x, y)
    # goal: tọa độ đích (x, y) 

    def find_path(game_map, start, goal):
        
        
        open_set = []
        heapq.heappush(open_set, (0, start))
        
        came_from = {start: None}
        g_score = {start: 0}
        f_score = {start: AStar.heuristic(start, goal)}
        
        tracemalloc.start()
        expanded_nodes = 0

        while open_set:
            # Lấy phần tử có f_score nhỏ nhất
            #print("List node: ", open_set)

            _, current = heapq.heappop(open_set)
            expanded_nodes += 1

            if current == goal:
                break

            for neighbor in AStar.get_pos_near(current):
                if not is_valid(game_map, neighbor):
                    continue

                #print("List node: ", g_score)
                cost_g_score = g_score[current] + 1  # Chi phí di chuyển mặc định là 1

                if neighbor not in g_score or cost_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = cost_g_score
                    f_score[neighbor] = cost_g_score + AStar.heuristic(neighbor, goal)
                    heapq.heappush(open_set, (f_score[neighbor], neighbor))

        # Nếu không tìm thấy đường đi
        if goal not in came_from:
            return [start]

        path = reconstruct_path(came_from, start, goal)
        print("path", path)
        print("nodes expanded", expanded_nodes)

        current, peak_memory = tracemalloc.get_traced_memory()
        print("current ", current)
        print("peak_memory ", peak_memory)
        
        peak_memory_kb = peak_memory / (1024)  
        print('total ',  peak_memory_kb)
        tracemalloc.stop()


        return path, expanded_nodes, peak_memory_kb
    @staticmethod
    def heuristic(start, goal):
        # Sử dụng khoảng cách Manhattan
        return abs(start[0] - goal[0]) + abs(start[1] - goal[1])

    @staticmethod
    def get_pos_near(pos):
        x, y = pos
        return [
            (x + 1, y),  # phải
            (x - 1, y),  # trái
            (x, y + 1),  # xuống
            (x, y - 1)   # lên
        ]
