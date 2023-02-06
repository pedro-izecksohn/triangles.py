from math import pi, sin, cos
from os import urandom
import pygame
from pygame.locals import QUIT
import random

degree=pi/90
scrwidth=1024
scrheight=768
bgcolor=(0,0,0)
color=(0,255,0)

class Line:
    def __init__(self, a, b):
        self.a=a
        self.b=b
    def getList(self):
        width=self.b[0]-self.a[0]
        height=self.b[1]-self.a[1]
        length=((width*width)+(height*height))**(1/2)
        ws=width/length
        hs=height/length
        ret=[]
        n=0
        while n<length:
            ret.append((int(self.a[0]+(ws*n)), int(self.a[1]+(hs*n))))
            n+=1
        return ret

class Triangle:
    CLOCKWISE=1
    COUNTERCLOCKWISE=0
    def __init__(self, centerx, centery, ray=50, mainangle=0, rotdir=CLOCKWISE):
        self.centerx=centerx
        self.centery=centery
        self.ray=ray
        self.mainangle=mainangle
        self.rotdir=rotdir
    def getA(self):
        x=(cos(self.mainangle)*self.ray)+self.centerx
        y=(sin(self.mainangle)*self.ray)+self.centery
        return (x,y)
    def getB(self):
        angle=self.mainangle+(degree*60)
        x=(cos(angle)*self.ray)+self.centerx
        y=(sin(angle)*self.ray)+self.centery
        return (x,y)
    def getC(self):
        angle=self.mainangle-(degree*60)
        x=(cos(angle)*self.ray)+self.centerx
        y=(sin(angle)*self.ray)+self.centery
        return (x,y)
    def getAllPoints(self):
        ret=[]
        a=self.getA()
        b=self.getB()
        c=self.getC()
        ab=Line(a,b)
        ac=Line(a,c)
        bc=Line(b,c)
        ret.extend(ab.getList())
        ret.extend(ac.getList())
        ret.extend(bc.getList())
        return ret
    def rotate (self):
        if self.rotdir==Triangle.CLOCKWISE:
            self.mainangle+=degree
        else:
            self.mainangle-=degree
    def walk(self):
        self.centerx+=(urandom(1)[0]%3)-1
        self.centery+=(urandom(1)[0]%3)-1
        if self.centerx+self.ray<0:
            self.centerx+=1
        if self.centerx-self.ray>scrwidth:
            self.centerx-=1
        if self.centery+self.ray<0:
            self.centery+=1
        if self.centery-self.ray>scrheight:
            self.centery-=1

def getTriangles(n):
    ret=[]
    while len(ret)<n:
        ret.append(Triangle(random.randrange(scrwidth),random.randrange(scrheight),rotdir=urandom(1)[0]%2))
    return ret

def main():
    pygame.init()
    surface = pygame.display.set_mode((scrwidth, scrheight))
    clock = pygame.time.Clock()
    triangles=getTriangles(3)
    while True:
        for ev in pygame.event.get():
            if ev.type == QUIT:
                pygame.quit()
        clock.tick(60)
        surface.fill(bgcolor)
        for t in triangles:
            t.rotate()
            t.walk()
            for p in t.getAllPoints():
                surface.set_at(p, color)
        pygame.display.flip()

main()
