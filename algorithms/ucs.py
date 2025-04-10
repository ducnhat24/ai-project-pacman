import heapq
from utils.pathfinding_utils import is_valid  # Giữ lại nếu cần kiểm tra vị trí hợp lệ
from board_info import BoardInfo  # Import class BoardInfo và truy cập đến danh sách red_nodes

class UCS:
    @staticmethod
    # Hàm trả về đường đi từ vị trí bắt đầu đến vị trí đích dưới dạng danh sách các tọa độ (x, y)
    # Lưu ý: đường đi không bao gồm vị trí bắt đầu.
    def find_path(game_map, start, goal):
        path = []           # Danh sách các bước di chuyển (không bao gồm start)
        expanded_nodes = 0  # Số lượng các red node đã được duyệt
        memory = 0          # Memory usage

        # Lưu ý: Ta làm việc với một bản sao của danh sách red_nodes để không thay đổi dữ liệu gốc trong BoardInfo.
        red_nodes = list(BoardInfo.red_nodes)

        # Nếu goal không nằm trong red_nodes thì có thể thêm vào danh sách này để đảm bảo luôn có thể nhận diện mục tiêu.
        if goal not in red_nodes:
            red_nodes.append(goal)

        # Priority queue (min-heap): mỗi phần tử là (cost, node, path_to_node)
        heap = [(0, start, [])]
        visited = set()

        while heap:
            cost, current, current_path = heapq.heappop(heap)

            if current in visited:
                continue
            visited.add(current)

            # Nếu là red node hợp lệ, tăng số lượng expanded_nodes
            if current in red_nodes and is_valid(game_map, current):
                expanded_nodes += 1

            # Nếu đã đến đích
            if current == goal:
                path = current_path
                break

            # Duyệt các vị trí liền kề
            for neighbor in UCS.get_pos_near(current):
                if neighbor in visited:
                    continue
                if is_valid(game_map, neighbor):
                    heapq.heappush(heap, (cost + 1, neighbor, current_path + [neighbor]))

        print("path:", path)
        print("nodes expanded:", expanded_nodes)
        return path, expanded_nodes, memory

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
