import heapq
import tracemalloc

from utils.pathfinding_utils import is_valid, reconstruct_path  # Import from pathfinding_utils

class UCS:
    @staticmethod
    # Hàm này trả về đường đi từ vị trí bắt đầu đến vị trí đích dưới dạng danh sách các tọa độ (x, y)
    # Lưu ý: trả về không bao gồm tọa độ bắt đầu.
    def find_path(game_map, start, goal):
        tracemalloc.start()
        
        open_set = []
        heapq.heappush(open_set, (0, start))
        
        came_from = {start: None}
        cost_so_far = {start: 0}
        
        expanded_nodes = 0

        while open_set:
            # Lấy phần tử có chi phí thấp nhất
            current_cost, current = heapq.heappop(open_set)
            expanded_nodes += 1

            if current == goal:
                break

            for neighbor in UCS.get_pos_near(current):
                if not is_valid(game_map, neighbor):
                    continue

                new_cost = cost_so_far[current] + 1  # Chi phí di chuyển mặc định là 1

                if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                    cost_so_far[neighbor] = new_cost
                    came_from[neighbor] = current
                    heapq.heappush(open_set, (new_cost, neighbor))

        # Nếu không tìm thấy đường đi, trả về danh sách chỉ chứa vị trí bắt đầu
        if goal not in came_from:
            return [start]

        path = reconstruct_path(came_from, start, goal)
        print("path", path)
        print("nodes expanded", expanded_nodes)

        current, peak_memory = tracemalloc.get_traced_memory()
        print("current ", current)
        print("peak_memory ", peak_memory)

        peak_memory_kb = peak_memory / (1024)  
        tracemalloc.stop()

        return path, expanded_nodes, peak_memory_kb

    @staticmethod
    def get_pos_near(pos):
        x, y = pos
        return [
            (x + 1, y),  # phải
            (x - 1, y),  # trái
            (x, y + 1),  # xuống
            (x, y - 1)   # lên
        ]
