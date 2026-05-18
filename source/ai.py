
import math
import utils

class AI:
    def __init__(self, game_map, depth = 4):
        self.map = game_map     # Map của game 
        self.nMap = self.map.N_map  # Số cột, hàng của map
        self.templates = utils.create_template_dict()   # Các mẫu và điểm tương ứng
        self.depth = depth  # Độ sâu tìm kiếm
        self.currentI = None
        self.currentJ = None
        self.boardValue = 0    # giá trị trạng thái của bàn cờ
        self.childNode = []    # Tệp chứa các nút con
        self.visitedNodes = 0      # Số nút con đã duyệt


    # Sau khi đánh, tạo tập nút con mới(newchilNode) và thêm các vị trí xung quanh đó 
    # rồi xóa vị trí vừa đánh, không ảnh hưởng oldChildNode
    def newChildNode(self, i = None, j = None, oldChildNode = None):
        # Nếu không truyền tham số thì lấy
        if i == None:
            i = self.map.lastI
            j = self.map.lastJ
            oldChildNode = self.childNode

        # Copy để sửa đổi không hưởng đến oldChiNode
        newChildNode = oldChildNode.copy()
        # Nếu nút vừa đánh có trong childNode thì xóa nó đi
        if (i, j) in newChildNode:
            newChildNode.remove((i, j))
        # 8 vị trí xung quanh (i,j)
        find = [(i-1, j-1), (i-1, j), (i-1, j+1), 
                (i,   j-1),           (i,   j+1), 
                (i+1, j-1), (i+1, j), (i+1, j+1)]
        
        for test in find :
            # Nếu vị trí hợp lệ và chưa có trong childNode thì thêm vào
            if (test not in newChildNode) and self.map.isValid(test[0], test[1]) :
                newChildNode.append(test)
        return newChildNode


    # Hàm AI move levelA = minimax; levelB = alphaBeta
    def move(self, levelA = True):
        # Nếu AI đi lượt đầu đánh vào giữa
        if self.map.countTurn == 0:
            self.currentI = self.currentJ = int(self.nMap/2)
        elif levelA:
            # Minimax trả về nước đi ở self.currentI, self.currentJ
            self.minimax()
        else:
            # AlphaBeta trả về nước đi ở self.currentI, self.currentJ
             self.alphaBeta()

        # Đi nước vừa tính được
        self.map.setMove(self.currentI, self.currentJ, 1)



    # Hàm đếm xem template xuất hiện mấy lần theo các chiều quanh vị trí i, j
    def countTemplate(self, i, j, template):
        length = len(template)
        count = 0
        # 4 chiều cần quét
        dirs = [(1, 0), (0, 1), (1, 1), (-1, 1)]
        # Kiểm tra từng chiều
        for dir in dirs:
            x = dir[0]
            y = dir[1]
            
            # dir = (1, 0) hoặc (0, 1)
            if x*y == 0:
                #  Số cần bước lùi tối đa = length-1, nó = i hoặc j nếu nó nhỏ hơn length-1 (đến giới hạn map)
                steps_back = min(length-1, i)*x + min(length-1, j)*y
            
            # dir = (1, 1)
            elif x == 1:
                steps_back = min(length-1, i, j)
            
            # dir = (-1, 1)
            else:
                steps_back = min(length-1, self.nMap-i-1, j)
            
            # Lùi khoảng steps_back
            i0 = i - steps_back*x
            j0 = j - steps_back*y

            # Tiến lần lượt (0 -> steps_back) bước để quét template xuất hiện k  
            for a in range(steps_back + 1):
                inew = i0 + a*x
                jnew = j0 + a*y

                # Biến same xem template có xuất hiện k 
                same = True
                # kiểm tra, so từng số trong template với map
                for index in range(length):

                    # Nếu ra ngoài map hoặc khác thì cập nhật same = False và break
                    if not(self.map.isInBoard(inew, jnew))\
                            or self.map.board[inew][jnew] != template[index]:
                        same = False
                        break

                    inew += x
                    jnew += y

                if same:
                    count += 1   # cập nhật count
        return count


    # Hàm ước lượng điểm bàn cờ(boardValue) sau khi đánh state vào vị trí i, j
    def heuristic(self, i = None, j = None, oldBoardValue = None ):
        # Nếu không truyền tham số thì lấy
        if i == None:
            i = self.map.lastI
            j = self.map.lastJ
            oldBoardValue = self.boardValue

        # Lưu state để tý xóa rồi trả lại 
        state = self.map.board[i][j]
        beforeValue = 0
        afterValue = 0

        # Xét từng template
        for template in self.templates:
            # score là điểm của template đang xét
            score = self.templates[template]
            # Tạm thời xóa quân cờ ở i, j để tính 
            self.map.board[i][j] = 0
            # Tính giá trị của các template cũ xung quanh i, j khi chưa đánh
            beforeValue += self.countTemplate(i, j, template)*score
            # Trả lại trạng thái như cũ
            self.map.board[i][j] = state
            # Tính giá trị của các template mới xung quanh i, j sau khi đánh
            afterValue += self.countTemplate(i, j, template)*score
        # Giá trị mới = giá trị cũ + giá trị tăng thêm 
        return oldBoardValue + afterValue - beforeValue


    # Hàm minimax, input: depth(độ sâu), boardvalue(điểm bàn cờ hiện tại), childNode(tập con), lastI,lastJ(nước đi trước đó), max=AI 
    def minimax(self, depth = None, boardValue = None, childNode = None,\
                 lastI = None, lastJ = None, maximizingPlayer = True):
        
        # Nếu không truyền thì lấy từ ai
        if depth == None:
            depth = self.depth
            boardValue = self.boardValue
            childNode = self.childNode
            lastI = self.map.lastI
            lastJ = self.map.lastJ

        # Điều kiện dừng hàm
        if self.map.isWin(lastI, lastJ):
            # Nếu đã win mà lượt đánh tiếp là max thì min win
            if maximizingPlayer:
                return -math.inf
            else:
                return +math.inf
        # Nếu hòa
        elif self.map.isDraw():
            return 0
        # Nếu chạm giới hạn độ sâu
        elif depth == 0:
            return boardValue
        
        # Biến đếm số nút đã duyệt
        if depth == self.depth:
            self.visitedNodes = 0
        if maximizingPlayer:
            max_val = -math.inf
            # duyệt từng nút con (i, j)
            for child in childNode:
                self.visitedNodes += 1
                i, j = child[0], child[1]
                # AI đánh thử để tìm kiếm
                self.map.board[i][j] = 1
                # Tập nút con mới của nút con (i, j)
                newChildNode = self.newChildNode(i, j, childNode)            
                # Tính giá trị bàn cờ của nút con (i, j)
                newBoardVal = self.heuristic(i, j, boardValue)
                # Gọi minimax để tính nút con
                eval = self.minimax(depth-1, newBoardVal, newChildNode, i, j, False)
                # Nếu tìm được nút con tốt hơn thì cập nhật i, j
                if eval > max_val:
                    max_val = eval
                    if depth == self.depth:
                        self.currentI = i
                        self.currentJ = j
                # xóa đánh thử khi kết thúc tìm kiếm
                self.map.board[i][j] = 0 
            return max_val
        
        # Nếu minPlayer
        else:
            min_val = math.inf
            for child in childNode:
                self.visitedNodes += 1
                i, j = child[0], child[1]
                self.map.board[i][j] = -1
                newChildNode = self.newChildNode(i, j, childNode)
                newBoardVal = self.heuristic(i, j, boardValue)
                eval = self.minimax(depth-1, newBoardVal, newChildNode, i, j, True)
                if eval < min_val:
                    min_val = eval
                    if depth == self.depth:
                        self.currentI = i
                        self.currentJ = j
                self.map.board[i][j] = 0
            return min_val
        
    # Hàm alphaBeta
    def alphaBeta(self, depth = None, boardValue = None, childNode = None, lastI = None,\
                  lastJ = None, alpha = -math.inf, beta = math.inf, maximizingPlayer = True):
        
        # Nếu không truyền thì lấy từ ai
        if depth == None:
            depth = self.depth
            boardValue = self.boardValue
            childNode = self.childNode
            lastI = self.map.lastI
            lastJ = self.map.lastJ

        # Điều kiện dừng hàm
        if self.map.isWin(lastI, lastJ):
            # Nếu đã win mà lượt đánh tiếp là max thì min win
            if maximizingPlayer:
                return -math.inf
            else:
                return +math.inf
        # Nếu hòa
        elif self.map.isDraw():
            return 0
        # Nếu chạm giới hạn độ sâu
        elif depth == 0:
            return boardValue
        
        # Biến đếm số nút đã duyệt
        if depth == self.depth:
            self.visitedNodes = 0
        if maximizingPlayer:
            max_val = -math.inf
            for child in childNode:
                self.visitedNodes += 1
                i, j = child[0], child[1]
                self.map.board[i][j] = 1
                newChildNode = self.newChildNode(i, j, childNode)
                newBoardVal = self.heuristic(i, j, boardValue)
                eval = self.alphaBeta(depth-1, newBoardVal, newChildNode, i, j, alpha, beta, False)
                if eval > max_val:
                    max_val = eval
                    if depth == self.depth:
                        self.currentI = i
                        self.currentJ = j

                self.map.board[i][j] = 0
                alpha = max(alpha, eval) 
                if beta <= alpha: # cắt nhánh
                    break
            return max_val
        else:
            min_val = math.inf
            for child in childNode:
                self.visitedNodes += 1
                i, j = child[0], child[1]
                self.map.board[i][j] = -1
                newChildNode = self.newChildNode(i, j, childNode)
                newBoardVal = self.heuristic(i, j, boardValue)
                eval = self.alphaBeta(depth-1, newBoardVal, newChildNode, i, j, alpha, beta, True)
                if eval < min_val:
                    min_val = eval
                    if depth == self.depth:
                        self.currentI = i
                        self.currentJ = j
                self.map.board[i][j] = 0
                beta = min(beta, eval)
                if beta <= alpha: # cắt nhánh
                    break
            return min_val

