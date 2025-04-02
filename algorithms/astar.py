import heapq

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
        print("A* algorithm is not implemented yet.")