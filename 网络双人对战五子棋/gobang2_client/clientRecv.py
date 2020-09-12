# -*- coding: utf-8 -*-
# @Time    : 2020/8/1 12:58
# @Author  : LQY
""" clientserverRecv"""
import threading
from chessman import *
from engine import *
from chessboard import *
import re

class ClientRecvThread(threading.Thread):
    def __init__(self,chessboard,chesswhite,engine,client_socket):  # 服务端收发要用客户端的socket
        '''初始化'''
        super().__init__()
        self.chessboard = chessboard
        self.chesswhite = chesswhite
        self.engine = engine
        self.client_socket = client_socket

    def run(self):
        # 等待主线程唤醒
        self.chesswhite.doWait()

        while True:
            # 接收服务端发来的坐标信息
            recv_pos = self.client_socket.recv(1024).decode('gbk')
            pattern = '^([1-9]|1[0-5]),([a-o]|[A-O]|[1-9]|1[0-5])$'
            ret = re.findall(pattern, recv_pos)
            if len(ret):
                posX, posY = ret[0]
                posX = int(posX)
                # 如果第二个参数是字母,进行转数字的处理
                if posY.isalpha() and ord(posY) >= 97:
                    posY = ord(posY) - ord('a') + 1
                elif posY.isalpha() and ord(posY) >= 65:
                    posY = ord(posY) - ord('A') + 1
                else:
                    posY = int(posY)

                # 判断是否为空
                if self.chessboard.isEmpty((posX, posY)):
                    self.chesswhite.setPos((posX, posY))
            print("对方发过来的坐标是：", ret)

            # 3 电脑notify
            self.chesswhite.doNotify()

            # 1 电脑wait
            self.chesswhite.doWait()


