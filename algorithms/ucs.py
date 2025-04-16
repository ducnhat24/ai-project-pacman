import heapq
import tracemalloc
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
        tracemalloc.start()
        
        # Tiền xử lý: tạo tập các nút red và đảm bảo goal luôn có trong tập
        red_nodes = set(BoardInfo.red_nodes)
        if goal not in red_nodes:
            red_nodes.add(goal)
        
        # Theo dõi các nút đã mở rộng (node: cost tối ưu đến nó)
        expanded_nodes = {}
        expanded_red_nodes_count = 0
        
        # Nếu start là nút red, lưu thêm thông tin về chiều dài đoạn đường đi
        red_nodes_with_length = {start: 0} if start in red_nodes else {}
        
        total_expanded_nodes = 0
        
        # Khởi tạo biến path trước khi vào vòng lặp
        path = []
        # Hàng đợi ưu tiên: (chi phí đến nút, nút hiện tại, đường đi từ nút đầu)
        heap = [(0, start, [])]
        
        # Các hướng di chuyển: lên, xuống, trái, phải
        directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]

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
                
            # Duyệt theo 4 hướng
            for dx, dy in directions:
                result = UCS.traverse_direction(game_map, current, dx, dy, red_nodes)
                if result:
                    next_pos, path_segment, step_cost = result
                    new_cost = cost_so_far + step_cost
                    
                    # Nếu chưa mở rộng nút hoặc tìm được đường đi tốt hơn
                    if next_pos not in expanded_nodes or new_cost < expanded_nodes[next_pos]:
                        new_path = current_path + path_segment
                        heapq.heappush(heap, (new_cost, next_pos, new_path))
                        # Cập nhật (hoặc khởi tạo) giá trị chiều dài đoạn đường từ current đến next_pos
                        if next_pos not in red_nodes_with_length or len(path_segment) < red_nodes_with_length[next_pos]:
                            red_nodes_with_length[next_pos] = len(path_segment)
        
        # Nếu không tìm thấy đường đi, path vẫn là []
        print("path:", path)
        print("nodes expanded:", expanded_red_nodes_count)
        print("total nodes passed:", total_expanded_nodes)
        
        current_mem, peak_memory = tracemalloc.get_traced_memory()
        print("current:", current_mem)
        print("peak_memory:", peak_memory)
        
        peak_memory_kb = peak_memory / 1024
        tracemalloc.stop()
        
        return path, total_expanded_nodes, peak_memory_kb
