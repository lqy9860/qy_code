# -*- coding: utf-8 -*-
# @Time    : 2020/7/30 11:15
# @Author  : LQY
""" engine"""
import random
from chessman import *
import re
from chessboard import *

class Engine():
    def __init__(self,chessboard):
        self.__chessboard = chessboard

    def computerGo(self,chessman):
        '''
        电脑在随机位置下棋
        :param chessman: 棋子对象,里面已经设置好棋子颜色
        :return:
        '''
        if not isinstance(chessman,ChessMan):
            raise Exception('第一个参数必须为ChessMan对象')

        while True:
            # 电脑随机下棋
            posX = random.randint(1,15)
            posY = random.randint(1,15)
            # 判断位置是否为空
            if self.__chessboard.isEmpty((posX,posY)):
                print(f'电脑下棋的位置：({posX},{posY})')
                # 1如果下棋位置为空，则把位置写入棋子对象中
                chessman.setPos((posX,posY))
                # chessman.setColor('O')  # 设置电脑下白棋
                # 退出循环
                break

    # def userGo(self,chessman):
    #
    #     if not isinstance(chessman,ChessMan):
    #         raise Exception('第一个参数必须为ChessMan对象')
    #
    #     while True:
    #         pos = input("请输入pos:")
    #         posX = int(pos[0])  # 转换为整型
    #         posY = ord(pos[2])-ord('A') + 1  #转换成数字，注意pos[1]是‘,'
    #         # 判断位置是否为空
    #         if self.__chessboard.isEmpty((posX,posY)):
    #             print(f'人下棋的位置：({posX},{posY})')
    #             # 1如果下棋位置为空，则把位置写入棋子对象中
    #             chessman.setPos((posX,posY))
    #             chessman.setColor('X')
    #             # 退出循环
    #             break

    def userGo(self,chessman,userinput):
        '''
        人下棋
        :param chessman: 棋子对象
        :param userinput: 用户输入的字符串，如’5,A'
        :return:
        '''
        if not isinstance(chessman,ChessMan):
            raise Exception('第一个参数必须为ChessMan对象')

        # 采用正则表达式进行匹配，一位数1-9或者两位数：1[0-5]，要用括号括起来代表提取
        pattern = '^([1-9]|1[0-5]),([a-o])$'
        ret = re.findall(pattern,userinput)
        # print(ret)
        if re:  #判断是否匹配成功
            posX,posY = ret[0] #ret[0]是一个元组，把值依次传递
            posX = int(posX)
            posY = ord(posY)-ord('a')+1
            # 判断是否为空
            if self.__chessboard.isEmpty((posX, posY)):
                chessman.setPos((posX, posY))
                # chessman.setColor('X')
                return True
        # 没有匹配到或者位置不空
        return False

    def isWon(self,pos,color):
        '''
        判断当下某一颗棋子后是否赢棋
        :param pos:棋子的位置
        :param color:棋子的颜色
        :return:True为赢，False胜负未分
        '''
        if not isinstance(pos,tuple) and not isinstance(pos,list):
            raise Exception('第一个参数必须为元组或列表')   # 抛出异常
        if pos[0] <= 0 or pos[0] > ChessBoard.BOARD_SIZE:
            raise Exception('下标越界')
        if pos[1] <= 0 or pos[1] > ChessBoard.BOARD_SIZE:
            raise Exception('下标越界')

        # 上下方向: 范围（pos[0]-4,pos[1])--(pos[0] + 4,pos[1])
        start_x = 1
        end_x = ChessBoard.BOARD_SIZE
        if pos[0] - 4 >= 1:
            start_x = pos[0] - 4
        if pos[0] + 4 <= 15:
            end_x = pos[0] + 4

        count = 0
        for posX in range(start_x,end_x+1):
            if self.__chessboard.getChess((posX,pos[1])) == color:
                count += 1
                if count >= 5:
                    return True
            else:
                count = 0

        # 左右方向:范围（pos[0],pos[1]-4)--(pos[0],pos[1] + 4)
        start_y = 1
        end_y = self.__chessboard.BOARD_SIZE
        if pos[1] - 4 >= 1:
            start_y = pos[1] - 4
        if pos[1] + 4 <= 15:
            end_y = pos[1] + 4

        count = 0
        for posY in range(start_y,end_y+1):
            if self.__chessboard.getChess((pos[0],posY)) == color:
                count += 1
                if count >= 5:
                    return True
            else:
                count = 0

        # 左上右下
        count = 0
        s = pos[0] - pos[1]  #计算行列间的差值
        start = 0
        end = 0
        if pos[0] < pos[1]: #行比列小,s是负数,加在列
            # 设取点为（5,6），从1开始到14结束，循环14次
            start = 1
            end = 15 + s
        if pos[0] == pos[1]:  # 点都在对角线上，需要循环15次
            start = 1
            end = 15
        if pos[0] > pos[1]:  # 行比列大，s是正数,加在行
            # 设取点（6,5），从2开始，15结束，循环14次
            start = 1 + s
            end = 15
        for i in range(start,end+1):
            if self.__chessboard.getChess((i,i-s)) == color:
                count += 1
                if count >= 5:
                    return True
            else:
                count = 0

        # 左下右上
        count = 0
        s = pos[0] + pos[1]
        if s <= 16:
            # x+y<=16,设（5,6），循环10次，从1开始，到10,即(s-1)结束
            start = start_x
            end = s - start_y
            for i in range(start, end + 1):
                if self.__chessboard.getChess((i,s - i)) == color:
                    count += 1
                    if count >= 5:
                        return True
                else:
                    # 一旦断开 统计数清0
                    count = 0
        if 16 < s <= 26:
            # x+y > 16,设（11,10），循环10次，从6，即（s%16+1)开始，15结束，
            start = s % 16 + 1
            end = 15
            for i in range(start, end + 1):
                if self.__chessboard.getChess((i,s - i)) == color:
                    count += 1
                    if count >= 5:
                        return True
                else:
                    # 一旦断开 统计数清0
                    count = 0

        # 四个条件均不满足
        return False

    def isWonman(self,chessman):
        '''
        判断当下某一颗棋子后是否赢棋
        :param chessman: 棋子对象，包括位置颜色
        :return: True为赢，False胜负未分
        '''
        if not isinstance(chessman,ChessMan):
            raise Exception('第一个参数必须为ChessMan对象')

        pos = chessman.getPos()
        color = chessman.getColor()
        return self.isWon(pos,color)

    def play(self):
        '''游戏主流程'''
        userBlack = True   # 用户选择黑棋则为True 用户选择白棋则为False 每盘棋改变一次
        usergo = True    # 轮到用户下则为True 轮到电脑下则为False 每步棋改变一次

        chessmanUser = ChessMan()  # 创建棋子对象
        chessmanPc = ChessMan()
        while True:   # 外循环
            # 用户选择先后
            user_sort = input("用户选择先后：(b代表黑棋先下，w代表白棋后下)")
            if user_sort == 'b':
                userBlack = True
                usergo = True
            else:
                userBlack = False
                usergo = False

            # 初始化棋盘
            self.__chessboard.initBoard()
            # 方法不能直接Chessboard.initBoard(),因为定义的是实例方法，类只能用自己的类方法

            # 判断是否轮到用户下
            while True:  # 内循环
                # 如果用户选b,则用户先，下黑棋
                if userBlack:
                    chessmanUser.setColor('X')
                    chessmanPc.setColor('O')
                else:
                    chessmanUser.setColor('O')
                    chessmanPc.setColor('X')

                if usergo:  # 代表用户下
                    userinput = input("请用户输入下棋坐标:")
                    user_ret = self.userGo(chessmanUser, userinput)
                    if user_ret:
                        # 返回真才把棋子传进chessman，并放置在棋盘上
                        self.__chessboard.setChessMan(chessmanUser)
                else:  # 轮到电脑下
                    self.computerGo(chessmanPc)
                    self.__chessboard.setChessMan(chessmanPc)
                self.__chessboard.printBoard()

                # 判断输赢
                if usergo:
                    user_iswon = self.isWonman(chessmanUser)
                    if user_iswon:  # 如果赢了判断是否继续游戏
                        print("你赢了")
                        break  # 如果赢棋就跳出内循环
                else:
                    com_iswon = self.isWonman(chessmanPc)
                    if com_iswon:
                        print("你输了")
                        break  # 如果赢棋就跳出内循环

                usergo = not usergo

            # 判断是否继续游戏
            user_contin = input("是否继续游戏:(是为y,否为n):")
            if user_contin == 'n':
                print("结束游戏")
                break  # 结束游戏则跳出外循环
            else:
                print("继续游戏")






