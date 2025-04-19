# Pacman Game 🎮

## 👥 Members
- 22120194 - Nguyễn Nhật Long
- 22120197 - Nguyễn Vĩnh Lương
- 22120238 - Nguyễn Minh Nguyên
- 22120252 - Giang Đức Nhật

## 📜 Description
This project is a Pacman game implemented in Python using **Pygame**, where each ghost uses a different pathfinding algorithm:
- Blue Ghost: Breadth-First Search (BFS)
- Pink Ghost: Depth-First Search (DFS)
- Orange Ghost: Uniform Cost Search (UCS)
- Red Ghost: A* Search (A-Star)

## 🚀 How to Run

### 1. Install dependencies
You can install all required packages using pip:

```bash
pip install -r requirements.txt
``` 
### 2. Run the game
After installing the dependencies, run:
```bash
py main.py
``` 

## 📁 Project Structure
```
ai-project-pacman/
├── algorithms                  # Các thuật toán tìm kiếm
│   ├── astar.py                  
│   ├── bfs.py          
│   ├── dfs.py
│   ├── ucs.py
│
├── assets/                     # Hình ảnh, âm thanh
│   ├── images/             
│   └── sounds/
│
├── entities/                   # Các đối tượng trong game
│   ├── entity.py                   
│   ├── ghost.py                    
│   ├── pacman.py
│   ├── blue_ghost.py
│   ├── pink_ghost.py
│   ├── orange_ghost.py
│   └── red_ghost.py
│   
├── maze/                       # Xử lý xoay quanh ma trận
│   ├── board_info.py
│   ├── level_config.py
│   └── maze_drawing.py
│   
├── scenes/                     # Xử lý giao diện của game
│   ├── base_scene.py
│   ├── maze_scene.py
│   ├── menu.py
│   └── win_scene.py
│
├── utils/                      # Các hàm hỗ trợ về UI, đo thông số,..
│   ├── button.py
│   ├── image_button.py
│   ├── text_button.py
│   ├── sounds.py
│   ├── pathfinding_utils.py
│   ├── pathfinding.py
│   └── performance_monitor.py
│    
├── game.py                     # Vòng lặp của game
├── main.py                     # Khởi động game
├── scene_manager.py            # Quản lý các mànhinhf
├── settings.py                 # Cấu hình khác
├── requirements.txt            # Danh sách thư viện cần cài
└── README.md                   
```
