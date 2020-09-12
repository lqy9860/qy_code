# -*- coding: utf-8 -*-
# @Time    : 2020/7/30 9:27
# @Author  : LQY
""" main"""
from chessboard import *
from chessman import *
from engine import *
import threading
import time
import random

def test1():
    chessboard = ChessBoard()
    chessboard.initBoard()
    chessboard.printBoard()

def test2():
    chessboard = ChessBoard()  # 创建棋盘类对象
    chessman = ChessMan()  # 创建棋子类对象

    # 清空棋盘
    chessboard.initBoard()
    # 在（3,5）位置上放一颗黑棋
    chessboard.setChess((3,5),'X')

    # 在（4,7）位置放一颗白棋
    chessman.setPos((4,7))
    chessman.setColor('O')
    chessboard.setChessMan(chessman)
    chessboard.printBoard()

    # 测试读取棋子
    ret = chessboard.getChess((4,5))
    print(ret)

    # 测试是否为空
    ret = chessboard.isempty((4,14))
    if ret:
        print('empty')
    else:
        print('not empty')

def test3():
    '''测试电脑下棋'''
    chessboard = ChessBoard()  # 创建棋盘类对象
    chessman = ChessMan()  # 创建棋子类对象
    engine = Engine(chessboard)  #创建引擎对象，并把棋盘传进去

    # 清空棋盘
    chessboard.initBoard()

    # 电脑下棋
    engine.computerGo(chessman)  # 已将电脑的下棋位置传入chessman中
    chessboard.setChessMan(chessman)  # 棋盘把棋子放进对应位置

    # 人下棋
    while True:
        userinput = input("请输入下棋坐标:")
        ret = engine.userGo(chessman, userinput)
        if ret:
            # 返回真才把棋子传进chessman
            chessboard.setChessMan(chessman)
            # 打印棋盘
            # chessboard.printBoard()
            break

    # 打印棋盘
    chessboard.printBoard()

def test4():
    '''测试人下棋'''
    chessboard = ChessBoard()  # 创建棋盘类对象
    chessman = ChessMan()  # 创建棋子类对象
    engine = Engine(chessboard)  # 创建引擎对象，并把棋盘传进去

    # 清空棋盘
    chessboard.initBoard()

    # 人下棋
    userinput = input("请输入下棋坐标:")
    ret = engine.userGo(chessman,userinput)
    if ret:
        # 返回真才把棋子传进chessman
        chessboard.setChessMan(chessman)
        # 打印棋盘
        chessboard.printBoard()

def test5():
    '''测试上下方向'''
    chessboard = ChessBoard()  # 创建棋盘类对象
    chessman = ChessMan()  # 创建棋子类对象
    engine = Engine(chessboard)

    # 清空棋盘
    chessboard.initBoard()

    chessboard.setChess((3, 5), 'X')
    chessboard.setChess((4, 5), 'X')
    chessboard.setChess((5, 5), 'X')
    chessboard.setChess((6, 5), 'X')
    chessboard.setChess((7, 5), 'X')
    # chessboard.setChess((8, 5), 'X')
    #
    # 打印棋盘
    chessboard.printBoard()

    # 判断输赢
    ret = engine.isWon((3,5),'X')
    if ret:
        print("胜负已分")
    else:
        print("胜负未分")

def test6():
    '''测试左右方向'''
    chessboard = ChessBoard()  # 创建棋盘类对象
    chessman = ChessMan()  # 创建棋子类对象
    engine = Engine(chessboard)

    # 清空棋盘
    chessboard.initBoard()

    chessboard.setChess((1, 1), 'X')
    chessboard.setChess((1, 2), 'X')
    # chessboard.setChess((1, 3), 'X')
    chessboard.setChess((1, 4), 'X')
    chessboard.setChess((1, 5), 'X')
    # chessboard.setChess((8, 5), 'X')
    #
    # 打印棋盘
    chessboard.printBoard()

    # 判断输赢
    ret = engine.isWon((1, 5), 'X')
    if ret:
        print("胜负已分")
    else:
        print("胜负未分")

