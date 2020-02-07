import pygame
import time
import random
from pygame.locals import *
import sys
import os
import pygame.mixer

display_width = 1080
display_height = 1080

#colors
black =(0,0,0)
white = (255,255,255)
blue =(0,0,50)
bright_yellow=(255,255,0)

green =(0,200,0)
yellow_orange=(255,174,66)
orange=(255,165,0)
red =(200,0,0)
yellow =(200,200,0)
violet =(127,0,255)
yellow_green=(154,205,50)

#-------------------------
title_width=800
SizeCardW = 70
SizeCardH = 120
GapSize = 10 

DONUT = 'donut'
SQUARE = 'square'
DIAMOND = 'diamond'
LINES = 'lines'
OVAL = 'oval'
BoxColor = green
REVEALSPEED = 8

AllColors = (green,yellow,yellow_green,yellow_orange,orange,red,violet,white)
AllShapes = (DONUT, SQUARE, DIAMOND, LINES, OVAL)
DISPLAYSURF = pygame.display.set_mode((display_width, display_height))
HIGHLIGHTCOLOR = yellow_green

pygame.init()
gameDisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('Shuffle')
clock = pygame.time.Clock()

title = pygame.image.load('shuffle.png')
smallText = pygame.font.Font("freesansbold.ttf",20)
largetext = pygame.font.Font("freesansbold.ttf",40)
XMARGIN = int((display_width - (4 * (SizeCardW + GapSize))) / 2)
YMARGIN = int((display_height - (4 * (SizeCardH + GapSize))) / 2)

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def text_objects(text,font,color):
    textSurface = font.render(text,True, color)
    return textSurface, textSurface.get_rect()   

