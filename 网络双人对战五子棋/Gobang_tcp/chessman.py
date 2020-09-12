import threading

class ChessMan(object):
    # 棋子类
    def __init__(self):
        self.__pos=[0,0]
        self.__color='+'
        self.con=threading.Condition()

    def NOTIFY(self):
        # 对notify进行封装
        self.con.acquire()
        self.con.notify()
        self.con.release()

    def WAIT(self):
        # 对wait进行封装
        self.con.acquire()
        self.con.wait()
        self.con.release()


    def setPos(self,pos):
        # 设置棋子位置
        self.__pos=pos

    def getPos(self):
        # 获取棋子位置
        return  self.__pos

    def setColor(self, color):
        # 设置棋子颜色
        self.__color = color

    def getColor(self):
        # 获取棋子颜色
        return self.__color

    # 装饰器,先return再setter
    @property
    def Pos(self):
        return self.__pos

    # 根据前面的方法命名
    @Pos.setter
    def Pos(self,pos):
        self.__pos=pos

    @property
    def Color(self):
        return  self.__color

    @Color.setter
    def Color(self,color):
        self.__color=color



