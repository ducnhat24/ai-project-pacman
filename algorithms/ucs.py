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
            priority, current, current_path, cost_so_far = heapq.heappop(heap)

            # Nếu đã mở rộng current với chi phí nhỏ hơn hoặc bằng thì bỏ qua
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
