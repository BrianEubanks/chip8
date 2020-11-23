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
        
        self.romfile=f
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

        self.scr=d.C8screen()
        self.open()
        

    #Load RomFile to memory at Address 0x200
    def open(self):
        with open(self.romfile,"r") as f:
        #Read Rom File
        #Flip to Big Endian
            word = np.fromfile(f,dtype=np.uint8).newbyteorder()
        a = 0
        while a < len(word):
            #print(format(i,'04x'))
            self.MM[a+0x200] = word[a]
            a+=1


    #Fetch next instruction at PC
    #Increment Program Counter
    #Returns the instruction
    def fetch(self):
    
        instruction=self.MM[self.PC]<<8
        self.PC+=1
        instruction+=self.MM[self.PC]
        self.PC+=1

        #print(format(c8.PC-2,'03x')+": "+format(instruction,'04x'))
        return instruction
        
        

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
    



    def tick(self):

        #Fetch Instruction
        #Increment PC
        instruction = self.fetch()


        #Decode & Execute
    
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

    
        #00E0
        #CLS
        if(instruction == 0x00E0):
            self.scr.cls()


        #1NNN
        #JMP NNN
        elif(G==1):
            self.PC=NNN


        #2NNN
        #Call NNN
        elif (G==2):
            self.stack[SP]=PC
            self.SP+=1
            self.PC=NNN


        #00EE
        #RET
        elif (instruction == 0x00EE):
            self.SP-=1
            self.PC=self.stack[SP]
    
            #print(format(instruction,'04x'))


        #6XNN
        #Load x, NN
        elif(G==6):
            self.V[H]=NN


        #7XNN
        #Add x, NN
        elif(G==7):
            self.V[H]+=NN


        #ANNN
        #Ld I, NNN
        elif(G==0xA):
            self.I=NNN


        #DXYN
        #Display
        elif(G==0xD):

            #Get XY Coords
            xcoord = self.V[H]%64
            ycoord = self.V[J]%64
        
            #Get Sprite Data from pixels
            sprite = []
            for n in range(K):
                sprite.append(self.byteConvert(self.MM[self.I+n]))

            self.V[0xF]=self.scr.drawSprite(xcoord,ycoord,sprite,K)


        

    #Delay
    #sleep(.010)

    #Try to updateScreen
    #If the window is closed exit
        return self.scr.updScr()
    
   



def main(argv):
    #print(argv[0])
    #Try to load file from argument
    #It not found use ibmlogo
    romfile = "ibmlogo.ch8"
    if (len(argv)>0):
        if(path.exists(argv[0])):
            romfile = argv[0]
        
    c8 = chip8(romfile)


    while c8.tick():
        #c8.scr.updScr()
        #print(c8.PC)
        pass
    
        

if __name__ == "__main__":
    main(sys.argv[1:])

                
    
           
            
                           

           
           
        
        


        
