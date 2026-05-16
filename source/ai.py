from map import Map

class AI:
    def __init__(self, game_map, depth = 4):
        self.map = game_map
        self.boardValue
        self.childNode
        self.patternDic = {
                            [0, 1, 1, 1, 0]: 1e4,
                            [1, 1, 1, 0]: 1e2,
                            [1, 1, 0]: 1e1
                            }
        


    