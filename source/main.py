import pygame

from map import Map
from graphic import CaroGraphics


# =========================
# Khởi tạo game
# =========================

map_ = Map()

gfx = CaroGraphics(
    rows=map_.N_map,
    cols=map_.N_map
)

clock = pygame.time.Clock()

running = True

# Người chơi đầu tiên là X
current_player = 1

# Lưu nước cuối
last_move = None

# Đếm số ô đã đánh
move_count = 0

game_over = False


# =========================
# Vòng lặp game
# =========================

while running:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN and not game_over:

            mx, my = pygame.mouse.get_pos()

            row, col = gfx.mouse_to_grid(mx, my)

            # Kiểm tra trong map
            if map_.isValid(row, col):

                # Đánh cờ
                map_.setMove(row, col, current_player)

                last_move = (row, col)

                move_count += 1

                # Kiểm tra thắng
                if map_.isWin(row, col):

                    if current_player == 1:
                        print("X WIN")
                    else:
                        print("O WIN")

                    game_over = True

                # Kiểm tra hòa
                elif move_count == map_.N_map * map_.N_map:

                    print("DRAW")
                    game_over = True

                # Đổi lượt
                current_player *= -1

    # =========================
    # Vẽ
    # =========================

    gfx.draw_board()

    gfx.draw_pieces(
        map_.board,
        last_move
    )

    pygame.display.flip()

    clock.tick(60)

pygame.quit()