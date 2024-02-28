# Autor: Gustav Freitag
# Datum: 21.02.2024
# Zweck: Klasse Spielfeld

import pygame


class Spielfeld:
    """Vor.: -pos- ist eine Position (x,y) auf dem Bildschirm. -surface- ist die Surface der Anwendung.
    Eff.: Das Spielfeld ist leer und hat die Größe 600.
    Erg.: Eine Instanz der Klasse spielfeld ist geliefert."""
    def __init__(self,pos:(int,int),surface)->"Spielfeld":
        self.__surface = surface
        self.__groeße = 600
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
        """Vor.: -
        Eff.: -
        Erg.: Die Position des Bretts ist geliefert (oben, links)."""
        return self.__pos

    def beschieße(self,feld:(int,int)):
        """Vor.: -feld- ist eine Koordinate auf dem Spielbrett.
        Eff.: Das Feld ist mit der Koordinate -feld- ist als beschossen abgespeichert.
        Erg.: -"""
        a = self.__felder[feld[0]][feld[1]][0]
        self.__felder[feld[0]][feld[1]] = (a,1)

    def istFrei(self,feld:(int,int))->bool:
        """Vor.: -feld- ist eine Koordinate auf dem Spielbrett.
        Eff.: -
        Erg.: Es ist geliefert, ob das Feld mit den Koordinaten -feld- frei ist."""
        return self.__felder[feld[0]][feld[1]][0]==0
        
    def zeichneBrett(self):
        """Vor.: -
        Eff.: Das Spielbrett ist auf dem Bildschirm gezeichnet, jedoch nicht angezeigt.
        Erg.: -"""
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


    def setzeSchiffe(self,schiffe:[[(int,int)]]):
        """Vor.: -schiffe- ist eine Liste mit Listen von Koordinaten der Schiffe. Das Spielfeld ist leer.
        Eff.: Die Positionen der Schiffe sind abgespeichert.
        Erg.: -"""
        self.__felder = [[(0,0) for i in range(10)]for j in range(10)]
        for schiff in schiffe:
            for x,y in schiff:
                self.__felder[x][y] = (1,0)
        self.__schiffe = schiffe

    def setzeSchiff(self, alt_schiff:[(int, int)], neu_schiff:[(int, int)]):
        """Vor.: -alt_schiff- ist eine Liste der Koordinaten eines Schiffes, -neu_schiff- ist ebenfalls eine Liste mit Koordinaten.
        Eff.: Das Schiff liegt nun auf den Koordinaten -neu_schiff-, die Koordinaten -alt_schiff- sind leer.
        Erg.: -"""
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
        """Vor.: -
        Eff.: -
        Erg.: Eine Liste mit Listen der Koordinaten aller Schiffe ist geliefert."""
        return self.__schiffe

    def sindVersenkt(self)->bool:
        """Vor.: -
        Eff.: -
        Erg.: Es ist geliefert, ob alle Schiffe auf dem Spielbrett versenkt sind."""
        for schiff in self.__schiffe:
            for coord in schiff:
                if self.__felder[coord[0]][coord[1]][1] == 0:
                    return False
        return True

    def istVersenkt(self, id:int)->bool:
        """Vor.: -id- ist eine natürliche Zahl kleiner oder gleich 4.
        Eff.: -
        Erg.: Es ist geliefert, ob das Schiff mit der Id -id- versenkt ist."""
        for coord in self.__schiffe[id]:
            if self.__felder[coord[0]][coord[1]][1] == 0:
                return False
        return True
