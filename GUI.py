# -*- coding: utf-8 -*-
# Copyright © 2015-2016 Jay Sinco -v python2.6

import pygame
from pygame.locals import *
import sys
import pickle


# 模块函数

def fromIntToBinary(num, Max):
    if 0 <= num <= Max -1:
        mode = [0] * Max
        mode[num] = 1
        return mode
    else:
        return []
    
class Block:
    def __init__(self, px, py, color=[122,197,205]):
        self.color = color
        self.px = px
        self.py = py
        self.clicked = False
        
    def draw(self):
        offset = 1
        pygame.draw.rect(Screen,self.color,[self.px+offset,self.py+offset,Side_Length-offset*2, Side_Length-offset*2], 0)

    def isClicked(self, mx, my):
        if (self.px<=mx<=self.px+Side_Length) and (self.py<=my<=self.py+Side_Length):                    
            return True
        else:
            return False

class BlockList:
    def __init__(self, Width_Num, Height_Num):
        self.blocks = [Block(w*Side_Length, H2+h*Side_Length) for w in range(Width_Num) for h in range(Height_Num)]

    def draw(self):
        for block in self.blocks:
            block.draw()

    def onMouseClick(self, mx, my, mouseState):        
        for block in self.blocks:
            if block.isClicked(mx, my):
                if mouseState == (1,0,0):
                    block.color = [255,0,0]   # 鼠标划过后block的颜色
                    block.clicked = True
                elif mouseState == (0,0,1):
                    block.color = [122,197,205]   # clear后block的颜色
                    block.clicked = False
                                       
    def onClear(self):
        for block in self.blocks:
            block.color = [122,197,205]
            block.clicked = False
    
    def blockStatue(self):
        statue = []
        for block in self.blocks:
            if block.clicked == True:
                statue.append(1)
            else:
                statue.append(0) 
        return statue   
            
        
               
def draw_word(text, pos=(0,0), size=16, color=(0,0,0)):
    font = pygame.font.SysFont("Consolas", size)
    Screen.blit(font.render(text, True, color), pos)
    
def draw_scene():
    pygame.draw.line(Screen,[0,0,0],[0,H2],[W1,H2],1)
    pygame.draw.line(Screen,[0,0,0],[0,H2+H1],[W1,H2+H1],1)
    pygame.draw.rect(Screen,[0,0,0],[0,0,Window_Width, Window_Height], 1)
    draw_word("Number :  %s"%(Character), [W1/100,H1+H2+H3/3], 16)
    draw_word("Character Recognition", [W1/15,H2/6], 30)
    Blocks.draw()
  
  
    
# 参数
Side_Length = 60     # 绘图区方格边长
Height_Num = 5     # 绘图区宽处方格个数
Width_Num = 5     # 绘图区横处方格个数
H1 = Side_Length * Height_Num
W1 = Side_Length * Width_Num
H2 = H1/10
H3 = H1/15
Window_Height = H1+H2+H3
Window_Width = W1
MouseHold = False     # 鼠标被按住
Blocks = BlockList(Width_Num, Height_Num)   # 构造block集
Character = ""    # 当前字符


# pygame 初始化
pygame.init()
pygame.display.set_caption('Character Recognition')
Screen = pygame.display.set_mode((Window_Width, Window_Height), 0, 32)
print '''
********** GUIDE *******************
*  <Space>  =>  Clear drawing all  *
*  <Enter>  =>  Write mode file    *
*  <Letter> =>  Number for now     *
*  <leftM>  =>  draw               *
*  <rightM> =>  undraw             *
************************************
'''
  
# 事件循环

Data_File = open('Train_data.txt', 'w')
Character = ""
Target = -1

while True:
    for event in pygame.event.get():        
        if event.type == QUIT:
            sys.exit()       
        if event.type ==  MOUSEBUTTONDOWN:
            MouseHold = True                
        if event.type ==  MOUSEBUTTONUP:
            MouseHold = False            
        if event.type == MOUSEMOTION:
            if MouseHold:
                Blocks.onMouseClick(event.pos[0], event.pos[1], pygame.mouse.get_pressed())               
        if event.type == KEYDOWN:            
            if event.key == K_SPACE:
                Blocks.onClear()
            if 48 <= event.key <= 57:
                Target = event.key - 48
                Character = "%s" %(str(Target))
            if event.key == K_RETURN:
                BsL = []
                BsL.append(Blocks.blockStatue())
                BsL.append(fromIntToBinary(Target, 3))
                pickle.dump(BsL, Data_File, 0)
                print "Dump into file => ", BsL
                                                                
    Screen.fill((255, 255, 255))
    draw_scene()    
    pygame.display.update()


Data_File.close()



































    
    