# def main():
#     chessboard = ChessBoard()
#     engine = Engine(chessboard)
#     engine.play()

from usergothread import *
from computergothread import *
import socket
from clientRecv import *

def mainThread():

    # 创建客户端套接字
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # 创建服务端套接字
    # server_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # computergothread = ComputerGoThread(chessboard,chessmanPC,engine,client_socket)

    # 连接服务端
    address = ('192.168.55.29', 8000)  # 对手的ip地址和端口号
    client_socket.connect(address)

    while True:
        # 创建棋盘对象和引擎对象
        chessboard = ChessBoard()
        engine = Engine(chessboard)

        # 初始化和打印棋盘
        chessboard.initBoard()
        chessboard.printBoard()

        # 创建两个棋子对象
        chessblack = ChessMan()
        chesswhite = ChessMan()

        chessblack.setColor('X')  # 先手为黑棋
        chesswhite.setColor('O')  # 后手为白棋

        # 判断先后
        user_sort = input("请输入先后手：先为1")
        # 把先后信息发给对方
        msg = user_sort.encode('gbk')
        client_socket.send(msg)

        if user_sort == '1':
            # 若选1，则自己下黑棋
            # 把黑棋对象传给下棋进程，白棋对象传给接收线程
            # 创建用户下棋线程和接收线程
            print("我方先手")
            # 创建客户端下棋线程，传入chessblack唤醒UserGoThread
            usergothread = UserGoThread(chessblack, engine, client_socket)
            # 创建客户接收线程
            clientrecvthread = ClientRecvThread(chessboard, chesswhite, engine, client_socket)

        else:
            # 若选0，则自己下白棋
            # 把白棋对象传给下棋线程，黑棋对象传给接收线程
            print("对方先手")
            usergothread = UserGoThread(chesswhite, engine, client_socket)
            clientrecvthread = ClientRecvThread(chessboard, chessblack, engine, client_socket)  # 传入chessmanUser唤醒ClientRecvThread

        # 设置线程为守护线程，当主线程退出时子线程也随之退出
        usergothread.setDaemon(True)
        # computergothread.setDaemon(True)
        clientrecvthread.setDaemon(True)

        # 开始线程
        usergothread.start()
        # computergothread.start()
        clientrecvthread.start()

        # 先手（黑棋）notify
        # 若选1，唤醒usergothread中的wait
        # 若选0，唤醒clientrecvthread中的wait
        chessblack.doNotify()

        while True:
            # 1 用户wait
            chessblack.doWait()

            # 3 在棋盘上摆放用户下的棋子
            chessboard.setChessMan(chessblack)
            chessboard.printBoard()

            # 判断输赢
            if user_sort == '1':
                if engine.isWonman(chessblack):
                    print("恭喜赢了")
                    break
            if user_sort == '0':
                if engine.isWonman(chessblack):
                    print("输了")
                    break

            # 2 对方notify,唤醒客户端接收线程，接收对方的棋子
            chesswhite.doNotify()

            # 4 电脑wait
            chesswhite.doWait()

            # 5 在棋盘上摆放对方下的棋子
            chessboard.setChessMan(chesswhite)
            chessboard.printBoard()

            if user_sort == '1':
                if engine.isWonman(chesswhite):
                    print("输了")
                    break
            if user_sort == '0':
                if engine.isWonman(chesswhite):
                    print("恭喜赢了")
                    break

            # 6 用户notify
            chessblack.doNotify()

        # 是否继续游戏
        userinput = input("是否继续游戏：是为1,否为0")
        # 把是否继续信息发给对方
        msg = userinput.encode('gbk')
        client_socket.send(msg)
        if userinput == '0':
            break


if __name__=='__main__':
    # test2()
    # test3()
    # test4()
    # test5()
    # test6()
    # main()
    mainThread()
