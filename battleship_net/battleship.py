# Autor: Ivaylo Staykov
# Datum: 21.02.2024
# Zweck: Hauptdatei des SWP und Klasse Battleship


import pygame
pygame.init()
#from Sekretaer import *
from spielfeld import Spielfeld


class Battleship:
    def __init__(self, surface):
        self.__surface = surface
        self.__msf = Spielfeld((192//1, 120//1), self.__surface)  # //2 for smaller display
        self.__gsf = Spielfeld((1127//1, 120//1), self.__surface) # --------"---------
        self.__ships = [] # rectangles
        self.__ship_images = []



        text = ""
        run = True
        troll = False
        while run:
            screen.blit(BACKGROUND, (0, 0))
            draw_text('Schiffe Versenken', font1, (40, 140, 40), 500, 200)
            draw_text('pc-nummer des gegners:', font2, (40, 140, 40), 540, 600)
            draw_text(text, font2, (40, 140, 40), 1320, 600)
            if troll:
                draw_text('unbekannte pc-nummer', font2, (40, 140, 40), 540, 800)
                draw_text('bitte versuche erneut', font2, (40, 140, 40), 540, 880)
            for event in pygame.event.get():
                # handle text input
                if event.type == pygame.TEXTINPUT:
                    if len(text) < 5:
                        text += event.text

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]

                    elif event.key == pygame.K_RETURN:
                        if text.isnumeric() and (1 <= int(text) <= 25):
                            self.__pcnummer = int(text)
                            run = False

                        else:
                            troll = True


                if event.type == pygame.QUIT:
                    pygame.quit()

            pygame.display.update()

        # !!! TO-DO:
        # self.__sek = Sekretaer(self.__pcnummer)
        # gegnerIP = "10.16.102." + str(self.__pcnummer)
        # self.__k = Kanaele(gegnerIP, 55555)


    def aufbauPhase(self):
        def get_snapped_ship(snapship):
            x, y = snapship.center
            if (snapship.height != 240) and (snapship.width != 240):
                snap_x = (x - 192) // 60  # //30 for smaller displays
                snap_y = (y - 120) // 60
                snapship.center = 222 + (snap_x) * 60, 150 + (snap_y) * 60
            elif snapship.height == 240:
                snap_x = (x - 192) // 60  # //30 for smaller displays
                snap_y = (y - 120 - 30) // 60
                snapship.center = 222 + (snap_x) * 60, 180 + (snap_y) * 60
            else:
                snap_x = (x - 192 - 30) // 60  # //30 for smaller displays
                snap_y = (y - 120) // 60
                snapship.center = 252 + (snap_x) * 60, 150 + (snap_y) * 60
            return snapship

        def get_border_coordinates(rectangle_coords):
            border_coords = set()
            for x, y in rectangle_coords:
                # Check the top, bottom, left, and right neighbors
                top = (x, y - 1)
                bottom = (x, y + 1)
                left = (x - 1, y)
                right = (x + 1, y)
                topleft = (x - 1, y - 1)
                topright = (x + 1, y - 1)
                bottomleft = (x - 1, y + 1)
                bottomright = (x + 1, y + 1)
                # Add neighbors to the set
                for coord in [top, bottom, left, right, topleft, topright, bottomleft, bottomright]:
                    if (0 <= coord[0] <= 9) and (0 <= coord[1] <= 9):
                        border_coords.add(coord)
            return list(border_coords)

        def get_ship_squares(ship):
            ship_squares = []
            x0, y0 = ship.topleft
            x_pos, y_pos = (x0 - 192) // 60, (y0 - 120) // 60
            if ship.height <= 60:
                for i in range(ship.width // 60):
                    ship_squares.append((x_pos + i, y_pos))
            else:
                for i in range(ship.height // 60):
                    ship_squares.append((x_pos, y_pos + i))

            return ship_squares

        # load ships (pixel-values for big screen)
        SHIP0_IMAGE = pygame.image.load('resources/ship1.png')
        SHIP0 = pygame.transform.scale(SHIP0_IMAGE, (60, 180))

        SHIP1_IMAGE = pygame.image.load('resources/ship1.png')
        SHIP1 = pygame.transform.scale(SHIP1_IMAGE, (60, 180))

        SHIP2_IMAGE = pygame.image.load('resources/ship2.png')
        SHIP2 = pygame.transform.scale(SHIP2_IMAGE, (60, 240))

        SHIP3_IMAGE = pygame.image.load('resources/ship3.png')
        SHIP3 = pygame.transform.scale(SHIP3_IMAGE, (60, 240))

        SHIP4_IMAGE = pygame.image.load('resources/ship4.png')
        SHIP4 = pygame.transform.scale(SHIP4_IMAGE, (60, 300))

        ship_images = [SHIP0, SHIP1, SHIP2, SHIP3, SHIP4]
        ship_positions = [(250, 800), (350, 800), (450, 800), (550, 800), (650, 800)]

        ship0 = SHIP0.get_rect()
        ship0.topleft = ship_positions[0]

        ship1 = SHIP1.get_rect()
        ship1.topleft = ship_positions[1]

        ship2 = SHIP2.get_rect()
        ship2.topleft = ship_positions[2]

        ship3 = SHIP3.get_rect()
        ship3.topleft = ship_positions[3]

        ship4 = SHIP4.get_rect()
        ship4.topleft = ship_positions[4]

        ships = [ship0, ship1, ship2, ship3, ship4]

        # Bereit-Button
        pygame.font.init()
        surf = font2.render('bereit', True, (220, 220, 220))
        button = pygame.Rect(815, 600, 230, 67)

        active_ship = None
        run = True
        clock = pygame.time.Clock()
        while run:
            draw_window()
            draw_text('aufbauphase', font2, (40, 100, 40), 750, 20)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    all_placed = True
                    for ship in ships:
                        x1, y1 = ship.topleft
                        x2, y2 = ship.bottomright
                        if not((172 < x1 < 813) and (100 < y1 < 741) and (172 < x2 < 813) and (100 < y2 < 741)):
                            all_placed = False

                    if button.collidepoint(event.pos) and all_placed:
                        run = False
                        # !!! TO-DO:
                        # - senden des eigenen Spielfelds an den Gegner
                        # - empfangen des gegnerischen Spielfelds

                    if event.button == 1:
                        for num in range(len(ships)):
                            if ships[num].collidepoint(event.pos):
                                active_ship = num

                    elif event.button == 3:
                        for num in range(len(ships)):
                            if ships[num].collidepoint(event.pos):
                                active_ship = num

                    if active_ship != None:
                        x1, y1 = ships[active_ship].topleft
                        x2, y2 = ships[active_ship].bottomright
                        if (172 < x1 < 813) and (100 < y1 < 741) and (172 < x2 < 813) and (100 < y2 < 741):
                            snapped_ship = get_snapped_ship(ships[active_ship])
                            old_ship_squares = get_ship_squares(snapped_ship)
                            self.__gsf.setzteSchiff(old_ship_squares, None) # !!! must be changed to self.__msf
                        else:
                            old_ship_squares = None

                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        if active_ship != None:
                            x1, y1 = ships[active_ship].topleft
                            x2, y2 = ships[active_ship].bottomright
                            if (172<x1<813) and (100<y1<741) and (172<x2<813) and (100<y2<741):
                                squares_free = True
                                snapped_ship = get_snapped_ship(ships[active_ship])
                                new_ship_squares = get_ship_squares(snapped_ship)
                                potential_squares = get_border_coordinates(new_ship_squares)
                                for coord in potential_squares:
                                    if not (self.__gsf.istFrei(coord)): # !!! must be changed to self.__msf
                                        squares_free = False

                                if squares_free:
                                    ships[active_ship] = snapped_ship
                                    self.__gsf.setzteSchiff(old_ship_squares, new_ship_squares)  # !!! must be changed to self.__msf
                                else: # redundancy
                                    if ships[active_ship].height <= 60:
                                        ship_images[active_ship] = pygame.transform.rotate(ship_images[active_ship], 90)
                                        new_ship = ship_images[active_ship].get_rect()
                                        new_ship.topleft = ships[active_ship].topleft
                                        ships[active_ship] = new_ship
                                    ships[active_ship].topleft = ship_positions[active_ship]
                            else:
                                if ships[active_ship].height <= 60:
                                    ship_images[active_ship] = pygame.transform.rotate(ship_images[active_ship], 90)
                                    new_ship = ship_images[active_ship].get_rect()
                                    new_ship.topleft = ships[active_ship].topleft
                                    ships[active_ship] = new_ship
                                ships[active_ship].topleft = ship_positions[active_ship]


                            active_ship = None

                    elif event.button == 3:
                        if active_ship != None:
                            x1, y1 = ships[active_ship].topleft
                            x2, y2 = ships[active_ship].bottomright
                            if (172 < x1 < 813) and (100 < y1 < 741) and (172 < x2 < 813) and (100 < y2 < 741):
                                pot_ship_image = pygame.transform.rotate(ship_images[active_ship], 90)
                                pot_new_ship = pot_ship_image.get_rect()
                                pot_new_ship.topleft = ships[active_ship].topleft

                                squares_free = True
                                snapped_ship = get_snapped_ship(pot_new_ship)
                                new_ship_squares = get_ship_squares(snapped_ship)
                                potential_squares = get_border_coordinates(new_ship_squares)
                                for coord in potential_squares:
                                    if not (self.__gsf.istFrei(coord)):
                                        squares_free = False

                                for x, y in new_ship_squares:
                                    if not((0 <= x <= 9) and (0 <= y <= 9)):
                                        squares_free = False

                                if squares_free:
                                    ship_images[active_ship] = pygame.transform.rotate(ship_images[active_ship], 90)
                                    new_ship = ship_images[active_ship].get_rect()
                                    new_ship.topleft = ships[active_ship].topleft
                                    ships[active_ship] = new_ship
                                    self.__gsf.setzteSchiff(old_ship_squares, new_ship_squares)  # must be changed to self.__msf

                            active_ship = None

                if event.type == pygame.MOUSEMOTION:
                    if active_ship != None:
                        ships[active_ship].move_ip(event.rel)

            # grey outline
            if active_ship != None:
                x1, y1 = ships[active_ship].topleft
                x2, y2 = ships[active_ship].bottomright
                if (172 < x1 < 813) and (100 < y1 < 741) and (172 < x2 < 813) and (100 < y2 < 741):
                    snapped_rect = get_snapped_ship(ships[active_ship].copy())
                    w, h = snapped_rect.width, snapped_rect.height
                    x, y = snapped_rect.topleft
                    outline = pygame.Rect(x, y, w, h)
                    pygame.draw.rect(self.__surface, (100, 100, 100), outline)

            # draw ships
            for i in range(len(ships)):
                self.__surface.blit(ship_images[i], ships[i])
                pygame.draw.rect(self.__surface, "green", ships[i], 1) # optional

            # draw button
            a, b = pygame.mouse.get_pos()
            if button.x <= a <= button.x + 230 and button.y <= b <= button.y + 67:
                pygame.draw.rect(screen, (60, 150, 60), button)
            else:
                pygame.draw.rect(screen, (40, 100, 40), button)
            self.__surface.blit(surf, (button.x+17, button.y+7))

            pygame.display.flip()

            clock.tick(45)

        self.__ships = ships
        self.__ship_images = ship_images

    def beschussPhase(self):
        clicked = []
        
        def get_coords(coords):  #//2 for smaller display
            x, y = coords[0], coords[1]
            x -= 1127//1
            y -= 120//1
            x = x // (60 // 1)
            y = y // (60 // 1)
            return x, y

        clock = pygame.time.Clock()
        run = True
        while run:
            draw_window()
            draw_text('beschussphase', font2, (40, 100, 40), 720, 20)

            # draw ships
            for i in range(len(self.__ships)):
                self.__surface.blit(self.__ship_images[i], self.__ships[i])
                pygame.draw.rect(self.__surface, "green", self.__ships[i], 1)  # optional

            self.__gsf.zeichneBrett()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()

                # Abschussdetektion
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = get_coords(event.pos)

                    # TO-DO: Multiplayer-Abwechslung

                    if x in range(10) and y in range(10):
                        if not ((x, y) in clicked):
                            if event.button == 1:
                                clicked.append((x, y))
                                self.__gsf.beschieße((x, y))

            x0, y0 = pygame.mouse.get_pos()
            x, y = get_coords((x0, y0))
            if x in range(10) and y in range(10):
                if not ((x, y) in clicked):
                    square = pygame.Rect(1127 // 1 + x * 60 + 1, 120 // 1 + y * 60 + 1, 58, 58)  # //2 bzw. 30 bzw. 28 bei kleinerem Bildschirm
                    pygame.draw.rect(self.__surface, (50, 50, 50), square)

            pygame.display.flip()

            clock.tick(45)

        pygame.quit()
        

# Ausgangsbildschirm
n = 1 # Skalar; Standard ist 1; sonst 2
screen = pygame.display.set_mode((1920/n, 1200/n))
pygame.display.set_caption("Schiffe Versenken")

# load resources
SPIELFELD_IMAGE = pygame.image.load('resources/spielfeld.jpg')
LETTERS_IMAGE = pygame.image.load('resources/letters.jpg')
NUMBERS_IMAGE = pygame.image.load('resources/numbers.jpg')
BACKGROUND_IMAGE = pygame.image.load('resources/background.jpg')
BACKGROUND2_IMAGE = pygame.image.load('resources/background2.jpg')

# background
BACKGROUND = pygame.transform.scale(BACKGROUND_IMAGE, (1920/n, 1200/n))
BACKGROUND2 = pygame.transform.scale(BACKGROUND2_IMAGE, (1920/n, 1200/n))

font1 = pygame.font.Font('resources/font.ttf', 90)
font2 = pygame.font.Font('resources/font.ttf', 55)


def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))


def draw_window():
    screen.blit(BACKGROUND2, (0, 0))

    SPIELFELD = pygame.transform.scale(SPIELFELD_IMAGE, (601 / n, 601 / n))
    LETTERS = pygame.transform.scale(LETTERS_IMAGE, (60 / n, 601 / n))
    NUMBERS = pygame.transform.scale(NUMBERS_IMAGE, (601 / n, 60 / n))

    screen.blit(SPIELFELD, (192 / n, 120 / n))
    screen.blit(LETTERS, (132 / n, 120 / n))
    screen.blit(NUMBERS, (192 / n, 721 / n))
    draw_text('heim', font1, (40, 140, 40), 370 / n, 20 / n)

    screen.blit(SPIELFELD, (1127 / n, 120 / n))
    screen.blit(LETTERS, (1067 / n, 120 / n))
    screen.blit(NUMBERS, (1127 / n, 721 / n))
    draw_text('feind', font1, (40, 140, 40), 1300 / n, 20 / n)


# Hauptspielphase
battle = Battleship(screen)
battle.aufbauPhase()
battle.beschussPhase()

