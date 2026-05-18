from map import Map
from ai import AI


map_ = Map()
ai = AI(map_, 3)
run = True
while run:
    if map_.countTurn %2 == 0:
        ai.move()
    else:
        i, j = list(map(int, input("Nhập tọa độ hàng cột: ").split()))
        map_.setMove(i, j, -1)
    
    ai.boardValue = ai.heuristic()
    ai.childNode = ai.newChildNode()
        
    map_.drawBoard()
    print("boardValue: {0} ".format([ai.boardValue]))
    result = map_.checkResult(map_.lastI, map_.lastJ)
    if result != None:
        run = False
        if result == 1:
            state = "X win"
        elif result == -1:
            state = "O win"
        else:
            state = "Draw"
        
        print(state)




