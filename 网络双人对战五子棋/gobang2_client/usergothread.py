# -*- coding: utf-8 -*-
# @Time    : 2020/7/31 10:29
# @Author  : LQY
""" usergothread"""
import threading
from chessman import *
from engine import *
from chessboard import *


class UserGoThread(threading.Thread):
    '''用户下棋的线程'''

    def __init__(self,chessblack,engine,client_socket):
        '''初始化'''
        super().__init__()
        self.chessblack = chessblack
        self.engine = engine
        self.client_socket = client_socket


    def run(self):
        '''子线程执行的代码'''

        # 等待主线程唤醒
        self.chessblack.doWait()

        while True:
            # 1 用户下棋
            userinput = input("请用户输入下棋坐标:")
            ret = self.engine.userGo(self.chessblack,userinput)
            if ret:
                # 给服务端发消息说我方已下完棋，轮到对方下棋
                # 向服务器发送信息，并传递我方下的棋子的坐标
                print("我是客户端，我方已下完棋")
                # self.client_socket.send(msg.encode('gbk'))
                ret = self.chessblack.getPos()
                msg = str(ret[0])+str(',')+str(ret[1])
                self.client_socket.send(msg.encode('gbk'))

                # 2 用户notify
                self.chessblack.doNotify()

                # 3 用户wait
                self.chessblack.doWait()
            else:
                print("下棋重复")

