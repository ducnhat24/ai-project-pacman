import heapq
import math
from utils.pathfinding_utils import is_valid  
from board_info import BoardInfo 


class UCS:
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
            # Tính vị trí tiếp theo theo hướng cho trước
            next_pos = (current[0] + dx, current[1] + dy)
            
            if not is_valid(game_map, next_pos):
                # Nếu vị trí không hợp lệ thì dừng và trả về None
                return None
            
            path_segment.append(next_pos)
            # Cập nhật current cho lần duyệt tiếp theo
            current = next_pos
            
            # Nếu gặp nút red, tính chi phí và trả về thông tin
            if next_pos in red_nodes:
                cost = UCS.calculate_cost(start, next_pos)
                return next_pos, path_segment, cost

    @staticmethod
    def find_path(game_map, start, goal):
        path = []           # Danh sách các bước di chuyển (không bao gồm start)
        expanded_nodes_count = 0  
        memory = 0         
        red_nodes = list(BoardInfo.red_nodes)
        if goal not in red_nodes:
            red_nodes.append(goal)

        # Từ điển lưu lại các node đã mở rộng cùng với chi phí đường đi của chúng
        expanded_cost = {}
        # Priority queue (min-heap): mỗi phần tử là (priority, node, path_to_node, cost_so_far)
        # Lưu ý: cost_so_far là tổng chi phí đã đi đến node đó
        heap = [(0, start, [], 0)]
        memory = max(memory, len(heap))
        
        while heap:
            cost_so_far, current, current_path = heapq.heappop(heap)
            
            # Nếu đã có đường đi tốt hơn đến nút này thì bỏ qua
            if current in expanded_nodes and expanded_nodes[current] <= cost_so_far:
                continue
                
            expanded_nodes[current] = cost_so_far
            
            # Cập nhật số nút red được mở rộng và số nút đi qua (dựa trên độ dài của đoạn đường đi)
            if current in red_nodes:
                expanded_red_nodes_count += 1
                total_expanded_nodes += red_nodes_with_length.get(current, 0)
                
            # Nếu đã đến đích thì kết thúc
            if current == goal:
                path = current_path
                break

            # Duyệt các vị trí liền kề
            for neighbor in UCS.get_pos_near(current):
                if not is_valid(game_map, neighbor):
                    continue

                # Chi phí bước đi: khoảng cách Euclid giữa current và neighbor
                step_cost = math.sqrt((current[0] - neighbor[0]) ** 2 + (current[1] - neighbor[1]) ** 2)
                new_cost = cost_so_far + step_cost

                # Với UCS thuần, ưu tiên chỉ dựa vào new_cost (không cộng thêm heuristic)
                new_priority = new_cost
                # Nếu neighbor chưa được mở rộng hoặc tìm được chi phí nhỏ hơn thì thêm vào heap
                if neighbor not in expanded_cost or new_cost < expanded_cost.get(neighbor, float('inf')):
                    heapq.heappush(heap, (new_priority, neighbor, current_path + [neighbor], new_cost))
                    memory = max(memory, len(heap))
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
