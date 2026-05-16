import math


class Map:
    def __init__(self, N_map=9, N_win=4):
        self.N_map = N_map
        self.N_win = N_win

        # 0 = trống
        # 1 = AI (X)
        # -1 = Human (O)
        self.board = [[0 for _ in range(N_map)] for _ in range(N_map)]

        # 4 hướng cần kiểm tra
        self.dirs = [
            (1, 0),   # dọc
            (0, 1),   # ngang
            (1, 1),   # chéo chính
            (-1, 1)   # chéo phụ
        ]

        self.lastPlay = -1
        self.countTurn = 0

    # =========================
    # HIỂN THỊ BÀN CỜ
    # =========================
    def drawBoard(self):
        print()

        for i in range(self.N_map):
            for j in range(self.N_map):

                if self.board[i][j] == 0:
                    print(". ", end=" ")

                elif self.board[i][j] == 1:
                    print("X ", end=" ")

                else:
                    print("O ", end=" ")

            print()

        print()

    # =========================
    # ĐÁNH CỜ
    # =========================
    def setMove(self, i, j, state):
        self.board[i][j] = state
        self.lastPlay = state
        self.countTurn += 1

    # =========================
    # KIỂM TRA TRONG BÀN CỜ
    # =========================
    def isInBoard(self, i, j):
        return (
            0 <= i < self.N_map and
            0 <= j < self.N_map
        )

    # =========================
    # KIỂM TRA NƯỚC ĐI HỢP LỆ
    # =========================
    def isValid(self, i, j):
        return (
            self.isInBoard(i, j) and
            self.board[i][j] == 0
        )

    # =========================
    # ĐẾM LIÊN TIẾP 1 HƯỚNG
    # =========================
    def countDir(self, i, j, dir):
        count = 0

        state = self.board[i][j]

        xdir, ydir = dir

        for step in range(1, self.N_win):

            new_i = i + step * xdir
            new_j = j + step * ydir

            if (
                self.isInBoard(new_i, new_j)
                and self.board[new_i][new_j] == state
            ):
                count += 1

            else:
                break

        return count

    # =========================
    # KIỂM TRA THẮNG
    # =========================
    def isWin(self, i, j):

        for dir in self.dirs:

            count = (
                self.countDir(i, j, dir)
                + self.countDir(i, j, (-dir[0], -dir[1]))
                + 1
            )

            if count >= self.N_win:
                return True

        return False

    # =========================
    # KIỂM TRA HÒA
    # =========================
    def isDraw(self):
        return self.countTurn == self.N_map ** 2

    # =========================
    # KIỂM TRA KẾT QUẢ
    # =========================
    def checkResult(self, i, j):

        if self.isWin(i, j):
            return self.lastPlay

        elif self.isDraw():
            return 0

        return None

    # =========================
    # LẤY DANH SÁCH NƯỚC ĐI
    # =========================
    def getChildMoves(self):

        moves = []

        for i in range(self.N_map):
            for j in range(self.N_map):

                if self.isValid(i, j):
                    moves.append((i, j))

        return moves

    # =========================
    # HÀM ĐÁNH GIÁ
    # =========================
    def evaluate(self):

        score = 0

        for i in range(self.N_map):
            for j in range(self.N_map):

                # AI
                if self.board[i][j] == 1:
                    score += self.evaluatePosition(i, j)

                # Human
                elif self.board[i][j] == -1:
                    score -= self.evaluatePosition(i, j)

        return score

    # =========================
    # ĐÁNH GIÁ 1 Ô
    # =========================
    def evaluatePosition(self, i, j):

        total = 0

        for dir in self.dirs:

            count = (
                self.countDir(i, j, dir)
                + self.countDir(i, j, (-dir[0], -dir[1]))
                + 1
            )

            # điểm đơn giản
            if count == 2:
                total += 10

            elif count == 3:
                total += 100

            elif count >= 4:
                total += 10000

        return total

    # =========================
    # MINIMAX
    # =========================
    def minimax(self, depth, maximizingPlayer):

        # =====================
        # KIỂM TRA KẾT THÚC
        # =====================

        if depth == 0:
            return self.evaluate(), None

        # kiểm tra thắng/thua
        for i in range(self.N_map):
            for j in range(self.N_map):

                if self.board[i][j] != 0:

                    if self.isWin(i, j):

                        # AI thắng
                        if self.board[i][j] == 1:
                            return 1000000, None

                        # Human thắng
                        else:
                            return -1000000, None

        # hòa
        if self.isDraw():
            return 0, None

        # =====================
        # MAX PLAYER (AI)
        # =====================

        if maximizingPlayer:

            bestValue = -math.inf
            bestMove = None

            for move in self.getChildMoves():

                i, j = move

                # đánh thử
                self.setMove(i, j, 1)

                # đệ quy
                value, _ = self.minimax(depth - 1, False)

                # undo
                self.board[i][j] = 0
                self.countTurn -= 1

                # cập nhật tốt nhất
                if value > bestValue:
                    bestValue = value
                    bestMove = move

            return bestValue, bestMove

        # =====================
        # MIN PLAYER (HUMAN)
        # =====================

        else:

            bestValue = math.inf
            bestMove = None

            for move in self.getChildMoves():

                i, j = move

                # đánh thử
                self.setMove(i, j, -1)

                # đệ quy
                value, _ = self.minimax(depth - 1, True)

                # undo
                self.board[i][j] = 0
                self.countTurn -= 1

                # cập nhật tốt nhất
                if value < bestValue:
                    bestValue = value
                    bestMove = move

            return bestValue, bestMove


# =========================================
# GAME LOOP
# =========================================

game = Map()

turn = -1

while True:

    game.drawBoard()

    # =========================
    # HUMAN
    # =========================
    if turn == -1:

        print("Human turn")

        i = int(input("Row: "))
        j = int(input("Col: "))

        if not game.isValid(i, j):
            print("Invalid move")
            continue

        game.setMove(i, j, -1)

    # =========================
    # AI
    # =========================
    else:

        print("AI thinking...")

        value, move = game.minimax(3, True)

        i, j = move

        print("AI move:", move)
        print("Value:", value)

        game.setMove(i, j, 1)

    # =========================
    # CHECK RESULT
    # =========================

    result = game.checkResult(i, j)

    if result is not None:

        game.drawBoard()

        if result == 1:
            print("AI WIN")

        elif result == -1:
            print("HUMAN WIN")

        else:
            print("DRAW")

        break

    # đổi lượt
    turn *= -1