import pygame

from map import Map
from graphic import CaroGraphics
from ai import AI
from utils import create_template_dict

# =========================
# Khởi tạo game
# =========================

map_ = Map(N_map = 9, N_win = 4)
ai_=AI(map_)

gfx = CaroGraphics(
    rows=map_.N_map,
    cols=map_.N_map
)


clock = pygame.time.Clock()

running = True
#1 la AI, -1 la nguoi choi
# Người chơi đầu tiên là X
current_player = 1

game_over = False

levelA=True

# =========================
# Vòng lặp game
# =========================
while running:
    # =========================
    # AI đánh tự động
    # =========================
    if current_player==1:
        ai_.move(levelA = False)
        map_.setMove(ai_.currentI, ai_.currentJ, 1)
        current_player *= -1
    else:
    # ==================================
    # ==================================
    #even nguoi danh    
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN :
                # từ vị trí bấm chuột suy ra tọa độ trong map
                mx, my = pygame.mouse.get_pos()
            
                button = gfx.check_button_click((mx, my))

                if button == "Restart":

                    map_ = Map(N_map=map_.N_map, N_win=map_.N_win)
                    ai_=AI(map_)
                    current_player = 1
                    map_.countTurn = 0
                    game_over = False
                    map_.lastPlay = None
                    message = ""
                    continue

                elif button == "Exit":

                    running = False
                elif game_over:
                    continue
                else:
                    map_.lastI, map_.lastJ = gfx.mouse_to_grid(mx, my)
                    # Đánh cờ
                    map_.setMove( map_.lastI, map_.lastJ, current_player)
                    current_player *= -1

                    #==========================
                    #cap nhat xoa nuoc da danh ra khoi childnod

    ai_.boardValue = ai_.heuristic()
    ai_.childNode = ai_.newChildNode()
    map_.result= map_.checkResult( map_.lastI, map_.lastJ )
    if  map_.result is not None:
        # X win
        if map_.result == 1:
            gfx.message="X WIN"
        # O win
        elif map_.result == -1:
            gfx.message="O WIN"
        # hòa
        else:
            gfx.message="DRAW"

        game_over = True                
                # Đổi lượt
                
    
    # =========================
    # Vẽ
    # =========================

    gfx.draw_board()

    #vẽ bảng nút bấm bên cạnh
    gfx.draw_side_panel()
    gfx.draw_pieces(
        map_.board,
        map_.lastPlay
    )
    if game_over:
        gfx.draw_message(gfx.message)

    pygame.display.flip()

    clock.tick(60)

pygame.quit()