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
        
        # Tạo tập các nút red và đảm bảo goal luôn có trong tập.
        red_nodes = set(BoardInfo.red_nodes)
        if goal not in red_nodes:
            red_nodes.add(goal)
        
        print("Danh sách node đỏ:", list(red_nodes))
        print("Số lượng node đỏ:", len(red_nodes))
        
        # Sử dụng dictionary lưu lại các nút đã mở rộng với chi phí tối ưu (g) đã đạt được.
        expanded_nodes = {}
        expanded_red_nodes_count = 0
        
        # Nếu start là nút red, lưu thông tin chiều dài đoạn đường.
        red_nodes_with_length = {start: 0} if start in red_nodes else {}
        
        total_expanded_nodes = 0
        path = []
        
        # Hàng đợi ưu tiên: (f = g + h, g, nút hiện tại, đường đi từ nút bắt đầu)
        start_h = AStar.heuristic(start, goal)
        heap = [(start_h, 0, start, [])]  # (f, g, current, path)
        
        # Các hướng di chuyển: lên, xuống, trái, phải.
        directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]
        
        while heap:
            f, g, current, current_path = heapq.heappop(heap)
            
            # Bỏ qua nếu đã có đường ngắn hơn đến current
            if current in expanded_nodes and expanded_nodes[current] <= g:
                continue
            expanded_nodes[current] = g
            
            # Nếu current là một nút red, lưu lại thông tin mở rộng
            if current in red_nodes:
                expanded_red_nodes_count += 1
                total_expanded_nodes += red_nodes_with_length.get(current, 0)
            
            # Kiểm tra nếu đã đạt đích
            if current == goal:
                path = current_path
                break
            
            # Duyệt qua các hướng di chuyển
            for dx, dy in directions:
                result = AStar.traverse_direction(game_map, current, dx, dy, red_nodes)
                if result:
                    next_pos, path_segment, step_cost = result
                    
                    new_g = g + step_cost            # Chi phí từ start đến next_pos
                    new_f = new_g + AStar.heuristic(next_pos, goal)  # f = g + h
                    
                    # Kiểm tra nếu có cách ngắn hơn tới next_pos
                    if next_pos not in expanded_nodes or new_g < expanded_nodes[next_pos]:
                        new_path = current_path + path_segment
                        heapq.heappush(heap, (new_f, new_g, next_pos, new_path))
                        # Cập nhật chiều dài đoạn đường của nút red nếu tốt hơn
                        if next_pos not in red_nodes_with_length or len(path_segment) < red_nodes_with_length[next_pos]:
                            red_nodes_with_length[next_pos] = len(path_segment)
        
        # Hiển thị các thông tin debug
        print("Path:", path)
        print("Nodes red expanded:", expanded_red_nodes_count)
        print("Total nodes passed:", total_expanded_nodes)
        
        current_mem, peak_memory = tracemalloc.get_traced_memory()
        print("Current memory:", current_mem)
        print("Peak memory:", peak_memory)
        
        peak_memory_kb = peak_memory / 1024
        tracemalloc.stop()
        
        return path, total_expanded_nodes, peak_memory_kb
