import heapq
import tracemalloc
from utils.pathfinding_utils import is_valid  
from maze.board_info import BoardInfo 

class AStar:
    @staticmethod
    def calculate_cost(current, next_pos, dot_count=0):
        """
        Tính chi phí di chuyển từ nút current đến nút next_pos.
        Nếu tung độ (y) bằng nhau: trả về |hoành độ_current - hoành độ_next|.
        Nếu hoành độ (x) bằng nhau: trả về |tung độ_current - tung độ_next|.
        """
        if current[1] == next_pos[1]:
            base_cost = abs(current[0] - next_pos[0])
        elif current[0] == next_pos[0]:
            base_cost = abs(current[1] - next_pos[1])
        else:
            base_cost = 0 

        bonus = dot_count * 0.7
        return base_cost - bonus

    @staticmethod
    def traverse_direction(game_map, start, dx, dy, red_nodes):
        """
        Di chuyển từ nút start theo hướng (dx, dy) cho đến khi gặp nút red hoặc vị trí không hợp lệ.
        Trả về tuple (next_pos, path_segment, cost) nếu gặp được nút red, ngược lại trả về None.
        """
        current = start
        path_segment = []
        dot_count = 0

        while True:
            # Tính vị trí tiếp theo theo hướng cho trước
            next_pos = (current[0] + dx, current[1] + dy)
            
            if not is_valid(game_map, next_pos):
                return None
            
            path_segment.append(next_pos)
            # Đếm số lượng thức ăn
            x, y = next_pos
            if game_map[y][x] == 1:
                dot_count += 1
                
            current = next_pos
            
            # Nếu gặp nút red, tính chi phí và trả về thông tin
            if next_pos in red_nodes:
                cost = AStar.calculate_cost(start, next_pos, dot_count)
                return next_pos, path_segment, cost

    @staticmethod
    def heuristic(node, goal):
        """
        Hàm heuristic ước lượng chi phí từ node hiện tại đến đích (goal).
        Ở đây sử dụng khoảng cách Manhattan.
        """
        return abs(node[0] - goal[0]) + abs(node[1] - goal[1])

    @staticmethod
    def find_path(game_map, start, goal):
        tracemalloc.start()
        
        # Tiền xử lý: tạo tập các nút red và đảm bảo goal luôn có trong tập
        red_nodes = set(BoardInfo.red_nodes)
        if goal not in red_nodes:
            red_nodes.add(goal)
        
        # Theo dõi các nút đã mở rộng (node: chi phí tốt nhất g(n) đến nó)
        expanded_nodes = {}
        expanded_red_nodes_count = 0
        
        # Nếu start là nút red, lưu thêm thông tin về chiều dài đoạn đường đi
        red_nodes_with_length = {start: 0} if start in red_nodes else {}
        total_expanded_nodes = 0
        
        # Khởi tạo biến path trước khi vào vòng lặp
        path = []

        # Hàng đợi ưu tiên: (f(n) = g(n) + h(n), nút hiện tại, đường đi từ nút đầu, g(n))
        g_start = 0
        h_start = AStar.heuristic(start, goal)
        f_start = g_start + h_start

        heap = [(f_start, start, [], g_start)]
        
        # Các hướng di chuyển: lên, xuống, trái, phải
        directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]

        while heap:
            f_cost, current, current_path, g_cost = heapq.heappop(heap)
            
            # Nếu đã có đường đi tốt hơn đến nút này thì bỏ qua
            if current in expanded_nodes:
                continue
                
            expanded_nodes[current] = f_cost
            
            # Cập nhật số nút red được mở rộng và số nút đi qua (dựa trên độ dài của đoạn đường đi)
            if current in red_nodes:
                expanded_red_nodes_count += 1
                total_expanded_nodes += red_nodes_with_length.get(current, 0)
                
            # Nếu đã đến đích thì kết thúc
            if current == goal:
                path = current_path
                break
                
            # Duyệt theo 4 hướng
            for dx, dy in directions:
                result = AStar.traverse_direction(game_map, current, dx, dy, red_nodes)
                if result:
                    next_pos, path_segment, step_cost = result
                    new_g = g_cost + step_cost
                    new_h = AStar.heuristic(next_pos, goal)

                    new_f = new_g + new_h
                    
                    # Nếu chưa mở rộng nút hoặc tìm được đường đi tốt hơn
                    if next_pos not in expanded_nodes:
                        new_path = current_path + path_segment
                        heapq.heappush(heap, (new_f, next_pos, new_path, new_g))
                        # Cập nhật (hoặc khởi tạo) giá trị chiều dài đoạn đường từ current đến next_pos
                        if next_pos not in red_nodes_with_length or len(path_segment) < red_nodes_with_length[next_pos]:
                            red_nodes_with_length[next_pos] = len(path_segment)
        

        print("path:", path)
        print("nodes expanded:", expanded_red_nodes_count)
        print("total nodes passed:", total_expanded_nodes)
        
        current_mem, peak_memory = tracemalloc.get_traced_memory()
        print("current:", current_mem)
        print("peak_memory:", peak_memory)
        
        peak_memory_kb = peak_memory / 1024
        tracemalloc.stop()

        return path, total_expanded_nodes, peak_memory_kb
