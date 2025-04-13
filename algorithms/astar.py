import heapq
import tracemalloc
from utils.pathfinding_utils import is_valid  
from board_info import BoardInfo 

class AStar:
    @staticmethod
    def calculate_cost(current, next_pos):
        """
        Tính chi phí di chuyển từ nút current đến nút next_pos.
        Nếu tung độ (y) bằng nhau: trả về |hoành độ_current - hoành độ_next|.
        Nếu hoành độ (x) bằng nhau: trả về |tung độ_current - tung độ_next|.
        """
        if current[1] == next_pos[1]:
            return abs(current[0] - next_pos[0])
        elif current[0] == next_pos[0]:
            return abs(current[1] - next_pos[1])
        return 0

    @staticmethod
    def traverse_direction(game_map, start, dx, dy, red_nodes):
        """
        Di chuyển từ nút start theo hướng (dx, dy) cho đến khi gặp nút red hoặc vị trí không hợp lệ.
        Trả về tuple (next_pos, path_segment, cost) nếu gặp được nút red, ngược lại trả về None.
        """
        current = start
        path_segment = []
        while True:
            next_pos = (current[0] + dx, current[1] + dy)
            
            if not is_valid(game_map, next_pos):
                return None
            
            path_segment.append(next_pos)
            current = next_pos
            
            if next_pos in red_nodes:
                cost = AStar.calculate_cost(start, next_pos)
                return next_pos, path_segment, cost

    @staticmethod
    def heuristic(pos, goal):
        """
        Hàm heuristic sử dụng khoảng cách Manhattan giữa pos và goal.
        Đây là hàm ước lượng dưới (admissible) với các di chuyển theo 4 hướng.
        """
        return abs(pos[0] - goal[0]) + abs(pos[1] - goal[1])

    @staticmethod
    def find_path(game_map, start, goal):
        tracemalloc.start()
        
        # Tiền xử lý: tạo tập các nút red và đảm bảo goal luôn có trong tập.
        red_nodes = set(BoardInfo.red_nodes)
        if goal not in red_nodes:
            red_nodes.add(goal)
        
        # Bổ sung: Lưu list các node đỏ và in số lượng node.
        print("Danh sách node đỏ:", list(red_nodes))
        print("Số lượng node đỏ:", len(red_nodes))
        
        # Theo dõi các nút đã mở rộng (node: chi phí tối ưu đến nó).
        expanded_nodes = {}
        expanded_red_nodes_count = 0
        
        # Nếu start là nút red, lưu thông tin chiều dài đoạn đường.
        red_nodes_with_length = {start: 0} if start in red_nodes else {}
        
        total_expanded_nodes = 0
        path = []
        
        # Hàng đợi ưu tiên của A*: (f = g + h, g, nút hiện tại, đường đi từ nút đầu)
        heap = [(AStar.heuristic(start, goal), 0, start, [])]
        
        # Các hướng di chuyển: lên, xuống, trái, phải.
        directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]
        
        while heap:
            f_val, cost_so_far, current, current_path = heapq.heappop(heap)
            
            if current in expanded_nodes and expanded_nodes[current] <= cost_so_far:
                continue
            expanded_nodes[current] = cost_so_far
            
            if current in red_nodes:
                expanded_red_nodes_count += 1
                total_expanded_nodes += red_nodes_with_length.get(current, 0)
            
            if current == goal:
                path = current_path
                break
            
            for dx, dy in directions:
                result = AStar.traverse_direction(game_map, current, dx, dy, red_nodes)
                if result:
                    next_pos, path_segment, step_cost = result
                    new_cost = cost_so_far + step_cost
                    new_f = new_cost + AStar.heuristic(next_pos, goal)
                    
                    if next_pos not in expanded_nodes or new_cost < expanded_nodes[next_pos]:
                        new_path = current_path + path_segment
                        heapq.heappush(heap, (new_f, new_cost, next_pos, new_path))
                        if next_pos not in red_nodes_with_length or len(path_segment) < red_nodes_with_length[next_pos]:
                            red_nodes_with_length[next_pos] = len(path_segment)
                            
        print("path:", path)
        print("nodes expanded:", expanded_red_nodes_count)
        print("total nodes passed:", total_expanded_nodes)
        
        current_mem, peak_memory = tracemalloc.get_traced_memory()
        print("current memory:", current_mem)
        print("peak memory:", peak_memory)
        
        peak_memory_kb = peak_memory / 1024
        tracemalloc.stop()
        
        return path, total_expanded_nodes, peak_memory_kb





























