import pygame

class CaroGraphics(object):
    def __init__(self, rows=9, cols=9, cell_size=70, margin=50):

        pygame.init()

        self.rows = rows
        self.cols = cols
        self.cell_size = cell_size
        self.margin = margin

        self.panel_width = 180
        width = cols * cell_size + margin * 2 + self.panel_width
        height = rows * cell_size + margin * 2

        self.screen = pygame.display.set_mode((width, height),pygame.RESIZABLE)
        pygame.display.set_caption("Caro Game")
        self.font = pygame.font.SysFont("arial", 40, bold=True)

        # Màu
        self.BG_COLOR = (245, 245, 245)
        self.LINE_COLOR = (120, 120, 120)

        self.X_COLOR = (220, 50, 50)
        self.O_COLOR = (50, 100, 220)

        self.HIGHLIGHT = (120, 220, 120)
        self.message=""

        #tạo danh sách nút bấm
        self.buttons = {}

    def _grid_to_pixel(self, row, col):

        x = self.margin + col * self.cell_size + self.cell_size // 2
        y = self.margin + row * self.cell_size + self.cell_size // 2

        return (x, y)

    def draw_board(self):

        self.screen.fill(self.BG_COLOR)

        start_x = self.margin
        start_y = self.margin

        end_x = self.margin + self.cols * self.cell_size
        end_y = self.margin + self.rows * self.cell_size

        # Ngang
        for r in range(self.rows + 1):

            y = start_y + r * self.cell_size

            pygame.draw.line(
                self.screen,
                self.LINE_COLOR,
                (start_x, y),
                (end_x, y),
                1
            )

        # Dọc
        for c in range(self.cols + 1):

            x = start_x + c * self.cell_size

            pygame.draw.line(
                self.screen,
                self.LINE_COLOR,
                (x, start_y),
                (x, end_y),
                1
            )

    def draw_pieces(self, board, last_move=None):

        offset = self.cell_size // 3

        for r in range(self.rows):
            for c in range(self.cols):

                val = board[r][c]

                if val == 0:
                    continue

                # Highlight nước cuối
                if last_move == (r, c):

                    rect_x = self.margin + c * self.cell_size + 1
                    rect_y = self.margin + r * self.cell_size + 1

                    pygame.draw.rect(
                        self.screen,
                        self.HIGHLIGHT,
                        (
                            rect_x,
                            rect_y,
                            self.cell_size - 2,
                            self.cell_size - 2
                        )
                    )

                center = self._grid_to_pixel(r, c)

                # X
                if val == 1:

                    x, y = center

                    pygame.draw.line(
                        self.screen,
                        self.X_COLOR,
                        (x-offset, y-offset),
                        (x+offset, y+offset),
                        4
                    )

                    pygame.draw.line(
                        self.screen,
                        self.X_COLOR,
                        (x+offset, y-offset),
                        (x-offset, y+offset),
                        4
                    )

                # O
                elif val == -1:

                    pygame.draw.circle(
                        self.screen,
                        self.O_COLOR,
                        center,
                        offset,
                        4
                    )

    def mouse_to_grid(self, mx, my):

        col = (mx - self.margin) // self.cell_size
        row = (my - self.margin) // self.cell_size

        return row, col
    
    def draw_message(self, text):

        # Tạo text surface
        text_surface = self.font.render(
            text,
            True,
            (20, 20, 20)
        )

        # Lấy hình chữ nhật của text
        rect = text_surface.get_rect()

        # Đặt giữa màn hình
        rect.center = (
            self.screen.get_width() // 2,
            self.margin // 2
        )

        # Vẽ nền trắng phía sau text
        bg_rect = rect.inflate(20, 10)

        pygame.draw.rect(
            self.screen,
            (255, 255, 255),
            bg_rect
        )

        pygame.draw.rect(
            self.screen,
            (50, 50, 50),
            bg_rect,
            2
        )

        # Vẽ text
        self.screen.blit(text_surface, rect)

    def draw_side_panel(self):

        board_width = self.cols * self.cell_size + self.margin * 2

        panel_x = board_width

        panel_rect = pygame.Rect(
            panel_x,
            0,
            self.panel_width,
            self.screen.get_height()
        )

        # nền panel
        pygame.draw.rect(
            self.screen,
            (230, 230, 230),
            panel_rect
        )

        # title
        title = self.font.render(
            "MENU",
            True,
            (20, 20, 20)
        )

        self.screen.blit(
            title,
            (panel_x + 40, 30)
        )

        # tạo button
        self.draw_button(
            "Restart",
            panel_x + 20,
            100
        )

        self.draw_button(
            "Undo",
            panel_x + 20,
            180
        )

        self.draw_button(
            "Exit",
            panel_x + 20,
            260
        )

    def draw_button(self, text, x, y,
                    width=140,
                    height=50):

        rect = pygame.Rect(x, y, width, height)

        # lưu button
        self.buttons[text] = rect

        # nền
        pygame.draw.rect(
            self.screen,
            (180, 180, 180),
            rect,
            border_radius=10
        )

        # viền
        pygame.draw.rect(
            self.screen,
            (80, 80, 80),
            rect,
            2,
            border_radius=10
        )

        # text
        text_surface = self.font.render(
            text,
            True,
            (0, 0, 0)
        )

        text_rect = text_surface.get_rect(center=rect.center)

        self.screen.blit(text_surface, text_rect)
    def check_button_click(self, pos):

        for name, rect in self.buttons.items():

            if rect.collidepoint(pos):
                return name

        return None