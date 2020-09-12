import threading
import time
import re

class RECV_UserGoThread(threading.Thread):
    def __init__(self,chessman,engine,client_socker):
        super().__init__()
        self.chessman=chessman
        self.engine=engine
        self.client_socker=client_socker
        self.con=threading.Condition()


    def run(self):
        # 先等待,解决先后手问题
        self.chessman.WAIT()
        try:
            while 1:
                # 1.用户下棋
                print('轮到对方下棋')
                # 获取用户下棋位置
                recv_data = self.client_socker.recv(1024).decode('gbk')
                print('对方下棋位置:',recv_data)
                if len(recv_data) != 0 and recv_data != None:
                    # 正则表达式判断输入的格式 (1-15,a-o或1-15)
                    pattern = '^([1-9]|1[0-5]),([a-o]|[A-O]|[1-9]|1[0-5])$'
                    ret = re.findall(pattern, recv_data)
                    # print(ret)
                    if len(ret):
                        posX, posY = ret[0]
                        posX = int(posX)
                        # 如果第二个参数是字母,进行转数字的处理
                        if posY.isalpha() and ord(posY)>=97 :
                            posY = ord(posY) - ord('a') + 1
                        elif posY.isalpha() and ord(posY)>=65:
                            posY = ord(posY) - ord('A') + 1
                        else:
                            posY = int(posY)
                self.chessman.Pos = (posX, posY)
                # 2.notify
                self.chessman.NOTIFY()
                # 3.wait
                self.chessman.WAIT()
        except Exception as e:
            print(e)


class UserGoThread(threading.Thread):
    def __init__(self,chessman,engine,client_socker):
        super().__init__()
        self.chessman=chessman
        self.engine=engine
        self.client_socker=client_socker
        self.con=threading.Condition()


    def run(self):
        # 先等待,解决先后手问题
        self.chessman.WAIT()
        try:
            while 1:
                # time.sleep(1)
                print('轮到我方下棋')
                # 1.用户下棋
                # 获取用户下棋位置
                userInput = input("请输入下棋位置:")
                ret=self.engine.userGo(self.chessman, userInput)
                if ret:
                    # 发送棋子坐标
                    self.client_socker.send(userInput.encode('gbk'))
                    # 2.notify
                    self.chessman.NOTIFY()
                    # 3.wait
                    self.chessman.WAIT()
                else:
                    print('输入格式错误或棋子重复')
        except Exception as  e:
            print(e)
