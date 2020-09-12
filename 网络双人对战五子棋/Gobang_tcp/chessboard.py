from chessman import  ChessMan


class ChessBoard(object):
    BOAED_SIZE=15

    def __init__(self):
        # 初始化
        self.__board=[[0 for i in range(ChessBoard.BOAED_SIZE+1)]
                    for i in range(ChessBoard.BOAED_SIZE+1)]

    # 清空棋盘
    def initBoard(self):
        # 忽略第一行
        for i in  range(1,ChessBoard.BOAED_SIZE+1):
            for j in range(1,ChessBoard.BOAED_SIZE+1):
                self.__board[i][j]='+'

    # 打印棋盘
    def printBoard(self):
        # 打印行号
        print('  ',end='')
        for i in range(1, ChessBoard.BOAED_SIZE + 1):
            print(chr(i+ord('a')-1),end='')
        print()

        for i in range(1, ChessBoard.BOAED_SIZE + 1):
            # 打印列号
            print('%2d'%i,end='')
            for j in range(1, ChessBoard.BOAED_SIZE + 1):
               print(self.__board[i][j],end='')
            print()


    def setChess(self,pos,color):
        # 放置棋子
        if not isinstance(pos,tuple) and not isinstance(pos,list):
            raise Exception("第一个参数被选为元组或列表")
        if pos[0] <= 0 or pos[0]>ChessBoard.BOAED_SIZE:
            raise  Exception('下标越界')
        if pos[1] <= 0 or pos[1]>ChessBoard.BOAED_SIZE:
            raise  Exception('下标越界')
        self.__board[pos[0]][pos[1]]=color


    def setChessMan(self,chessman):
        if not isinstance(chessman,ChessMan):
            raise Exception('第一个参数必须为ChessMan对象')

        pos=chessman.Pos
        color=chessman.Color
        self.setChess(pos,color)

    def getChess(self,pos):
        if not isinstance(pos, tuple) and not isinstance(pos, list):
            raise Exception("第一个参数被选为元组或列表")
        if pos[0] <= 0 or pos[0] > ChessBoard.BOAED_SIZE:
            raise Exception('下标越界')
        if pos[1] <= 0 or pos[1] > ChessBoard.BOAED_SIZE:
            raise Exception('下标越界')
        return  self.__board[pos[0]][pos[1]]

    def isEmpty(self,pos):
        if not isinstance(pos, tuple) and not isinstance(pos, list):
            raise Exception("第一个参数被选为元组或列表")
        if pos[0] <= 0 or pos[0] > ChessBoard.BOAED_SIZE:
            raise Exception('下标越界')
        if pos[1] <= 0 or pos[1] > ChessBoard.BOAED_SIZE:
            raise Exception('下标越界')
        return self.getChess(pos)=='+'

