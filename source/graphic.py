import pygame

class CaroGraphics(object):
    def __init__(self, rows=9, cols=9, cell_size=60, margin=40):

        pygame.init()

        self.rows = rows
        self.cols = cols
        self.cell_size = cell_size
        self.margin = margin

        width = cols * cell_size + margin * 2
        height = rows * cell_size + margin * 2

        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Caro Game")

        # Màu
        self.BG_COLOR = (245, 245, 245)
        self.LINE_COLOR = (120, 120, 120)

        self.X_COLOR = (220, 50, 50)
        self.O_COLOR = (50, 100, 220)

        self.HIGHLIGHT = (120, 220, 120)

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