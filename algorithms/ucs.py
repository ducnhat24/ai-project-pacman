import heapq
import math
from utils.pathfinding_utils import is_valid  
from board_info import BoardInfo  

class UCS:
    @staticmethod
    # Hàm trả về đường đi từ vị trí bắt đầu đến vị trí đích dưới dạng danh sách các tọa độ (x, y)
    # Lưu ý: đường đi không bao gồm vị trí bắt đầu.
    def find_path(game_map, start, goal):
        path = []           # Danh sách các bước di chuyển (không bao gồm start)
        expanded_nodes_count = 0  # Số lượng các red node hợp lệ đã được duyệt
        memory = 0          # Memory usage

        # Lấy danh sách red_nodes từ BoardInfo và thêm goal nếu chưa có trong danh sách
        red_nodes = list(BoardInfo.red_nodes)
        if goal not in red_nodes:
            red_nodes.append(goal)

        # Từ điển lưu lại các node đã mở rộng cùng với chi phí đường đi của chúng
        expanded_cost = {}
        # Priority queue (min-heap): mỗi phần tử là (priority, node, path_to_node, cost_so_far)
        # Lưu ý: cost_so_far là tổng chi phí đã đi đến node đó
        heap = [(0, start, [], 0)]
        while heap:
            priority, current, current_path, cost_so_far = heapq.heappop(heap)

            # Nếu đã mở rộng current với chi phí nhỏ hơn hoặc bằng thì cập nhật lại
            if current in expanded_cost and expanded_cost[current] <= cost_so_far:
                continue

            # Lưu lại chi phí đường đi cho node này
            expanded_cost[current] = cost_so_far
            # Nếu current là red node hợp lệ, tăng số đếm expanded_nodes_count
            if current in red_nodes and is_valid(game_map, current):
                expanded_nodes_count += 1
            # Nếu đã đến đích, lưu lại path và kết thúc vòng lặp
            if current == goal:
                path = current_path
                break
            # Tính toán red_target: điểm đỏ gần current nhất theo khoảng cách Euclid
            red_target = None
            min_distance = float('inf')
            for red in red_nodes:
                d = math.sqrt((current[0] - red[0]) ** 2 + (current[1] - red[1]) ** 2)
                if d < min_distance:
                    min_distance = d
                    red_target = red

            # Duyệt các vị trí liền kề
            for neighbor in UCS.get_pos_near(current):
                if not is_valid(game_map, neighbor):
                    continue
                step_cost = math.sqrt((current[0] - neighbor[0]) ** 2 + (current[1] - neighbor[1]) ** 2)
                new_cost = cost_so_far + step_cost

                # Tính khoảng cách từ neighbor đến red_target
                if red_target is not None:
                    step= math.sqrt((neighbor[0] - red_target[0]) ** 2 + (neighbor[1] - red_target[1]) ** 2)
                else:
                    step = 0

                new_priority = new_cost + step

                # Nếu neighbor chưa được mở rộng hoặc tìm được chi phí nhỏ hơn thì thêm vào heap
                if neighbor not in expanded_cost or new_cost < expanded_cost.get(neighbor, float('inf')):
                    heapq.heappush(heap, (new_priority, neighbor, current_path + [neighbor], new_cost))

        print("path:", path)
        print("nodes expanded:", expanded_nodes_count)
        return path, expanded_nodes_count, memory

    @staticmethod
    def get_pos_near(pos):
        x, y = pos
        return [
            (x + 1, y),  # Phải
            (x - 1, y),  # Trái
            (x, y + 1),  # Xuống
            (x, y - 1)   # Lên
        ]




# import heapq
# import tracemalloc

# from utils.pathfinding_utils import is_valid, reconstruct_path  # Import from pathfinding_utils

# class UCS:
#     @staticmethod
#     # Hàm này trả về đường đi từ vị trí bắt đầu đến vị trí đích dưới dạng danh sách các tọa độ (x, y)
#     # Lưu ý: trả về không bao gồm tọa độ bắt đầu.
#     def find_path(game_map, start, goal):
#         tracemalloc.start()
        
#         open_set = []
#         heapq.heappush(open_set, (0, start))
        
#         came_from = {start: None}
#         cost_so_far = {start: 0}
        
#         expanded_nodes = 0

#         while open_set:
#             # Lấy phần tử có chi phí thấp nhất
#             current_cost, current = heapq.heappop(open_set)
#             expanded_nodes += 1

#             if current == goal:
#                 break

#             for neighbor in UCS.get_pos_near(current):
#                 if not is_valid(game_map, neighbor):
#                     continue

#                 new_cost = cost_so_far[current] + 1  # Chi phí di chuyển mặc định là 1

#                 if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
#                     cost_so_far[neighbor] = new_cost
#                     came_from[neighbor] = current
#                     heapq.heappush(open_set, (new_cost, neighbor))

#         # Nếu không tìm thấy đường đi, trả về danh sách chỉ chứa vị trí bắt đầu
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
#     def get_pos_near(pos):
#         x, y = pos
#         return [
#             (x + 1, y),  # phải
#             (x - 1, y),  # trái
#             (x, y + 1),  # xuống
#             (x, y - 1)   # lên
#         ]
