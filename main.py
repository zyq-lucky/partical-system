import tkinter as tk
from PIL import Image, ImageTk
from time import time, sleep
import random
import math
import pygame

colors = ['red',  'yellow', 'white', 'orange','blue','pink','purple']
# 定义重力加速度
g = 0.08

# 定义2019烟花粒子的类
class Particle2019:
    h = 1
    a = 1
    vx = 0
    vy = 0
    # 定义粒子初始化函数
    def __init__(self, cv, nid,total,v,size,color, px=0,py=0,lifetime = 80):
        # id表示在每簇烟花中的不同粒子
        self.nid = nid
        # total表示每簇烟花的粒子总数
        self.total = total
        # px，py表示粒子的位置信息
        self.px = px
        self.py = py
        # vx，vy表示粒子的速度信息
        self.v = v
        self.vy1 = math.sin(math.radians(self.nid / self.total * 360)) * self.v # 烟花获得的初速度
        self.vx1 = random.uniform(0.1, 0.2)
        self.vy0 = math.sin(math.radians(self.nid / self.total * 360)) * self.v
        self.vx0 = 0.6 * math.cos(math.radians(self.nid / self.total * 360)) * self.v
        self.vy91 = 0.6 * math.sin(math.radians(self.nid / self.total * 360)) * self.v
        self.vx91 = 0.5 * math.cos(math.radians(self.nid / self.total * 360)) * self.v
        self.vx92 = 0.5 * math.cos(math.radians(self.nid / self.total * 120)) * self.v
        self.vy92 = 1.2 * math.sin(math.radians(self.nid / self.total * 120)) * self.v
        # 定义数字字样‘2’的绘制初速度
        self.vx21 = 0.9 * math.cos(math.radians(-90+self.nid / self.total * 180)) * self.v
        self.vy21 = 0.9 * math.sin(math.radians(-90+self.nid / self.total * 180)) * self.v
        self.vx22 = 1.2 * math.cos(math.radians(-90+self.nid / self.total * 180)) * self.v
        self.vy22 = 0.9 * self.v
        # size表示粒子的大小
        self.size = size
        # size表示粒子的颜色
        self.color = color
        # lifetime表示粒子的生命周期
        self.lifetime = lifetime
        # 初始化粒子在画布中的对象
        self.cv = cv
        self.object1 = self.cv.create_oval(px - size, py - size, px + size, py + size, fill=self.color)
        self.object0 = self.cv.create_oval(px - size-90, py - size, px + size-90, py + size, fill=self.color)
        self.object91 = self.cv.create_oval(px - size + 90, py - size-10, px + size + 90, py + size-10, fill=self.color)
        self.object92 = self.cv.create_oval(px - size + 90, py - size-10, px + size + 90, py + size-10 ,
                                            fill=self.color)
        self.object21 = self.cv.create_oval(px - size - 200, py - size, px + size -200, py + size,
                                            fill=self.color)
        self.object22 = self.cv.create_oval(px - size - 200, py - size, px + size - 200, py + size,
                                            fill=self.color)


    # 定义绘制新一帧时，粒子更新函数
    def update(self):
        self.lifetime -= self.h
        # 若粒子处于烟花绽放阶段
        if self.lifetime > 0:
            tx1 = self.vx1 * self.h
            ty1 = self.vy1 * self.h
            self.vy1 = self.vy1 + g * self.h
            self.cv.move(self.object1,tx1,ty1)
            tx0 = self.vx0 * self.h
            ty0 = self.vy0 * self.h
            self.vy0 = self.vy0 + g * self.h
            self.cv.move(self.object0, tx0, ty0)
            tx91 = self.vx91 * self.h
            ty91 = self.vy91 * self.h
            self.vy91 = self.vy91 + g * self.h
            self.cv.move(self.object91, tx91, ty91)
            tx92 = self.vx92 * self.h
            ty92 = self.vy92 * self.h
            self.vy92 = self.vy92 + g * self.h
            self.cv.move(self.object92, tx92, ty92)

            tx21 = self.vx21 * self.h
            ty21 = self.vy21 * self.h
            self.vy21 = self.vy21 + g * self.h
            self.cv.move(self.object21, tx21, ty21)
            tx22 = self.vx22 * self.h
            ty22 = self.vy22 * self.h
            self.vy22 = self.vy22 + g * self.h
            self.cv.move(self.object22, tx22, ty22)
            # 若生命周期已结束
        elif self.lifetime <= 0:
            self.cv.delete(self.object1)
            self.cv.delete(self.object0)
            self.cv.delete(self.object91)
            self.cv.delete(self.object92)
            self.cv.delete(self.object21)
            self.cv.delete(self.object22)