def button(msg,x,y,w,h,ic,ac,action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    up = pygame.MOUSEBUTTONUP
    #print(mouse)
    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        pygame.draw.rect(gameDisplay, ac, (x,y,w,h))
        pygame.draw.rect(gameDisplay, blue, (x+3,y+3,w-6,h-6))
        if click[0] == 1 and action != None:
            action()
    else:  
        pygame.draw.rect(gameDisplay, ic, (x,y,w,h))
        pygame.draw.rect(gameDisplay, blue, (x+3,y+3,w-6,h-6))    

    
    TextSurf, TextRect = text_objects(msg, smallText,yellow)
    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        TextSurf, TextRect = text_objects(msg, smallText,white)
    TextRect.center = ( (x+(w/2)),(y+ (h/2)))
    gameDisplay.blit(TextSurf,TextRect)

def game_intro():

    intro = True
    pygame.mixer.music.stop()
    pygame.mixer.music.set_volume(0.05)
    pygame.mixer.music.load('foo.mp3')
    pygame.mixer.music.play(-1)
    
    while intro:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == pygame.quit:
                pygame,quit
                quit()
        gameDisplay.fill(blue)
        gameDisplay.blit(title,((display_width/2)-(title_width/2),50))

        largeText = pygame.font.Font('freesansbold.ttf',115)
    
        button("4x3",540-75,350,150,40,yellow,white,game4x3)
        button("4x4",540-75,400,150,40,yellow,white,game4x4)
        button("5x4",540-75,450,150,40,yellow,white,game5x4)
        button("6x5",540-75,500,150,40,yellow,white,game6x5)
        button("6x6",540-75,550,150,40,yellow,white,game6x6)
        button("Exit",540-75,625,150,40,yellow,white,"quit")

        mouse = pygame.mouse.get_pos()
    
        pygame.display.update()
        clock.tick(30)

def getRandomizedBoard(boardw,boardh):
    icons = []
    for color in AllColors:
        for shape in AllShapes:
            icons.append( (shape, color) )

    random.shuffle(icons) 
    numIconsUsed = int(boardw * boardh / 2) 
    icons = icons[:numIconsUsed] * 2 
    random.shuffle(icons)

    board = []
    for x in range(boardw):
        column = []
        for y in range(boardh):
            column.append(icons[0])
            del icons[0]
        board.append(column)
    return board

def leftTopCoordsOfBox(boxx, boxy):

    left = boxx * (SizeCardW + GapSize) + XMARGIN
    top = boxy * (SizeCardH + GapSize) + YMARGIN
    return (left, top)

def drawBoard(board,boardw,boardh,revealed):

    for boxx in range(boardw):
        for boxy in range(boardh):
            left, top = leftTopCoordsOfBox(boxx, boxy)
           
            if not revealed[boxx][boxy]:

                pygame.draw.rect(DISPLAYSURF, BoxColor, (left, top, SizeCardW, SizeCardH))
            else:

                shape, color = getShapeAndColor(board, boxx, boxy)
                drawIcon(shape, color, boxx, boxy)

def getShapeAndColor(board, boxx, boxy):

    return board[boxx][boxy][0], board[boxx][boxy][1]


def generateRevealedBoxesData(val,boardw,boardh):
    revealedBoxes = []
    for i in range(boardw):
        revealedBoxes.append([val] * boardh)
    return revealedBoxes

def getBoxAtPixel(x, y,boardw,boardh):
    for boxx in range(boardw):
        for boxy in range(boardh):
            left, top = leftTopCoordsOfBox(boxx, boxy)
            boxRect = pygame.Rect(left, top, SizeCardW, SizeCardH)
            if boxRect.collidepoint(x, y):
                return (boxx, boxy)
    return (None, None)

def drawHighlightBox(boxx, boxy):
    left, top = leftTopCoordsOfBox(boxx, boxy)
    pygame.draw.rect(DISPLAYSURF, white, (left, top, SizeCardW, SizeCardH))

def drawIcon(shape, color, boxx, boxy):
    quarter = int(SizeCardW * 0.25)
    half =    int(SizeCardH * 0.5) 

    left, top = leftTopCoordsOfBox(boxx, boxy)

    if shape == DONUT:
        pygame.draw.ellipse(DISPLAYSURF, color, (left, top + quarter, SizeCardW, half))
        pygame.draw.ellipse(DISPLAYSURF, color, (left, top + half, SizeCardW, half))
    elif shape == SQUARE:
        pygame.draw.rect(DISPLAYSURF, color, (left + quarter, top + quarter, SizeCardW - half, SizeCardH - half))
    elif shape == DIAMOND:
        pygame.draw.polygon(DISPLAYSURF, color, ((left + half, top), (left + SizeCardW - 1, top + half), (left + half, top + SizeCardH - 1), (left, top + half)))
    elif shape == LINES:
        for i in range(0, SizeCardW, 4):
            pygame.draw.line(DISPLAYSURF, color, (left, top + i), (left + i, top))
            pygame.draw.line(DISPLAYSURF, color, (left + i, top + SizeCardH - 1), (left + SizeCardW - 1, top + i))
    elif shape == OVAL:
        pygame.draw.ellipse(DISPLAYSURF, color, (left, top + quarter, SizeCardW, half))

def hasWon(revealedBoxes):
 
    for i in revealedBoxes:
        if False in i:
            return False 
    return 1

def game4x3():

    FPSCLOCK = pygame.time.Clock()
    mousex = 0
    mousey = 0
    boardw = 4
    boardh = 3
    Score = 0
    Misses = 0
    wait = False
    helperxx = 0
    helperyy = 0
    
    
    mainboard = getRandomizedBoard(boardw,boardh)
    revealedBoxes = generateRevealedBoxesData(False,boardw,boardh)
    firstSelection = None
    while True:
        mouseClicked = False
        button("Exit",50,900,150,40,yellow,white,game_intro)
        if not hasWon(revealedBoxes):
            DISPLAYSURF.fill(blue)
            button("Exit",50,900,150,40,yellow,white,game_intro)
            drawBoard(mainboard,boardw,boardh,revealedBoxes)
            if firstSelection != None:
                left, top = leftTopCoordsOfBox(helperxx, helperyy)
                icon1shape, icon1color = getShapeAndColor(mainboard, firstSelection[0], firstSelection[1])
                pygame.draw.rect(DISPLAYSURF, icon1color, (left, top, SizeCardW, SizeCardH), 4)
                

        TextSurf, TextRect = text_objects("Score: %d" %Score, smallText,yellow)
        TextRect.center =  (80),(60)
        gameDisplay.blit(TextSurf,TextRect)
        while wait == False:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONUP:
                    wait = True
        
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEMOTION:
                mousex, mousey = event.pos
            elif event.type == MOUSEBUTTONUP:
                mousex, mousey = event.pos
                mouseClicked = True
        boxx, boxy = getBoxAtPixel(mousex, mousey,boardw,boardh)
        if not hasWon(revealedBoxes):
            if boxx != None and boxy != None:
                if not revealedBoxes[boxx][boxy]:
                    drawHighlightBox(boxx, boxy)
                if not revealedBoxes[boxx][boxy] and mouseClicked:
                    revealedBoxes[boxx][boxy] = True
                    DISPLAYSURF.fill(blue)
                    button("Exit",50,900,150,40,yellow,white,game_intro)
                    drawBoard(mainboard,boardw,boardh,revealedBoxes)
                    if firstSelection != None:
                        left, top = leftTopCoordsOfBox(helperxx, helperyy)
                        icon1shape, icon1color = getShapeAndColor(mainboard, firstSelection[0], firstSelection[1])
                        pygame.draw.rect(DISPLAYSURF, icon1color, (left, top, SizeCardW, SizeCardH), 4)
                    TextSurf, TextRect = text_objects("Score: %d" %Score, smallText,yellow)
                    TextRect.center =  (80),(60)
                    
                    gameDisplay.blit(TextSurf,TextRect)
                    pygame.display.update()
                    FPSCLOCK.tick(30)
                    
                    if firstSelection == None:
                        firstSelection = (boxx,boxy)
                        helperxx =boxx
                        helperyy =boxy 
                        left, top = leftTopCoordsOfBox(boxx, boxy)
                        icon1shape, icon1color = getShapeAndColor(mainboard, firstSelection[0], firstSelection[1])
                        pygame.draw.rect(DISPLAYSURF, icon1color, (left, top, SizeCardW, SizeCardH), 4)
                    else:
                        icon1shape, icon1color = getShapeAndColor(mainboard, firstSelection[0], firstSelection[1])
                        icon2shape, icon2color = getShapeAndColor(mainboard, boxx, boxy)
                        left, top = leftTopCoordsOfBox(boxx, boxy)
                        pygame.draw.rect(DISPLAYSURF, icon2color, (left, top, SizeCardW, SizeCardH), 4)
                        pygame.display.update()

                        if icon1shape != icon2shape or icon1color != icon2color:

                            pygame.time.wait(1000)
                            revealedBoxes[firstSelection[0]][firstSelection[1]] = False
                            revealedBoxes[boxx][boxy] = False
                            if Misses >= 0:
                                Score = Score - 20*2**Misses
                                if Score < 0:
                                    Score = 0
                            Misses = Misses + 1

                        elif hasWon(revealedBoxes):
                            pygame.mixer.music.set_volume(0.05)
                            pygame.mixer.music.load('applaud.mp3')
                            pygame.mixer.music.play(0)
                            DISPLAYSURF.fill(blue)
                            button("Exit",50,900,150,40,yellow,white,game_intro)
                            TextSurf, TextRect = text_objects("Congratulations!", largetext,yellow)
                            TextRect.center =  (530),(530)
                            gameDisplay.blit(TextSurf,TextRect)
                            pygame.display.update()

                        elif icon1shape == icon2shape and icon1color == icon2color:
                            Misses = 0
                            Score = Score + 100
                            
                            
                        firstSelection = None


                

                
        

        pygame.display.update()
        FPSCLOCK.tick(30)

def game4x4():
    FPSCLOCK = pygame.time.Clock()
    mousex = 0
    mousey = 0
    boardw = 4
    boardh = 4
    Score = 0
    Misses = 0
    wait = False
    helperxx = 0
    helperyy = 0
    
    mainboard = getRandomizedBoard(boardw,boardh)
    revealedBoxes = generateRevealedBoxesData(False,boardw,boardh)
    firstSelection = None
    while True:
        mouseClicked = False
        button("Exit",50,900,150,40,yellow,white,game_intro)
        if not hasWon(revealedBoxes):
            DISPLAYSURF.fill(blue)
            button("Exit",50,900,150,40,yellow,white,game_intro)
            drawBoard(mainboard,boardw,boardh,revealedBoxes)
            if firstSelection != None:
                left, top = leftTopCoordsOfBox(helperxx, helperyy)
                icon1shape, icon1color = getShapeAndColor(mainboard, firstSelection[0], firstSelection[1])
                pygame.draw.rect(DISPLAYSURF, icon1color, (left, top, SizeCardW, SizeCardH), 4)
                

        TextSurf, TextRect = text_objects("Score: %d" %Score, smallText,yellow)
        TextRect.center =  (80),(60)
        gameDisplay.blit(TextSurf,TextRect)
        while wait == False:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONUP:
                    wait = True
        
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEMOTION:
                mousex, mousey = event.pos
            elif event.type == MOUSEBUTTONUP:
                mousex, mousey = event.pos
                mouseClicked = True
        boxx, boxy = getBoxAtPixel(mousex, mousey,boardw,boardh)
        if not hasWon(revealedBoxes):
            if boxx != None and boxy != None:
                if not revealedBoxes[boxx][boxy]:
                    drawHighlightBox(boxx, boxy)
                if not revealedBoxes[boxx][boxy] and mouseClicked:
                    revealedBoxes[boxx][boxy] = True
                    DISPLAYSURF.fill(blue)
                    button("Exit",50,900,150,40,yellow,white,game_intro)
                    drawBoard(mainboard,boardw,boardh,revealedBoxes)
                    if firstSelection != None:
                        left, top = leftTopCoordsOfBox(helperxx, helperyy)
                        icon1shape, icon1color = getShapeAndColor(mainboard, firstSelection[0], firstSelection[1])
                        pygame.draw.rect(DISPLAYSURF, icon1color, (left, top, SizeCardW, SizeCardH), 4)
                    TextSurf, TextRect = text_objects("Score: %d" %Score, smallText,yellow)
                    TextRect.center =  (80),(60)
                    
                    gameDisplay.blit(TextSurf,TextRect)
                    pygame.display.update()
                    FPSCLOCK.tick(30)
                    
                    if firstSelection == None:
                        firstSelection = (boxx,boxy)
                        helperxx =boxx
                        helperyy =boxy 
                        left, top = leftTopCoordsOfBox(boxx, boxy)
                        icon1shape, icon1color = getShapeAndColor(mainboard, firstSelection[0], firstSelection[1])
                        pygame.draw.rect(DISPLAYSURF, icon1color, (left, top, SizeCardW, SizeCardH), 4)
                    else:
                        icon1shape, icon1color = getShapeAndColor(mainboard, firstSelection[0], firstSelection[1])
                        icon2shape, icon2color = getShapeAndColor(mainboard, boxx, boxy)
                        left, top = leftTopCoordsOfBox(boxx, boxy)
                        pygame.draw.rect(DISPLAYSURF, icon2color, (left, top, SizeCardW, SizeCardH), 4)
                        pygame.display.update()

                        if icon1shape != icon2shape or icon1color != icon2color:

                            pygame.time.wait(1000)
                            revealedBoxes[firstSelection[0]][firstSelection[1]] = False
                            revealedBoxes[boxx][boxy] = False
                            if Misses >= 0:
                                Score = Score - 20*2**Misses
                                if Score < 0:
                                    Score = 0
                            Misses = Misses + 1

                        elif hasWon(revealedBoxes):
                            pygame.mixer.music.set_volume(0.05)
                            pygame.mixer.music.load('applaud.mp3')
                            pygame.mixer.music.play(0)
                            DISPLAYSURF.fill(blue)
                            button("Exit",50,900,150,40,yellow,white,game_intro)
                            TextSurf, TextRect = text_objects("Congratulations!", largetext,yellow)
                            TextRect.center =  (530),(530)
                            gameDisplay.blit(TextSurf,TextRect)
                            pygame.display.update()

                        elif icon1shape == icon2shape and icon1color == icon2color:
                            Misses = 0
                            Score = Score + 100
                            
                            
                        firstSelection = None


                

                
        

        pygame.display.update()
        FPSCLOCK.tick(30)

def game5x4():
    FPSCLOCK = pygame.time.Clock()
    mousex = 0
    mousey = 0
    boardw = 5
    boardh = 4
    Score = 0
    Misses = 0
    wait = False
    helperxx = 0
    helperyy = 0
    
    mainboard = getRandomizedBoard(boardw,boardh)
    revealedBoxes = generateRevealedBoxesData(False,boardw,boardh)
    firstSelection = None
    while True:
        mouseClicked = False
        button("Exit",50,900,150,40,yellow,white,game_intro)
        if not hasWon(revealedBoxes):
            DISPLAYSURF.fill(blue)
            button("Exit",50,900,150,40,yellow,white,game_intro)
            drawBoard(mainboard,boardw,boardh,revealedBoxes)
            if firstSelection != None:
                left, top = leftTopCoordsOfBox(helperxx, helperyy)
                icon1shape, icon1color = getShapeAndColor(mainboard, firstSelection[0], firstSelection[1])
                pygame.draw.rect(DISPLAYSURF, icon1color, (left, top, SizeCardW, SizeCardH), 4)
                

        TextSurf, TextRect = text_objects("Score: %d" %Score, smallText,yellow)
        TextRect.center =  (80),(60)
        gameDisplay.blit(TextSurf,TextRect)
        while wait == False:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONUP:
                    wait = True
        
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEMOTION:
                mousex, mousey = event.pos
            elif event.type == MOUSEBUTTONUP:
                mousex, mousey = event.pos
                mouseClicked = True
        boxx, boxy = getBoxAtPixel(mousex, mousey,boardw,boardh)
        if not hasWon(revealedBoxes):
            if boxx != None and boxy != None:
                if not revealedBoxes[boxx][boxy]:
                    drawHighlightBox(boxx, boxy)
                if not revealedBoxes[boxx][boxy] and mouseClicked:
                    revealedBoxes[boxx][boxy] = True
                    DISPLAYSURF.fill(blue)
                    button("Exit",50,900,150,40,yellow,white,game_intro)
                    drawBoard(mainboard,boardw,boardh,revealedBoxes)
                    if firstSelection != None:
                        left, top = leftTopCoordsOfBox(helperxx, helperyy)
                        icon1shape, icon1color = getShapeAndColor(mainboard, firstSelection[0], firstSelection[1])
                        pygame.draw.rect(DISPLAYSURF, icon1color, (left, top, SizeCardW, SizeCardH), 4)
                    TextSurf, TextRect = text_objects("Score: %d" %Score, smallText,yellow)
                    TextRect.center =  (80),(60)
                    
                    gameDisplay.blit(TextSurf,TextRect)
                    pygame.display.update()
                    FPSCLOCK.tick(30)
                    
                    if firstSelection == None:
                        firstSelection = (boxx,boxy)
                        helperxx =boxx
                        helperyy =boxy 
                        left, top = leftTopCoordsOfBox(boxx, boxy)
                        icon1shape, icon1color = getShapeAndColor(mainboard, firstSelection[0], firstSelection[1])
                        pygame.draw.rect(DISPLAYSURF, icon1color, (left, top, SizeCardW, SizeCardH), 4)
                    else:
                        icon1shape, icon1color = getShapeAndColor(mainboard, firstSelection[0], firstSelection[1])
                        icon2shape, icon2color = getShapeAndColor(mainboard, boxx, boxy)
                        left, top = leftTopCoordsOfBox(boxx, boxy)
                        pygame.draw.rect(DISPLAYSURF, icon2color, (left, top, SizeCardW, SizeCardH), 4)
                        pygame.display.update()

                        if icon1shape != icon2shape or icon1color != icon2color:

                            pygame.time.wait(1000)
                            revealedBoxes[firstSelection[0]][firstSelection[1]] = False
                            revealedBoxes[boxx][boxy] = False
                            if Misses >= 0:
                                Score = Score - 20*2**Misses
                                if Score < 0:
                                    Score = 0
                            Misses = Misses + 1

                        elif hasWon(revealedBoxes):
                            pygame.mixer.music.set_volume(0.05)
                            pygame.mixer.music.load('applaud.mp3')
                            pygame.mixer.music.play(0)
                            DISPLAYSURF.fill(blue)
                            button("Exit",50,900,150,40,yellow,white,game_intro)
                            TextSurf, TextRect = text_objects("Congratulations!", largetext,yellow)
                            TextRect.center =  (530),(530)
                            gameDisplay.blit(TextSurf,TextRect)
                            pygame.display.update()

                        elif icon1shape == icon2shape and icon1color == icon2color:
                            Misses = 0
                            Score = Score + 100
                            
                            
                        firstSelection = None


                

                
        

        pygame.display.update()
        FPSCLOCK.tick(30)

def game6x5():
    FPSCLOCK = pygame.time.Clock()
    mousex = 0
    mousey = 0
    boardw = 6
    boardh = 5
    Score = 0
    Misses = 0
    wait = False
    helperxx = 0
    helperyy = 0
    
    mainboard = getRandomizedBoard(boardw,boardh)
    revealedBoxes = generateRevealedBoxesData(False,boardw,boardh)
    firstSelection = None
    while True:
        mouseClicked = False
        button("Exit",50,900,150,40,yellow,white,game_intro)
        if not hasWon(revealedBoxes):
            DISPLAYSURF.fill(blue)
            button("Exit",50,900,150,40,yellow,white,game_intro)
            drawBoard(mainboard,boardw,boardh,revealedBoxes)
            if firstSelection != None:
                left, top = leftTopCoordsOfBox(helperxx, helperyy)
                icon1shape, icon1color = getShapeAndColor(mainboard, firstSelection[0], firstSelection[1])
                pygame.draw.rect(DISPLAYSURF, icon1color, (left, top, SizeCardW, SizeCardH), 4)
                

        TextSurf, TextRect = text_objects("Score: %d" %Score, smallText,yellow)
        TextRect.center =  (80),(60)
        gameDisplay.blit(TextSurf,TextRect)
        while wait == False:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONUP:
                    wait = True
        
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEMOTION:
                mousex, mousey = event.pos
            elif event.type == MOUSEBUTTONUP:
                mousex, mousey = event.pos
                mouseClicked = True
        boxx, boxy = getBoxAtPixel(mousex, mousey,boardw,boardh)
        if not hasWon(revealedBoxes):
            if boxx != None and boxy != None:
                if not revealedBoxes[boxx][boxy]:
                    drawHighlightBox(boxx, boxy)
                if not revealedBoxes[boxx][boxy] and mouseClicked:
                    revealedBoxes[boxx][boxy] = True
                    DISPLAYSURF.fill(blue)
                    button("Exit",50,900,150,40,yellow,white,game_intro)
                    drawBoard(mainboard,boardw,boardh,revealedBoxes)
                    if firstSelection != None:
                        left, top = leftTopCoordsOfBox(helperxx, helperyy)
                        icon1shape, icon1color = getShapeAndColor(mainboard, firstSelection[0], firstSelection[1])
                        pygame.draw.rect(DISPLAYSURF, icon1color, (left, top, SizeCardW, SizeCardH), 4)
                    TextSurf, TextRect = text_objects("Score: %d" %Score, smallText,yellow)
                    TextRect.center =  (80),(60)
                    
                    gameDisplay.blit(TextSurf,TextRect)
                    pygame.display.update()
                    FPSCLOCK.tick(30)
                    
                    if firstSelection == None:
                        firstSelection = (boxx,boxy)
                        helperxx =boxx
                        helperyy =boxy 
                        left, top = leftTopCoordsOfBox(boxx, boxy)
                        icon1shape, icon1color = getShapeAndColor(mainboard, firstSelection[0], firstSelection[1])
                        pygame.draw.rect(DISPLAYSURF, icon1color, (left, top, SizeCardW, SizeCardH), 4)
                    else:
                        icon1shape, icon1color = getShapeAndColor(mainboard, firstSelection[0], firstSelection[1])
                        icon2shape, icon2color = getShapeAndColor(mainboard, boxx, boxy)
                        left, top = leftTopCoordsOfBox(boxx, boxy)
                        pygame.draw.rect(DISPLAYSURF, icon2color, (left, top, SizeCardW, SizeCardH), 4)
                        pygame.display.update()

                        if icon1shape != icon2shape or icon1color != icon2color:

                            pygame.time.wait(1000)
                            revealedBoxes[firstSelection[0]][firstSelection[1]] = False
                            revealedBoxes[boxx][boxy] = False
                            if Misses >= 0:
                                Score = Score - 20*2**Misses
                                if Score < 0:
                                    Score = 0
                            Misses = Misses + 1

                        elif hasWon(revealedBoxes):
                            pygame.mixer.music.set_volume(0.05)
                            pygame.mixer.music.load('applaud.mp3')
                            pygame.mixer.music.play(0)
                            DISPLAYSURF.fill(blue)
                            button("Exit",50,900,150,40,yellow,white,game_intro)
                            TextSurf, TextRect = text_objects("Congratulations!", largetext,yellow)
                            TextRect.center =  (530),(530)
                            gameDisplay.blit(TextSurf,TextRect)
                            pygame.display.update()

                        elif icon1shape == icon2shape and icon1color == icon2color:
                            Misses = 0
                            Score = Score + 100
                            
                            
                        firstSelection = None


                

                
        

        pygame.display.update()
        FPSCLOCK.tick(30)

def game6x6():
    FPSCLOCK = pygame.time.Clock()
    mousex = 0
    mousey = 0
    boardw = 6
    boardh = 6
    Score = 0
    Misses = 0
    wait = False
    helperxx = 0
    helperyy = 0
    
    mainboard = getRandomizedBoard(boardw,boardh)
    revealedBoxes = generateRevealedBoxesData(False,boardw,boardh)
    firstSelection = None
    while True:
        mouseClicked = False
        button("Exit",50,900,150,40,yellow,white,game_intro)
        if not hasWon(revealedBoxes):
            DISPLAYSURF.fill(blue)
            button("Exit",50,900,150,40,yellow,white,game_intro)
            drawBoard(mainboard,boardw,boardh,revealedBoxes)
            if firstSelection != None:
                left, top = leftTopCoordsOfBox(helperxx, helperyy)
                icon1shape, icon1color = getShapeAndColor(mainboard, firstSelection[0], firstSelection[1])
                pygame.draw.rect(DISPLAYSURF, icon1color, (left, top, SizeCardW, SizeCardH), 4)
                

        TextSurf, TextRect = text_objects("Score: %d" %Score, smallText,yellow)
        TextRect.center =  (80),(60)
        gameDisplay.blit(TextSurf,TextRect)
        while wait == False:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONUP:
                    wait = True
        
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEMOTION:
                mousex, mousey = event.pos
            elif event.type == MOUSEBUTTONUP:
                mousex, mousey = event.pos
                mouseClicked = True
        boxx, boxy = getBoxAtPixel(mousex, mousey,boardw,boardh)
        if not hasWon(revealedBoxes):
            if boxx != None and boxy != None:
                if not revealedBoxes[boxx][boxy]:
                    drawHighlightBox(boxx, boxy)
                if not revealedBoxes[boxx][boxy] and mouseClicked:
                    revealedBoxes[boxx][boxy] = True
                    DISPLAYSURF.fill(blue)
                    button("Exit",50,900,150,40,yellow,white,game_intro)
                    drawBoard(mainboard,boardw,boardh,revealedBoxes)
                    if firstSelection != None:
                        left, top = leftTopCoordsOfBox(helperxx, helperyy)
                        icon1shape, icon1color = getShapeAndColor(mainboard, firstSelection[0], firstSelection[1])
                        pygame.draw.rect(DISPLAYSURF, icon1color, (left, top, SizeCardW, SizeCardH), 4)
                    TextSurf, TextRect = text_objects("Score: %d" %Score, smallText,yellow)
                    TextRect.center =  (80),(60)
                    
                    gameDisplay.blit(TextSurf,TextRect)
                    pygame.display.update()
                    FPSCLOCK.tick(30)
                    
                    if firstSelection == None:
                        firstSelection = (boxx,boxy)
                        helperxx =boxx
                        helperyy =boxy 
                        left, top = leftTopCoordsOfBox(boxx, boxy)
                        icon1shape, icon1color = getShapeAndColor(mainboard, firstSelection[0], firstSelection[1])
                        pygame.draw.rect(DISPLAYSURF, icon1color, (left, top, SizeCardW, SizeCardH), 4)
                    else:
                        icon1shape, icon1color = getShapeAndColor(mainboard, firstSelection[0], firstSelection[1])
                        icon2shape, icon2color = getShapeAndColor(mainboard, boxx, boxy)
                        left, top = leftTopCoordsOfBox(boxx, boxy)
                        pygame.draw.rect(DISPLAYSURF, icon2color, (left, top, SizeCardW, SizeCardH), 4)
                        pygame.display.update()

                        if icon1shape != icon2shape or icon1color != icon2color:

                            pygame.time.wait(1000)
                            revealedBoxes[firstSelection[0]][firstSelection[1]] = False
                            revealedBoxes[boxx][boxy] = False
                            if Misses >= 0:
                                Score = Score - 20*2**Misses
                                if Score < 0:
                                    Score = 0
                            Misses = Misses + 1

                        elif hasWon(revealedBoxes):
                            pygame.mixer.music.set_volume(0.05)
                            pygame.mixer.music.load('applaud.mp3')
                            pygame.mixer.music.play(0)
                            DISPLAYSURF.fill(blue)
                            button("Exit",50,900,150,40,yellow,white,game_intro)
                            TextSurf, TextRect = text_objects("Congratulations!", largetext,yellow)
                            TextRect.center =  (530),(530)
                            gameDisplay.blit(TextSurf,TextRect)
                            pygame.display.update()

                        elif icon1shape == icon2shape and icon1color == icon2color:
                            Misses = 0
                            Score = Score + 100
                            
                            
                        firstSelection = None


                

                
        

        pygame.display.update()
        FPSCLOCK.tick(30)

game_intro()
pygame.quit()
quit()