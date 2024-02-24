#21.02.2024
#Gustav Freitag
#Klasse Spielfeld

import pygame
#import Schiffe

class Spielfeld:
    def __init__(self,pos:(int,int),surface)->"Spielfeld":
        self.__surface = surface
        self.__groeße = 600//1
        self.__pos = pos
        self.__felder = [[(0,0) for i in range(10)]for j in range(10)]  #(a,b): a-Schiff da?, b-bereits beschossen?
        #self.__schiffe = Schiffe()

    def gibPos(self)-> (int,int):
        return self.__pos

    def beschieße(self,feld:(int,int)):
        a = self.__felder[feld[0]][feld[1]][0]
        self.__felder[feld[0]][feld[1]] = (a,1)

    def istFrei(self,feld:(int,int))->bool: 
        #frei = True
        #for i in range(feld[0]-1,feld[0]+1):
        #    for j in range(feld[1]-1,feld[1]+1):
        #        if self.__felder[i][j][0]==1:
        #            frei = False
        #return frei
        return self.__felder[feld[0]][feld[1]][0]==0
        
    def zeichneBrett(self):
        
        x,y = self.__pos
        for i in range(10):
            for j in range (10):
                a,b = self.__felder[i][j]
                if b == 1:
                    if a == 0:
                        pygame.draw.circle(self.__surface,(200,200,200),(x+(i+0.5)*self.__groeße/10,y+(j+0.5)*self.__groeße/10),8)
                        
                    if a == 1:
                        pygame.draw.line(self.__surface,(255,20,20),(x+i*self.__groeße/10+4,y+j*self.__groeße/10+4),(x+(i+1)*self.__groeße/10-4,y+(j+1)*self.__groeße/10-4),3)
                        pygame.draw.line(self.__surface,(255,20,20),(x+(i+1)*self.__groeße/10-4,y+j*self.__groeße/10+4),(x+i*self.__groeße/10+4,y+(j+1)*self.__groeße/10-4),3)
        pygame.display.update()

    def zeichneRandSchiffe(self):
        pass

    def setzeSchiffe(self,schiffe:[[(int,int)]]): # ungenutzt
        self.__felder = [[(0,0) for i in range(10)]for j in range(10)]
        for schiff in schiffe:
            for x,y in schiff:
                self.__felder[x][y] = (1,0)
        #self.__schiffe.

    def setzteSchiff(self, alt_schiff:[(int, int)], neu_schiff:[(int, int)]):
        if alt_schiff:
            for x, y in alt_schiff:
                self.__felder[x][y] = (0, 0)
        if neu_schiff:
            for x, y in neu_schiff:
                self.__felder[x][y] = (1, 0)



    #def gibSchiffe(self)->[[(int,int)]]:
    #    return self.__schiffe.gibSchiffe()


#screen = pygame.display.set_mode((1920/2,1200/2))
#s = Spielfeld((192/2,120/2),screen)
#s.beschieße((0,0))
#s.beschieße((0,1))
#print(s.istFrei((1,1)))
#s.zeichneBrett()
#pygame.display.flip()

#screen = pygame.display.set_mode((1920, 1200))
#s = Spielfeld((192, 120), screen)
#s.setzteSchiff([(0, 1), (1, 1), (2, 1)])


'''felder = [[(0,0) for i in range(10)]for j in range(10)]
feld = (0,0)
a = felder[feld[0]][feld[1]][0]
felder[feld[0]][feld[1]] = (a,1)
print(felder)
'''
