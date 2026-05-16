import pygame

class CaroGraphics(object):
    def __init__(self, rows=18, cols=20, cell_size=35, margin=20):
        pygame.init()
        self.rows = rows
        self.cols = cols
        self.cell_size = cell_size
        self.margin = margin
        
        # Tự động tính kích thước cửa sổ dựa trên số ô và lề
        width = self.cols * self.cell_size + 2 * self.margin
        height = self.rows * self.cell_size + 2 * self.margin
        self.screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
        pygame.display.set_caption("Caro AI - Simple Graphics")

        # Định nghĩa màu sắc (RGB)
        self.BG_COLOR = (245, 245, 245)      # Trắng xám
        self.LINE_COLOR = (150, 150, 150)    # Xám
        self.X_COLOR = (235, 70, 70)         # Đỏ
        self.O_COLOR = (70, 130, 235)        # Xanh dương
        self.HIGHLIGHT_COLOR = (77, 199, 61) # Xanh lá

    def _grid_to_pixel(self, row, col):
        """Hàm nội bộ (helper): Chuyển index (row, col) thành tọa độ pixel ở TÂM của ô"""
        x = self.margin + col * self.cell_size + self.cell_size // 2
        y = self.margin + row * self.cell_size + self.cell_size // 2
        return pygame.math.Vector2(x, y)

    def draw_board(self):
        """Vẽ nền và lưới bàn cờ"""
        self.screen.fill(self.BG_COLOR)
        
        start_x = start_y = self.margin
        end_x = self.margin + self.cols * self.cell_size
        end_y = self.margin + self.rows * self.cell_size

        # Vẽ các đường ngang
        for r in range(self.rows + 1):
            y = start_y + r * self.cell_size
            pygame.draw.line(self.screen, self.LINE_COLOR, (start_x, y), (end_x, y), 1)
        
        # Vẽ các đường dọc
        for c in range(self.cols + 1):
            x = start_x + c * self.cell_size
            pygame.draw.line(self.screen, self.LINE_COLOR, (x, start_y), (x, end_y), 1)

    def draw_pieces(self, map_data, last_move=None):
        """
        Vẽ toàn bộ quân cờ từ mảng 2D. 
        map_data: mảng 2 chiều chứa 'X', 'O' hoặc kí tự rỗng.
        last_move: tuple (row, col) để bôi xanh nước đi cuối.
        """
        # Bán kính/Độ dài nhánh của X và O (chiếm 1/3 kích thước ô cho đẹp)
        offset = self.cell_size // 3 
        
        for r in range(self.rows):
            for c in range(self.cols):
                val = map_data[r][c]
                if val == 0 or val == '.' or val == '':  # Bỏ qua ô trống
                    continue
                
                center = self._grid_to_pixel(r, c)

                # Nổi bật nước đi cuối (Vẽ một ô vuông nền xanh lá mờ dưới quân cờ)
                if last_move and last_move == (r, c):
                    rect_x = self.margin + c * self.cell_size + 1
                    rect_y = self.margin + r * self.cell_size + 1
                    rect_size = self.cell_size - 1
                    pygame.draw.rect(self.screen, self.HIGHLIGHT_COLOR, (rect_x, rect_y, rect_size, rect_size))

                # Vẽ X (2 đường chéo)
                if val == 'X':
                    p1 = center + pygame.math.Vector2(-offset, -offset)
                    p2 = center + pygame.math.Vector2(offset, offset)
                    p3 = center + pygame.math.Vector2(offset, -offset)
                    p4 = center + pygame.math.Vector2(-offset, offset)
                    pygame.draw.line(self.screen, self.X_COLOR, p1, p2, 3)
                    pygame.draw.line(self.screen, self.X_COLOR, p3, p4, 3)
                
                # Vẽ O (Hình tròn rỗng tâm)
                elif val == 'O':
                    pygame.draw.circle(self.screen, self.O_COLOR, center, offset, 3)

if __name__ == "__main__":
    # 1. Giả lập dữ liệu bàn cờ
    ROWS, COLS = 18, 20
    board_data = [['.' for _ in range(COLS)] for _ in range(ROWS)]
    board_data[8][9] = 'X'
    board_data[8][10] = 'O'
    board_data[9][10] = 'X'
    
    # 2. Khởi tạo đồ họa
    gfx = CaroGraphics(rows=ROWS, cols=COLS)
    clock = pygame.time.Clock()
    running = True

    # 3. Vòng lặp chính
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            # Click chuột để test thả X
            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                # Công thức quy ngược từ pixel ra index của map
                col = (mx - gfx.margin) // gfx.cell_size
                row = (my - gfx.margin) // gfx.cell_size
                if 0 <= row < ROWS and 0 <= col < COLS:
                    board_data[row][col] = 'X'
                    last_move = (row, col)

        # Cập nhật đồ họa liên tục
        gfx.draw_board()
        # Truyền thử last_move = (9, 10) để xem highlight
        gfx.draw_pieces(board_data, last_move=(9, 10)) 
        
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()