# 定义普通烟花的类
class Particle:
    h = 1
    # 定义粒子初始化函数
    def __init__(self, cv, nid,total,v,size,color, px,py,lifetime,boomtime):
        # nid表示在每簇烟花中的不同粒子
        self.nid = nid
        # total表示每簇烟花的粒子总数
        self.total = total
        # px，py表示粒子的初始位置信息
        self.px = px
        self.py = py
        # vx，vy表示粒子的速度信息
        self.v = v # 烟花获得的初速度
        self.vx = math.cos(math.radians(self.nid / self.total * 360)) * self.v
        self.vy = math.sin(math.radians(self.nid / self.total * 360)) * self.v
        # size表示粒子的大小
        self.size = size
        # size表示粒子的颜色
        self.color = color
        # lifetime表示粒子的生命周期
        self.lifetime = lifetime
        # boomtime表示粒子开始爆炸的时间
        self.boomtime = boomtime
        # 初始化粒子在画布中的对象
        self.cv = cv


    # 定义绘制新一帧时，粒子更新函数
    def update(self):
        self.lifetime -= self.h
        self.boomtime -= self.h
        if self.boomtime == 0:
            self.object = self.cv.create_oval(self.px -self.size, self.py - self.size, self.px + self.size,
                                              self.py + self.size, fill=self.color)
            return
        # 若粒子处于烟花绽放阶段
        if self.lifetime > 0 and  self.boomtime <0:
            tx = self.vx * self.h
            ty = self.vy * self.h
            self.vy = self.vy + g * self.h
            self.cv.move(self.object,tx,ty)
            # 若生命周期已结束
        elif self.lifetime <= 0:
            self.cv.delete(self.object)

#

#  定义循环函数
def system(cv):
    for n in range(3):
        # 随机生成烟花的z总个数
        num = random.randint(4, 8)
        all = []  # 表示所有烟花的所有粒子
        for i in range(num - 1):
            parts = []  # 表示一簇烟花的所有粒子
            # 随机生成每簇烟花的初始位置
            px = random.randint(50, 850)
            py = random.randint(50, 200)
            # 随机生成每簇烟花的粒子总个数
            total = random.randint(30, 50)
            # 随机生成烟花的颜色
            color = random.choice(colors)
            # 随机生成烟花的初速度
            v = random.uniform(1.5, 3)
            # 随机生成烟花爆炸的时间点
            boomtime = random.randint(1, 20)
            for j in range(total):
                for m in range(4):
                    # 每簇烟花内的粒子速度略有不同
                    vn = random.uniform(0.4, 1.0)
                    # 随机生成生命周期
                    lifetime = random.randint(30, 80)
                    # 初始化粒子
                    p = Particle(cv, j + 1, total, v * vn, 2, color, px, py, lifetime,boomtime)
                    parts.append(p)
            all.append(parts)

        # 更新绘制
        pygame.mixer.music.play()
        total_time = 80
        while total_time > 0:
            sleep(0.01)
            for a in all:
                for p in a:
                    p.update()
            cv.update()
            total_time = total_time - 1
    # 绘制 2019 烟花
    parts = []  # 表示一簇烟花的所有粒子
    # 随机烟花的初始位置
    px = 500
    py = 150
    # 随机生成每簇烟花的粒子总个数
    total = random.randint(30, 50)
    color = random.choice(colors)
    v = random.uniform(2, 3)
    for j in range(total):
        for m in range(2):
            vn = random.uniform(0.9, 1.0)
            lifetime = random.randint(20, 50)
            p = Particle2019(cv, j + 1, total, v * vn, 2, color, px, py, lifetime)
            parts.append(p)
    total_time = 80
    pygame.mixer.music.play()
    while total_time > 0:
        sleep(0.01)
        for p in parts:
            p.update()
        cv.update()
        total_time = total_time - 1
    root.after(1, system, cv)

# def close(*ignore):
#     """退出程序、关闭窗口"""
#     global root
#     root.quit()

if __name__ == '__main__':
    root = tk.Tk()
    cv = tk.Canvas(root, height=600, width=900)
    # 选一个好看的背景会让效果更惊艳！
    image = Image.open("./backgroud.jpg")
    photo = ImageTk.PhotoImage(image)
    #
    cv.create_image(0, 0, image=photo, anchor='nw')
    cv.pack()
    pygame.mixer.init()
    track2 = pygame.mixer.music.load("sound.wav")

    root.after(10, system, cv)
    root.mainloop()
