
class Map:
    def __init__(self, N_map = 9, N_win = 4):
        self.N_map = N_map          # Kích thước map
        self.N_win = N_win          # Số giá trị liên tiếp để thắng
        self.board = [[0 for i in range(N_map)] for j in range(N_map)]  # Tạo map N*N
        self.dirs = [(1, 0), (0, 1), (1, 1), (-1, 1)]   # Các chiều của caro khi xét, x hướng xuống, y hướng sang ngang
        self.lastPlay = -1
        self.countTurn = 0
        self.boardValue = 0

    # Hàm vẽ map
    def drawBoard(self):
        for i in range(self.N_map):
            for j in range(self.N_map):
                if self.board[i][j] == 0:
                    print(". |", end=" ")
                elif self.board[i][j] == 1:
                    print("X |", end=" ")
                elif self.board[i][j] == -1:
                    print("O |", end=" ")
            print()
    
    # Hàm đánh X/O lên map 
    def setMove(self, i, j, state):
        self.board[i][j] = state
        self.lastPlay = state   # Lưu lại người vừa đánh
        self.countTurn += 1

    # Hàm kiểm tra vị trí có trong bàn cờ
    def isInBoard(self, i, j):
        return (i >= 0) and (i < self.N_map) and (j >= 0) and (j < self.N_map)
    
    # Hàm kiểm tra vị trí có hợp lệ không (trống và trong bàn cờ)
    def isValid(self, i, j):
        return self.isInBoard(i, j) and self.board[i][j] == 0 

    # Hàm đếm số X/O liên tiếp theo 1 chiều
    def countDir(self, i, j, dir):
        count = 0
        state = self.board[i][j]
        xdir, ydir = dir
        # Kiểm tra các giá trị theo chiều, nếu trùng count++ 
        for step in range(1, self.N_win):
            if self.isInBoard(i+step*xdir, j+step*ydir) and  self.board[i+step*xdir][j+step*ydir] == state:
                count += 1
            else:
                break
        return count

    # Hàm kiểm tra thắng chưa
    def isWin(self, i, j):
        for dir in self.dirs:
            count = self.countDir(i, j, dir) \
                + self.countDir(i, j, (-dir[0], -dir[1])) + 1  # Tổng số state liên tiếp = đếm 2 chiều ngược nhau + vị trí đang xét
            if count >= self.N_win:
                return True
        return False
    
    def isDraw(self):
        return self.countTurn == self.N_map**2
    
    def checkResult(self, i, j):
        if self.isWin(i, j):
            return self.lastPlay
        elif self.isDraw():
            return 0
        else:
            return None
    

