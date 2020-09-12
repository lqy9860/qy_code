import socket
import threading
from chessboard import ChessBoard
from chessman import  ChessMan
from engine import Engine
from usergothread import RECV_UserGoThread,UserGoThread


if __name__ == '__main__':
    # tcp套接字
        server_socker = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # 绑定端口
        addr = ('', 8000)
        server_socker.bind(addr)

        # 开启监听
        server_socker.listen()
        print('开始准备,等待连接')
        # 接收客户端连接
        client_socker, client_info = server_socker.accept()
        print("客户端%s准备完毕" % client_info[0])
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

                # 客户端选择先手或后手
                # '先手1,后手其他:'
                print('对方(用户)选择先后手:', end='')
                order = client_socker.recv(1024).decode()
                Firstchessman.Color = 'o'
                Latterchessman.Color = 'x'
                if order == '1':
                    # 对方先手,开启用户接收线程
                    print('对方先手')
                    tU = RECV_UserGoThread(Firstchessman, engine, client_socker)
                    tC = UserGoThread(Latterchessman, engine, client_socker)
                else:
                    print('我方先手')
                    tU = UserGoThread(Firstchessman, engine, client_socker)
                    tC = RECV_UserGoThread(Latterchessman, engine, client_socker)

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
                    # 4.1电脑wait
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

                print("是否继续,继续选1(对方选择)")
                cont = client_socker.recv(1024).decode()
                if not (cont == '1'):
                    print('退出')
                    break
                else:
                    print('继续')
        except Exception as e:
            print(e)
            # print(client_info[0], "断开连接")
