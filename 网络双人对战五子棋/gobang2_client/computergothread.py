# -*- coding: utf-8 -*-
# @Time    : 2020/7/31 10:29
# @Author  : LQY
""" computergothread"""
import threading
from chessman import *
from engine import *
from chessboard import *
import re

class ComputerGoThread(threading.Thread):
    '''电脑下棋的线程'''

    def __init__(self,chessboard,chessmanUser,engine,client_socket):  # 服务端收发要用客户端的socket
        '''初始化'''
        super().__init__()
        self.chessboard = chessboard
        self.chessmanUser = chessmanUser
        self.engine = engine

        self.client_socket = client_socket



    def run(self):
        '''子线程执行的代码'''
        # address = ('', 9860)
        # self.server_socket.bind(address)  # 绑定服务端地址和端口号
        #
        # self.server_socket.listen(5)  # 监听，最大连接数5
        #
        # # 一直等待客户端连接，连接成功后则创建一个线程
        # client_socket, client_info = self.server_socket.accept()  # 申请连接
        # 连接服务端
        # address = ('192.168.55.29', 8000)  # 对手的ip地址和端口号
        # self.client_socket.connect(address)
        while True:


            # 1 电脑wait
            self.chessmanUser.doWait()

            # # 2 电脑下棋
            # self.engine.computerGo(self.chessmanPC)
            #
            # # 接收客户端发来的坐标信息
            # recv_pos = client_socket.recv(1024)
            # print("我是服务端，对方发过来的坐标是：",recv_pos.decode('gbk'))
            #
            # # self.chessboard.setChessMan(list(recv_pos.decode('gbk')))
            #
            # # 下完棋后给客户端发送坐标信息
            # ret = str(self.chessmanPC.getPos()).encode('gbk')
            # client_socket.send(ret)

            # 接收服务端发来的坐标信息
            recv_pos = self.client_socket.recv(1024).decode('gbk')
            pattern = '^([1-9]|1[0-5]),([a-o])$'
            ret = re.findall(pattern, recv_pos)
            # print(ret)
            if ret:  # 判断是否匹配成功
                posX, posY = ret[0]  # ret[0]是一个元组，把值依次传递
                posX = int(posX)
                posY = ord(posY) - ord('a') + 1
                # 判断是否为空
                if self.chessboard.isEmpty((posX, posY)):
                    self.chessmanUser.setPos((posX, posY))
                    # chessman.setColor('X')

            # 没有匹配到或者位置不空

            print("我是客户端，对方发过来的坐标是：", ret)


            # 3 电脑notify
            self.chessmanUser.doNotify()



