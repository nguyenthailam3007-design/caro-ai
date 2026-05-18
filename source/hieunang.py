from map import Map
from ai import AI
import time

map_ = Map()
ai = AI(map_, 3)
run = True
while run:
    if map_.countTurn %2 == 0:
        start_time = time.time() 
        ai.move(levelA = True)
        end_time = time.time()
        minimaxTime = end_time - start_time
        print(f"minimax | time: {minimaxTime:.3f}s   (i,j) = ({ai.currentI},{ai.currentJ})   visitedNodes: {ai.visitedNodes}")
        start_time = time.time()
        ai.move(levelA = False)
        end_time = time.time()
        alphaBetaTime = end_time - start_time
        print(f"alphaBeta | time: {alphaBetaTime:.3f}s   (i,j) = ({ai.currentI},{ai.currentJ})   visitedNodes: {ai.visitedNodes}")
        map_.setMove(ai.currentI, ai.currentJ, 1)
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




