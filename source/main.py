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
map_.lastplay = None

# Đếm số ô đã đánh
map_.countTurn = 0

game_over = False


# =========================
# Vòng lặp game
# =========================

while running:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
            # từ vị trí bấm chuột suy ra tọa độ trong map
            mx, my = pygame.mouse.get_pos()
            #
            button = gfx.check_button_click((mx, my))

            if button == "Restart":

                map_ = Map(N_map=9, N_win=5)

                current_player = 1
                map_.countTurn = 0
                game_over = False
                map_.lastplay = None
                message = ""

                continue

            elif button == "Undo":

                print("Undo")

                continue

            elif button == "Exit":

                running = False


            row, col = gfx.mouse_to_grid(mx, my)

            # Kiểm tra trong map
            if map_.isValid(row, col):

                # Đánh cờ
                map_.setMove(row, col, current_player)

                map_.lastplay = (row, col)

                map_.countTurn += 1

                # Kiểm tra game over chưa
                # if map_.checkResult != None:
                #     # X win
                #     if map_.checkResult(row, col) == 1:
                #         gfx.message="X WIN"
                #     # O win
                #     elif map_.checkResult(row, col) == -1:
                #         gfx.message="O WIN"
                #     # hòa
                #     else:
                #         gfx.message="DRAW"

                #     game_over = True
                if map_.checkResult != None:
                    # X win
                    if map_.checkResult(row, col) == 1:
                        gfx.message="X WIN"
                    # O win
                    elif map_.checkResult(row, col) == -1:
                        gfx.message="O WIN"
                    # hòa
                    else:
                        gfx.message="DRAW"

                    game_over = True                
                # Đổi lượt
                current_player *= -1

    # =========================
    # Vẽ
    # =========================

    gfx.draw_board()
    #vẽ bảng nút bấm bên cạnh
    gfx.draw_side_panel()
    gfx.draw_pieces(
        map_.board,
        map_.lastplay
    )
    if game_over:
        gfx.draw_message(gfx.message)

    pygame.display.flip()

    clock.tick(60)

pygame.quit()