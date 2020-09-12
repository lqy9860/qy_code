# -*- coding: utf-8 -*-
# @Time    : 2020/7/30 9:21
# @Author  : LQY
""" chessboard"""

from chessman import *

class ChessBoard(object):
    # 类属性
    BOARD_SIZE = 15 # 棋盘的大小

    def __init__(self):
        # 棋盘的下标从0到15，申请内存
        self.__board = [[0 for i in range(ChessBoard.BOARD_SIZE+1)]
                        for i in range(ChessBoard.BOARD_SIZE+1)]


    def initBoard(self):
        '''清空棋盘'''

        #直接忽略第0行
        for i in range(1,ChessBoard.BOARD_SIZE+1):
            # 直接忽略第0列
            for j in range(1, ChessBoard.BOARD_SIZE + 1):
                self.__board[i][j] = '+'

    def printBoard(self):
        '''打印棋盘'''

        # 打印列号
        print('  ',end='')
        for j in range(1, ChessBoard.BOARD_SIZE + 1):
            c = chr(j + ord('a')-1)  #转换成字母ABCD...
            print(c,end=' ')
        print()

        # 打印整个棋盘
        for  i in range(1,ChessBoard.BOARD_SIZE + 1):
            # 打印行号
            print('%2d' %i,end='')
            for j in range(1, ChessBoard.BOARD_SIZE + 1):
                print(self.__board[i][j],end=' ')
            print()

    def setChess(self,pos,color):
        '''
        在棋盘上放置棋子
        :param pos: 棋子的位置，该值是一个长度为2的元组
        :param color: 棋子的颜色‘x'或’o'
        :return:
        '''
        if not isinstance(pos,tuple) and not isinstance(pos,list):
            raise Exception('第一个参数必须为元组或列表')   # 抛出异常
        if pos[0] <= 0 or pos[0] > ChessBoard.BOARD_SIZE:
            raise Exception('下标越界')
        if pos[1] <= 0 or pos[1] > ChessBoard.BOARD_SIZE:
            raise Exception('下标越界')

        self.__board[pos[0]][pos[1]] = color  # 放置棋子


    def setChessMan(self,chessman):
        '''
        在棋盘上放置棋子
        :param chessman: 棋子对象，需要包含棋子颜色和位置
        :return:
        '''
        if not isinstance(chessman,ChessMan):
            raise Exception('第一个参数必须为ChessMan对象')

        pos = chessman.getPos()  #接收棋子对象的位置
        color = chessman.getColor()  # 接收棋子对象的颜色
        self.setChess(pos,color)

    def getChess(self,pos):
        '''
        根据坐标读取棋子
        :param pos: 棋子的位置
        :return: 棋子的颜色；x或o或+
        '''
        if not isinstance(pos,tuple) and not isinstance(pos,list):
            raise Exception('第一个参数必须为元组或列表')   # 抛出异常
        if pos[0] <= 0 or pos[0] > ChessBoard.BOARD_SIZE:
            raise Exception('下标越界')
        if pos[1] <= 0 or pos[1] > ChessBoard.BOARD_SIZE:
            raise Exception('下标越界')

        return self.__board[pos[0]][pos[1]]

    def isEmpty(self,pos):
        '''
        判断某个坐标点是否为空
        :param pos: 坐标位置
        :return: True空，False不空
        '''
        if not isinstance(pos,tuple) and not isinstance(pos,list):
            raise Exception('第一个参数必须为元组或列表')   # 抛出异常
        if pos[0] <= 0 or pos[0] > ChessBoard.BOARD_SIZE:
            raise Exception('下标越界')
        if pos[1] <= 0 or pos[1] > ChessBoard.BOARD_SIZE:
            raise Exception('下标越界')

        return self.getChess(pos) == '+'