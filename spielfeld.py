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
        self.__schiffe = []

        SHIP1_IMAGE = pygame.image.load('resources/ship1_sunken.png')
        SHIP1 = pygame.transform.scale(SHIP1_IMAGE, (60, 180))

        SHIP2_IMAGE = pygame.image.load('resources/ship2_sunken.png')
        SHIP2 = pygame.transform.scale(SHIP2_IMAGE, (60, 240))

        SHIP3_IMAGE = pygame.image.load('resources/ship3_sunken.png')
        SHIP3 = pygame.transform.scale(SHIP3_IMAGE, (60, 240))

        SHIP4_IMAGE = pygame.image.load('resources/ship4_sunken.png')
        SHIP4 = pygame.transform.scale(SHIP4_IMAGE, (60, 300))

        self.__sunken_ship_images = [SHIP1, SHIP2, SHIP3, SHIP4]

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
        x, y = self.__pos

        length = len(self.__schiffe)
        if length > 0:
            for i in range(length):
                if self.istVersenkt(i):
                    xs = []
                    ys = []
                    for coord in self.__schiffe[i]:
                        xs.append(x + coord[0] * 60)
                        ys.append(y + coord[1] * 60)
                    rec_pos = (min(xs), min(ys))

                    if len(self.__schiffe[i]) == 3:
                        ship_rect_pic = self.__sunken_ship_images[0]
                    elif len(self.__schiffe[i]) == 4:
                        ship_rect_pic = self.__sunken_ship_images[2]
                    else:
                        ship_rect_pic = self.__sunken_ship_images[3]

                    if (max(xs) - min(xs)) > (max(ys)-min(ys)):
                        ship_rect_pic = pygame.transform.rotate(ship_rect_pic, 90)

                    ship_rect = ship_rect_pic.get_rect()
                    ship_rect.topleft = rec_pos[0], rec_pos[1]
                    self.__surface.blit(ship_rect_pic, ship_rect)

                    for coord in self.__schiffe[i]:
                        pygame.draw.rect(self.__surface, (200, 20, 20), (x + (coord[0]) * self.__groeße / 10, y + (coord[1]) * self.__groeße / 10, 61, 61), 3)

        for i in range(10):
            for j in range(10):
                a, b = self.__felder[i][j]
                if b == 1:
                    if a == 0:
                        pygame.draw.circle(self.__surface, (200, 200, 200),
                                           (x + (i + 0.5) * self.__groeße / 10, y + (j + 0.5) * self.__groeße / 10), 8)

                    if a == 1:
                        pygame.draw.line(self.__surface, (200, 20, 20),
                                         (x + i * self.__groeße / 10 + 3, y + j * self.__groeße / 10 + 3),
                                         (x + (i + 1) * self.__groeße / 10 - 3, y + (j + 1) * self.__groeße / 10 - 3),
                                         7)
                        pygame.draw.line(self.__surface, (200, 20, 20),
                                         (x + (i + 1) * self.__groeße / 10 - 3, y + j * self.__groeße / 10 + 3),
                                         (x + i * self.__groeße / 10 + 3, y + (j + 1) * self.__groeße / 10 - 3), 7)




        #pygame.display.update() # quatsch und schwachsinn

    def zeichneRandSchiffe(self):
        pass

    def setzeSchiffe(self,schiffe:[[(int,int)]]): 
        self.__felder = [[(0,0) for i in range(10)]for j in range(10)]
        for schiff in schiffe:
            for x,y in schiff:
                self.__felder[x][y] = (1,0)
        self.__schiffe = schiffe

    def setzeSchiff(self, alt_schiff:[(int, int)], neu_schiff:[(int, int)]):
        if alt_schiff:
            for x, y in alt_schiff:
                self.__felder[x][y] = (0, 0)
            if alt_schiff in self.__schiffe:
                self.__schiffe.remove(alt_schiff)
        if neu_schiff:
            for x, y in neu_schiff:
                self.__felder[x][y] = (1, 0)
            if not neu_schiff in self.__schiffe:
                self.__schiffe.append(neu_schiff)


    def gibSchiffe(self)->[[(int,int)]]:
        return self.__schiffe

    def sindVersenkt(self)->bool:
        for schiff in self.__schiffe:
            for coord in schiff: # maybe replace with lesser function
                if self.__felder[coord[0]][coord[1]][1] == 0:
                    return False
        return True

    def istVersenkt(self, id:int)->bool:
        for coord in self.__schiffe[id]:
            if self.__felder[coord[0]][coord[1]][1] == 0:
                return False
        return True


    
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
