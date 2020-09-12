import random
import re
from chessboard import ChessBoard
from chessman import  ChessMan


class Engine(object):
    def __init__(self,chessboard):
        self.__chessboard=chessboard

    def computerGo(self,chessman):
        if not isinstance(chessman,ChessMan):
            raise Exception('第一个参数必须为ChessMan对象')
        # 电脑随机下棋
        # 先判断是否为空
        while 1:
            posX=random.randint(1,15)
            posY=random.randint(1,15)
            # 如果为空,获取棋子位置并退出循环
            if self.__chessboard.isEmpty((posX,posY)):
                chessman.Pos=(posX,posY)
                print('电脑下棋位置:',posX,posY)
                break



    def userGo(self,chessman,userInput):
        if not isinstance(chessman,ChessMan):
            raise Exception('第一个参数必须为ChessMan对象')
        # 用户下棋
        # 正则表达式判断输入的格式 (1-15,a-o或1-15)
        pattern='^([1-9]|1[0-5]),([a-o]|[A-O]|[1-9]|1[0-5])$'
        ret=re.findall(pattern,userInput)
        if len(ret):
            posX,posY=ret[0]
            posX=int(posX)
            # 如果第二个参数是字母,进行转数字的处理
            if posY.isalpha() and ord(posY) >= 97:
                posY = ord(posY) - ord('a') + 1
            elif posY.isalpha() and ord(posY) >= 65:
                posY = ord(posY) - ord('A') + 1
            else:
                posY=int(posY)
            # 如果位置为空,设置棋子位置,并返回True
            if self.__chessboard.isEmpty((posX,posY)):
                chessman.Pos=(posX,posY)
                print('用户下棋位置:',posX, posY)
                return True

        return False


    def isWon(self,pos,color):
        if not isinstance(pos,tuple) and not isinstance(pos,list):
            raise Exception("第一个参数被选为元组或列表")
        if pos[0] <= 0 or pos[0]>ChessBoard.BOAED_SIZE:
            raise  Exception('下标越界')
        if pos[1] <= 0 or pos[1]>ChessBoard.BOAED_SIZE:
            raise  Exception('下标越界')
        # print("棋子位置",pos[0],pos[1])
        # 判断下某一颗棋子后是否赢
        # 上下
        count = 0
        # 开始标志
        startX=1
        if pos[0] -4>=1:
            startX=pos[0]-4

        # 结束标志
        endX=ChessBoard.BOAED_SIZE
        if pos[0] +4<=ChessBoard.BOAED_SIZE:
            endX=pos[0]+4
        #  posX范围
        for posX in range(startX,endX+1):
            if self.__chessboard.getChess((posX,pos[1]))==color :
                count +=1
                if count == 5:
                    return True
            else:
                count=0
        # 左右

        # 开始标志
        startY=1
        if pos[1] -4>=1:
            startY=pos[1]-4
        # 结束标志
        endY=ChessBoard.BOAED_SIZE
        if pos[1] +4<=ChessBoard.BOAED_SIZE:
            endY=pos[1]+4
        #  posY范围
        for posY in range(startY,endY+1):
            if self.__chessboard.getChess((pos[0],posY))==color :
                count +=1
                if count == 5:
                    return True
            else:
                count=0
        # 左上右下
        # 将棋盘划分为两部分,x>y和x<y
        # 开始标志
        startX=1
        if pos[0] >= pos[1] and pos[1]-4<=1  :
                startX=pos[0]-pos[1]+1
        elif pos[0] -4 >= 1 :
                startX = pos[0] - 4
        # 结束标志
        endX=ChessBoard.BOAED_SIZE
        if pos[0] <= pos[1] and pos[1]+4 >=ChessBoard.BOAED_SIZE:
            endX=15-(pos[1]-pos[0])
        elif pos[0] <=ChessBoard.BOAED_SIZE-4:
                endX = pos[0] + 4
        #  posX范围
        # print("左上右下范围",startX,endX)
        for posX in range(startX,endX+1):
            posY = pos[1] - (pos[0] - posX)
            # print(posX,posY)
            if self.__chessboard.getChess((posX,posY))==color :
                count +=1
                if count == 5:
                    return True
            else:
                count = 0
        # 左下右上
        # 将棋盘划分为两部分,(x+y>15)和(x+y<15)
        # 开始标志
        startX=1
        if pos[1]>=10  and  pos[0]+pos[1]>15:
                startX=pos[0]+pos[1]-15
        elif pos[0] - 4 >= 1 :
                startX = pos[0] - 4
        # 结束标志
        endX=ChessBoard.BOAED_SIZE
        if pos[1]<=5 and pos[0]+pos[1]<=15 :
            endX=pos[1] +pos[0]-1
        elif pos[0] +4<=ChessBoard.BOAED_SIZE:
                endX = pos[0] + 4
        #  posX范围
        # print("左下右上范围",startX,endX)
        for posX in range(startX,endX+1):
            posY = pos[1] + (pos[0] - posX)
            # print(posX,posY)
            if self.__chessboard.getChess((posX,posY))==color :
                count +=1
                if count == 5:
                    return True
            else:
                count=0
        return False

    def isWonMan(self,chessman):
        if not isinstance(chessman.Pos,tuple) and not isinstance(chessman.Pos,list):
            raise Exception("第一个参数被选为元组或列表")
        if chessman.Pos[0] <= 0 or chessman.Pos[0]>ChessBoard.BOAED_SIZE:
            raise  Exception('下标越界')
        if chessman.Pos[1] <= 0 or chessman.Pos[1]>ChessBoard.BOAED_SIZE:
            raise  Exception('下标越界')
        # 判断某一方下子后是否赢
        if not isinstance(chessman, ChessMan):
            raise Exception('第一个参数必须为ChessMan对象')

        pos=chessman.Pos
        color=chessman.Color
        return self.isWon(pos,color)



    def play(self):
        # 游戏主流程
        state=True
        # 外循环
        while 1:
            computerchessman = ChessMan()
            userchessman = ChessMan()
            # 用户选择先手或后手
            order=input('先手1,后手2:')
            if order=='1':
                # 初始化棋子类
                userchessman.Color = 'o'
                computerchessman.Color = 'x'
                state=True
            else:
                userchessman.Color = 'x'
                computerchessman.Color = 'o'
                state=False
            # 清空棋盘
            self.__chessboard.initBoard()
            # 内循环
            while 1:
                # 是否到用户下
                if state:
                    # 获取用户下棋位置
                    userInput = input("请输入用户下棋位置:")
                    ret=self.userGo(userchessman, userInput)
                    if ret:
                        # 放置用户下棋位置
                        self.__chessboard.setChessMan(userchessman)
                        # 打印棋盘
                        self.__chessboard.printBoard()

                        # 是否赢了
                        if self.isWonMan(userchessman):
                            # 退出外循环
                            print('uwin')
                            break
                        else:
                            state=False
                    else: continue
                # 电脑下
                else:
                    # 获取电脑随机下棋位置
                    self.computerGo(computerchessman)
                    # 放置电脑下棋位置
                    self.__chessboard.setChessMan(computerchessman)
                    # 打印棋盘
                    self.__chessboard.printBoard()
                    # 是否赢了
                    if self.isWonMan(computerchessman) :
                        # 退出外循环
                        print('cwin')
                        break
                    else:
                        state=True

            cont=input('是否继续(1继续)')
            #   是否继续
            if not (cont=='1'):
                break
