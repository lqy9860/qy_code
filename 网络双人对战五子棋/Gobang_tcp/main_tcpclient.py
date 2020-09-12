import socket
import threading
from chessboard import ChessBoard
from chessman import  ChessMan
from engine import Engine
from usergothread import RECV_UserGoThread,UserGoThread


if __name__ == '__main__':
    # tcp套接字
        client_socker = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        addr = ('192.168.55.29', 8000)
        # 连接
        client_socker.connect(addr)
        try:
            while 1:
                # 初始化棋盘
                chessboard = ChessBoard()
                chessboard.initBoard()
                # 初始化引擎类
                engine = Engine(chessboard)
                # 初始化两个棋子类
                Firstchessman = ChessMan()
                Latterchessman = ChessMan()

                Firstchessman.Color = 'o'
                Latterchessman.Color = 'x'
                # 客户端选择先手或后手
                # '先手1,后手其他:'
                select1=input('选择先后手(1为先手):')
                client_socker.send(select1.encode())

                if select1 == '1':
                    print('我方先手')
                    tU = UserGoThread(Firstchessman, engine, client_socker)
                    tC = RECV_UserGoThread(Latterchessman, engine, client_socker)
                else:
                    # 对方先手,开启用户接收线程
                    print('对方先手')
                    tU = RECV_UserGoThread(Firstchessman, engine, client_socker)
                    tC = UserGoThread(Latterchessman, engine, client_socker)

                # 设置守护线程,主线程退出,子线程自动退出
                tU.setDaemon(True)
                tC.setDaemon(True)
                tU.start()
                tC.start()
                # 先手notify一下
                Firstchessman.NOTIFY()

                while 1:
                    # 1.先手等待
                    Firstchessman.WAIT()
                    # 2.先手下子
                    # 放置先手下棋位置
                    chessboard.setChessMan(Firstchessman)
                    # 打印棋盘
                    chessboard.printBoard()
                    # 判断先手是否赢
                    if engine.isWonMan(Firstchessman):
                        print("先手 win")
                        break
                    # 3.后手notify
                    Latterchessman.NOTIFY()
                    # 后手子线程自动完成
                    # 4.1后手wait
                    Latterchessman.WAIT()
                    # 5.1后手下子
                    # 放置对方下棋位置
                    chessboard.setChessMan(Latterchessman)
                    # 打印棋盘
                    chessboard.printBoard()
                    # 判断后手是否赢
                    if engine.isWonMan(Latterchessman):
                        print("后手 win")
                        break
                    # 6.1先手notify
                    Firstchessman.NOTIFY()
                    # 用户子线程自动完成

                print("是否继续,继续选1")
                select2=input('是否继续(1继续):')
                client_socker.send(select2.encode())
                if not (select2 == '1'):
                    print('退出')
                    break
                else:
                    print('继续')
        except Exception as e:
            print(e)
            # print(client_info[0], "断开连接")
