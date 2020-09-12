import pygame
import time
def isWon():
    bcolor=[(250, 198, 115, 255),(250, 199, 108, 255),(249, 201, 101, 255)]
    wcolor = [(195, 164, 142, 255), ]
if __name__ == '__main__':

    # 初始化
    pygame.init()

    #创建窗口(必须)
    # set_mode会返回一个Surface对象，代表了在桌面上出现的那个窗口，三个参数第一个为元祖，代表分 辨率（必须）；第二个是一个标志位，具体意思见下表，如果不用什么特性，就指定0；第三个为色深。
    # RESIZABLE	创建一个可以改变大小的窗口
    screen=pygame.display.set_mode((500,481),pygame.RESIZABLE,32)
    # 每格大小33x32

    #获取背景图片
    background_img=pygame.image.load(r'H:\pei_xun_python\wenjiang\0730\wzq\img\board.jpg')

    # 设置时钟
    clock = pygame.time.Clock()
    # 棋子颜色切换
    chess_state=True
    i=0
    # 棋子图片字典
    w={}
    b={}
    # 棋子位置存储
    setwX=[]
    setwY=[]
    setbX=[]
    setbY=[]
    while True:
        # 监听事件
        for event in pygame.event.get():
            # 设置退出事件
            if event.type== pygame.QUIT:
                exit()

        # 设置背景图片位置
        screen.blit(background_img, (0, 0))
        w [i]= pygame.image.load(r'H:\pei_xun_python\wenjiang\0730\wzq\img\w_chess.png')
        b [i]=pygame.image.load(r'H:\pei_xun_python\wenjiang\0730\wzq\img\b_chess.png')
        x,y=pygame.mouse.get_pos()
        # 如果chess_state为True,白棋,否则黑棋
        if chess_state:
            screen.blit(w[0],(x-16.5,y-16))
        else:
            screen.blit(b[0], (x-16.5,y-16))
        # 获取键盘事件
        key = pygame.key.get_pressed()
        # 按下Enter键放置棋子
        if key[pygame.K_RETURN or pygame.K_SPACE]:
            x-=x%33 -5
            y-=y%32
            # 如果为True,白棋位置增加,否则黑棋位置增加
            if chess_state:
                setwX.append(x)
                setwY.append(y)
                print(setwX[len(setwX) - 1], setwY[len(setwX) - 1], i)
            else:
                setbX.append(x)
                setbY.append(y)
                print(setwX[len(setbX) - 1], setwY[len(setbX) - 1], i)
            chess_state=not chess_state
            col = screen.get_at((x, y))
            print(col)
            i+=1
            time.sleep(0.5)



        for j in range(len(setwX)):
            screen.blit(w[j],(setwX[j],setwY[j]))

        for j in range(len(setbX)):
            screen.blit(b[j],(setbX[j],setbY[j]))


        #刷新画面
        pygame.display.flip()
        # 设置刷新频率,每秒刷新n次
        clock.tick(10)

