import threading
import re

class ComputerGoThread(threading.Thread):
    def __init__(self, chessman, engine,client_socker):
        super().__init__()
        self.chessman = chessman
        self.engine = engine
        self.client_socker=client_socker
        self.con = threading.Condition()

    def run(self):
        while 1:
            # 1.wait
            self.chessman.WAIT()
            # 2.电脑下棋
            self.engine.computerGo(self.chessman)
            # 发送棋子位置
            msg = str(self.chessman.Pos[0]) + str(',') + str(self.chessman.Pos[1])
            self.client_socker.send(msg.encode('gbk'))
            # 3.notify
            self.chessman.NOTIFY()




class RECV_ComputerGoThread(threading.Thread):
    def __init__(self,chessman,engine,client_socker):
        super().__init__()
        self.chessman=chessman
        self.engine=engine
        self.client_socker=client_socker
        self.con=threading.Condition()

    def run(self):
        while 1:
            # 1.wait
            self.chessman.WAIT()
            # 2.接收电脑下棋
            recv_data = self.client_socker.recv(1024).decode('gbk')
            if len(recv_data) != 0 and recv_data != None:
                # 正则表达式判断输入的格式 (1-15,a-o或1-15)
                pattern = '^([1-9]|1[0-5]),([a-o]|[1-9]|1[0-5])$'
                ret = re.findall(pattern, recv_data)
                print(ret)
                if len(ret):
                    posX, posY = ret[0]
                    posX = int(posX)
                    # 如果第二个参数是字母,进行转数字的处理
                    if posY.isalpha():
                        posY = ord(posY) - ord('a') + 1
                    else:
                        posY = int(posY)
                    # print(posX,posY)
            self.chessman.Pos = (posX, posY)
            # 3.notify
            self.chessman.NOTIFY()
