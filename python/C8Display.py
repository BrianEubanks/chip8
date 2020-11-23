#Brian Eubanks
#
#Chip8 Interpreter/Emulator
#Display

import tkinter as tk
from tkinter import *


class C8screen:




    def __init__(self):

        #Create Window & Canvas
        self.window = tk.Tk()
        self.window.title("CHIP8")
        self.window.resizable(False,False)
        self.w = Canvas(self.window, width=640, height=320, bg="black")
        self.w.pack()
    
        self.XSize=64
        self.YSize=32
    
        self.ScrBUF=[[0]*self.YSize for _ in range(self.XSize)]
        self.ScrDAT=[[0]*self.YSize for _ in range(self.XSize)]
        #Create Pixels

        
        for x in range(self.XSize):
            for y in range(self.YSize):
                self.ScrBUF[x][y]=self.w.create_rectangle(x*10,y*10,(x*10)+10,(y*10)+10, fill="black")
                self.ScrDAT[x][y]=x*y


    def updScr(self):
        self.window.update()







    #Draw Sprite S[K][8] to (X,Y)
    #Sprite Size is K bytes long - Height of sprite
    #Return Flag register VF
    def drawSprite(self, X, Y, S, K):
        vf = 0
        for n in range(K):            
            for xi in range(8):
                for yi in range(K):
                    if (S[yi][xi])==1 and self.ScrDAT[X+xi][Y+yi]==1:
                        self.ScrDAT[X+xi][Y+yi]=0;
                        self.w.itemconfig(self.ScrBUF[X+xi][Y+yi], fill='black')
                        #Set flag because a bit was cleared
                        vf = 1
                        pass
                    elif (S[yi][xi])==1:
                        #print('yes')
                        self.ScrDAT[X+xi][Y+yi]=1;
                        self.w.itemconfig(self.ScrBUF[X+xi][Y+yi], fill='green')

        return vf
        
        