# import heapq
# import tracemalloc
# import gc

# from utils.pathfinding_utils import is_valid, reconstruct_path  # Import from pathfinding_utils

# class AStar:
#     @staticmethod
#     # Hàm này yêu cầu trả về đường đi từ vị trí bắt đầu đến vị trí đích
#     # theo dạng danh sách các tọa độ (x, y)
#     # lưu ý là tọa độ bắt đầu và đích đều là tuple (x, y)
#     # giá trị trả về là một danh sách chứa các tọa độ (x, y) từ vị trí bắt đầu đến vị trí đích (nhưng không lấy vị trí bắt đầu)

#     # Hàm có thể bạn sẽ cần sử dụng trong các thuật toán tìm đường:

#     # pathfinding_utils.is_valid(game_map, next_pos):  # Kiểm tra xem next_pos (x, y) có hợp lệ không 
#     # pathfinding_utils.reconstruct_path(came_from, start, goal):  # Trả về đường đi từ start đến goal, 
#     # với giá trị truyền vào là came_from:  ghi lại các điểm mà từ đó bạn đã di chuyển đến các điểm khác trong quá trình tìm đường.
#     # start: tọa độ bắt đầu (x, y)
#     # goal: tọa độ đích (x, y) 

#     def find_path(game_map, start, goal):
#         tracemalloc.start()

#         open_set = []
#         heapq.heappush(open_set, (0, start))
        
#         came_from = {start: None}
#         g_score = {start: 0}
#         f_score = {start: AStar.heuristic(start, goal)}
        
#         expanded_nodes = 0

#         while open_set:
#             # Lấy phần tử có f_score nhỏ nhất
#             #print("List node: ", open_set)

#             _, current = heapq.heappop(open_set)
#             expanded_nodes += 1

#             if current == goal:
#                 break

#             for neighbor in AStar.get_pos_near(current):
#                 if not is_valid(game_map, neighbor):
#                     continue

#                 #print("List node: ", g_score)
#                 cost_g_score = g_score[current] + 1  # Chi phí di chuyển mặc định là 1

#                 if neighbor not in g_score or cost_g_score < g_score[neighbor]:
#                     came_from[neighbor] = current
#                     g_score[neighbor] = cost_g_score
#                     f_score[neighbor] = cost_g_score + AStar.heuristic(neighbor, goal)
#                     heapq.heappush(open_set, (f_score[neighbor], neighbor))

#         # Nếu không tìm thấy đường đi
#         if goal not in came_from:
#             return [start]

#         path = reconstruct_path(came_from, start, goal)
#         print("path", path)
#         print("nodes expanded", expanded_nodes)

#         current, peak_memory = tracemalloc.get_traced_memory()
#         print("current ", current)
#         print("peak_memory ", peak_memory)
        
#         peak_memory_kb = peak_memory / (1024)  
#         tracemalloc.stop()


#         return path, expanded_nodes, peak_memory_kb
#     @staticmethod
#     def heuristic(start, goal):
#         # Sử dụng khoảng cách Manhattan
#         return abs(start[0] - goal[0]) + abs(start[1] - goal[1])

#     @staticmethod
#     def get_pos_near(pos):
#         x, y = pos
#         return [
#             (x + 1, y),  # phải
#             (x - 1, y),  # trái
#             (x, y + 1),  # xuống
#             (x, y - 1)   # lên
#         ]
