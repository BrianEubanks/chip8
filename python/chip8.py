#Brian Eubanks
#
#Chip8 Interpreter/Emulator


from os import path
import sys
import numpy as np

from time import sleep

import C8Display as d


class chip8:

    #Initialize Chip8
    def __init__(self, f):
        
        self.romfile=""
        #Main Memory
        self.MM = np.empty(4096, dtype=np.uint8)
        for i in range(4096):
            self.MM[i]=0
        #Registers V
        self.V = np.empty(4096, dtype=np.uint8)
        for i in range(16):
            self.V[i]=0
        #PC Start at 0x200
        self.PC = 0x200
        #Setup STack 
        self.stack = np.empty(16, dtype=np.uint8)
        self.SP = 0
        #Index
        self.I = 0
        #Timers
        self.DT = 0
        self.ST = 0

        #self.scr=d.screen()
        self.open()
        

    #Load RomFile to memory at Address 0x200
    def open(self):
        with open(romfile,"r") as f:
        #Read Rom File
        #Flip to Big Endian
            word = np.fromfile(f,dtype=np.uint8).newbyteorder()
        a = 0
        while a < len(word):
            #print(format(i,'04x'))
            self.MM[a+0x200] = word[a]
            a+=1


    #Do this better Maybe
    #Get each bit from the sprite byte and store in a list
    def byteConvert(self,sprite):
        pixels=[]
        for index in range(8):
            pixels.append(sprite%2)
            sprite=sprite>>1
        #print(pixels)
        #Have to reverse the list do display properly :)
        return pixels[::-1]
    




print(sys.argv)
print(len(sys.argv))




#Check File Arguments for RomFile

romfile = "ibmlogo.ch8"

c8 = chip8(romfile)
scr = d.C8screen()


while True:

    scr.updScr()

    #Fetch
    instruction=c8.MM[c8.PC]<<8
    c8.PC+=1
    instruction+=c8.MM[c8.PC]
    c8.PC+=1

    print(format(c8.PC-2,'03x')+": "+format(instruction,'04x'))
    

    # 0xGHJK
    # 0x-NNN
    # 0x--NN
    

    G = (instruction >> 12) % 0x10
    H = (instruction >> 8) % 0x10
    J = (instruction >> 4) % 0x10
    K = instruction % 0x10

    NN = instruction % 0x100
    NNN= instruction % 0x1000
    
    #print("Format: "+format(G,'01x')+format(H,'01x')+format(J,'01x')+format(K,'01x'))
    #print("Format: "+format(NNN,'03x')+" - " +format(NN,'02x'))

    

    #change to switch
    #00E0
    #CLS
    if(instruction == 0x00E0):
        #w.create_rectangle(0,0,640,320, fill="black")
        #for x in range(scr.XSize):
        #    for y in range(scr.YSize):
        #        scr.ScrDAT[x][y]=0
        pass
    #1NNN
    #JMP NNN
    elif(G==1):
        c8.PC=NNN
    #2NNN
    #Call NNN
    elif (G==2):
        c8.stack[SP]=PC
        c8.SP+=1
        c8.PC=NNN
    #00EE
    #RET
    elif (instruction == 0x00EE):
        c8.PC=c8.stack[SP]
        c8.SP-=1
    
        print(format(instruction,'04x'))

    #6XNN
    #Load x, NN
    elif(G==6):
        c8.V[H]=NN

    #7XNN
    #Add x, NN
    elif(G==7):
        c8.V[H]+=NN

    #ANNN
    #Ld I, NNN
    elif(G==0xA):
        I=NNN

    #DXYN
    #Display
    elif(G==0xD):

        #Get XY Coords
        xcoord = c8.V[H]%64
        ycoord = c8.V[J]%64
        
        #Get Sprite Data from pixels
        sprite = []
        for n in range(K):
            sprite.append(c8.byteConvert(c8.MM[I+n]))

        c8.V[0xF]=scr.drawSprite(xcoord,ycoord,sprite,K)
        

    
    sleep(.016)
    





                
    
           
            
                           

           
           
        
        


        
