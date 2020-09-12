from chessboard import ChessBoard
from chessman import  ChessMan
from engine import Engine
from usergothread import UserGoThread
from computergothread import ComputerGoThread

def test1():
    # 初始化棋盘
    chessboard = ChessBoard()
    chessboard.initBoard()
    chessboard.printBoard()

def test2():
    # 初始化棋盘
    chessboard = ChessBoard()
    chessboard.initBoard()
    # 在3,5位置放置x
    chessboard.setChess((3,5),'x')

    # 用棋子类在4,7放置o
    # 初始化棋子类
    chessman=ChessMan()
    chessman.Pos=(4,7)
    chessman.Color='o'
    # 放置
    chessboard.setChessMan(chessman)

    chessboard.printBoard()
    # 测试获取指定棋子位置
    ret=chessboard.getChess((4,11))
    print(ret)
    # 测试是否为空
    ret=  chessboard.isEmpty((1,1))
    print(ret)

def test3():
    # 初始化棋盘
    chessboard = ChessBoard()
    chessboard.initBoard()
    # 初始化棋子类
    chessman=ChessMan()
    chessman.Color='o'

    # 初始化引擎类
    engine=Engine(chessboard)
    # 获取电脑随机下棋位置
    engine.computerGo(chessman)
    # 放置电脑下棋位置
    chessboard.setChessMan(chessman)
    # 打印棋盘
    chessboard.printBoard()


def test4():
    # 初始化棋盘
    chessboard = ChessBoard()
    chessboard.initBoard()
    # 初始化棋子类
    chessman=ChessMan()
    chessman.Color='o'

    # 初始化引擎类
    engine=Engine(chessboard)
    # 获取用户下棋位置
    userInput=input("请输入用户下棋位置:")

    engine.userGo(chessman,userInput)
    # 放置用户下棋位置
    chessboard.setChessMan(chessman)
    # 打印棋盘
    chessboard.printBoard()


def test5():
    # 初始化棋盘
    chessboard = ChessBoard()
    chessboard.initBoard()
    # 初始化棋子类
    chessman=ChessMan()
    chessman.Color='o'

    # 初始化引擎类
    engine=Engine(chessboard)

    while 1:
        # 获取用户下棋位置
        userInput=input("请输入用户下棋位置:")

        engine.userGo(chessman,userInput)
        # 放置用户下棋位置
        chessboard.setChessMan(chessman)
        # 打印棋盘
        RET=engine.isWonMan(chessman)
        chessboard.printBoard()

        if RET:
            print('win')
            break


def main():
    # 初始化棋盘
    chessboard = ChessBoard()
    chessboard.initBoard()
    # 初始化引擎类
    engine = Engine(chessboard)
    engine.play()


def mainThread():
    # 初始化棋盘
    chessboard = ChessBoard()
    chessboard.initBoard()
    # 初始化引擎类
    engine = Engine(chessboard)
    userchessman = ChessMan()
    userchessman.Color='x'
    computerchessman = ChessMan()
    computerchessman.Color = 'o'
    # 创建线程和开启线程
    tU=UserGoThread(userchessman,engine)
    tC=ComputerGoThread(computerchessman,engine)
    # z设置守护线程,主线程退出,子线程自动退出
    tU.setDaemon(True)
    tC.setDaemon(True)
    tU.start()
    tC.start()
    while 1:

        #1.用户wait
        userchessman.WAIT()
        #2.用户下子
        # 放置用户下棋位置
        chessboard.setChessMan(userchessman)
        # 打印棋盘
        chessboard.printBoard()
        # 判断用户是否赢
        if engine.isWonMan(userchessman):
            print("u win")
            break
        #3.电脑notify
        computerchessman.NOTIFY()
        # 电脑子线程自动完成
        #4.1电脑wait
        computerchessman.WAIT()
        #5.1电脑下子
        # 放置电脑下棋位置
        chessboard.setChessMan(computerchessman)
        # 打印棋盘
        chessboard.printBoard()
        # 判断电脑是否赢
        if engine.isWonMan(computerchessman):
            print("c win")
            break
        #6.1用户notify
        userchessman.NOTIFY()
        # 用户子线程自动完成

if __name__ == '__main__':
    # mainThread()
    test5()