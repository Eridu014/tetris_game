#Tetris
#By Chad Fike


import random, time, pygame, sys
from pygame.locals import *

FPS = 25
WINDOWWIDTH = 640
WINDOWHEIGHT = 480
BOXSIZE = 20
BOARDWIDTH = 10
BOARDHEIGHT = 20
BLANK = '.'

MOVESIDEWAYSFREQ = 0.15
MOVEDOWNFREQ = 0.1

XMARGIN = int((WINDOWWIDTH - BOARDWIDTH * BOXSIZE) / 2)
TOPMARGIN = WINDOWHEIGHT - (BOARDWIDTH * BOXSIZE) -5

#fIX COLORS - LIGHT COLOR FOR EACH COLOR
WHITE = (255, 255, 255)
GRAY = (185, 185, 185)
COLOR1 = (16, 90, 184)
COLOR2 = (190, 150, 200)
COLOR3 = (200, 235, 80)
COLOR4 = (137, 137, 55)
COLOR5 = (213, 190, 95)
COLOR6 = (99, 188, 143)
COLOR7 = (124, 255, 239)
COLOR8 = (255, 212, 206)
COLOR9 = (255, 240, 233)
COLOR10 = (200, 200, 133)
COLOR11 = (241, 88, 177)

BORDERCOLOR = COLOR1
BGCOLOR = COLOR4
TEXTCOLOR = WHITE
TEXTSHADOWCOLOR = GRAY
COLORS = (COLOR2, COLOR3, COLOR4, COLOR5, COLOR6)
LIGHTCOLORS = (COLOR7, COLOR8, COLOR9, COLOR10, COLOR11)
assert len(COLORS) == len(LIGHTCOLORS)

TEMPLATEWIDTH = 5
TEMPLATEHEIGHT = 5

S_SHAPE_TEMPLATE = [['.....',
               '.....',
               '..00.',
               '.00..',
               '.....',],
               ['.....',
               '..0..',
               '..00.',
               '...0.',
               '.....',]]

I_SHAPE_TEMPLATE = [['.....',
               '.....',
               '..00.',
               '.00..',
               '.....',],
               ['.....',
               '..0..',
               '..00.',
               '...0.',
               '.....',]]

O_SHAPE_TEMPLATE = [['.....',
                '.....',
                '0000.',
                '.....',
                '.....',],
               ['..0..',
                '..0..',
                '..0..',
                '..0..',
                '.....',]]

J_SHAPE_TEMPLATE = [['.....',
               '.....',
               '..00.',
               '.00..',
               '.....',],
               ['.....',
               '..0..',
               '..00.',
               '...0.',
               '.....',]]

L_SHAPE_TEMPLATE = [['.....',
               '.....',
               '..0..',
               '..0..',
               '..00.',],
               ['.....',
               '..0..',
               '..00.',
               '...0.',
               '.....',]]

T_SHAPE_TEMPLATE = [['.....',
               '.....',
               '..00.',
               '..0..',
               '..0..',],
               ['.....',
               '..0..',
               '..00.',
               '...0.',
               '.....',]]
Z_SHAPE_TEMPLATE = [['.....',
               '.....',
               '..00.',
               '.00..',
               '.....',],
               ['.....',
               '..0..',
               '..00.',
               '...0.',
               '.....',]]

PIECES = { 'S' : S_SHAPE_TEMPLATE,
           'Z' : Z_SHAPE_TEMPLATE,
           'J' : J_SHAPE_TEMPLATE,
           'L' : L_SHAPE_TEMPLATE,
           'I' : I_SHAPE_TEMPLATE,
           'O' : O_SHAPE_TEMPLATE,
           'T' : T_SHAPE_TEMPLATE}

def main() :
    global FPSLOCK, DISPLAYSURF, BASICFONT, BIGFONT
    pygame.init()
    FPSLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    BASICFONT = pygame.font.Font('freesansbold.ttf', 18)
    BIGFONT = pygame.font.Font('freesansbold.ttf', 100)
    pygame.display.set_caption('Tetromino')

    showTextScreen('Textromino')
    while True: #Game Loop
        if random.randint(0, 1) == 0:
            pygame.mixer.music.load('tetrisb.mid')
        else :
            pygame.mixer.music.load('tetrisc.mid')
        pygame.mixer.music.play(-1, 0.0)
        runGame()
        pygame.mixer.music.stop()
        showTextScreen('Game Over')

def runGame() :
    #setup variables for game startup
    board = getBlankBoard()
    lastMoveDownTime = time.time()
    lastMoveSidewaysTime = time.time()
    lastFallTime = time.time()
    movingDown = False #Notice that there is no moving up variable
    movingLeft = False
    movingRight = False
    score = 0
    level, fallFreq = calculateLevelAndFallFrequency(score)
    fallingPiece = getNewPiece()
    nextPiece = getNewPiece()
    while True : #game loop
        if fallingPiece == None :
            fallingPiece = nextPiece
            nextPiece = getNewPiece()
            lastFallTime = time.time() #reset  lastFallTime
            if not isValidPosition(board, fallingPiece):
                return #no more pieces can fit on board = game over
        checkForQuit()
        for event in pygame.event.get() :
            if event.type == KEYUP :
                if (event.key == K_p) :
                    #pausing the game
                    DISPLAYSURF.fill(COLOR4)
                    pygame.mixer.music.stop()
                    showTextScreen('Paused') #Paused until key press
                    pygame.mixer.music.play(-1, 0.0)
                    lastFallTime = time.time()
                    lastMoveDownTime = time.time()
                    lastMoveSidewaysTime = time.time()
                elif (event.key == K_LEFT or event.key == K_a) :
                    movingLeft = False
                elif (event.key == K_RIGHT or event.key == K_d) :
                    movingRight = False
                elif (event.key == K_DOWN or event.key == K_s) :
                    movingDown = False
            elif event.type ==  KEYDOWN:
                    #moving the piece sideways
                if (event.key == K_LEFT or event.key == K_a) and isValidPosition(board, fallingPiece, adjX = -1) :
                        fallingPiece['x'] -= 1
                        movingLeft = True
                        movingRight = False
                        lastMoveSidewaysTime = time.time()
                elif (event.key == K_RIGHT or event.key == K_d) and isValidPosition(board, fallingPiece, adjX = 1) :
                        fallingPiece['x'] += 1
                        movingLeft = False
                        movingRight = True
                        lastMoveSidewaysTime = time.time()
                    #rotating the piece (if room to rotate)
                elif (event.key == K_UP or event.key == K_w):
                        fallingPiece['rotation'] = (fallingPiece['rotation'] + 1) % len(PIECES[fallingPiece['shape']])
                elif (event.key == K_q) : #rotate in the opposite direction
                    fallingPiece['rotation'] = (fallingPiece['rotation'] - 1) % len(PIECES[fallingPiece['shape']]) 
                    if not isValidPosition(board, fallingPiece) :
                            fallingPiece['rotation'] = (fallingPiece['rotation'] + 1) % len(PIECES[fallingPiece['shape']])
                    #Accelerating falling speed with down key
                elif (event.key == K_DOWN or event.key == K_s):
                        movingDown = True
                        if isValidPosition(board, fallingPiece, adjY = 1) :
                            fallingPiece['y'] += 1
                            lastMoveDownTime = time.time()
                elif event.key == K_SPACE: 
                        movingDown = False
                        movingRight = False
                        movingLeft = False
                        for i in range(1, BOARDHEIGHT):
                            if not isValidPosition(board, fallingPiece, adjY = i) :
                                break
                        fallingPiece['y'] += i - 1
                    #handle moving piece because of player input
            if (movingLeft or movingRight) and time.time() - lastMoveSidewaysTime > MOVESIDEWAYSFREQ :
                if movingLeft and isValidPosition(board, fallingPiece, adjX = -1) :
                        fallingPiece['x'] -= 1
                elif movingRight and isValidPosition(board, fallingPiece, adjX = 1) :
                    fallingPiece['x'] += 1
                    lastMoveSidewaysTime = time.time()
            if movingDown and time.time() - lastMoveSidewaysTime > MOVESIDEWAYSFREQ :
                    fallingPiece['y'] += 1
                    lastMoveDownTime =  time.time()
            if time.time() - lastFallTime > fallFreq :
                if not isValidPosition(board, fallingPiece, adjY = 1) :
                    addToBoard(board, fallingPiece)
                    score += removeCompleteLines(board)
                    level, fallFreq = calculateLevelAndFallFrequency(score)
                    fallingPiece = None
                else : 
                    #piece did not land 
                    fallingPiece['y'] += 1
                    lastFallTime = time.time()
            #drawing everything on board
            DISPLAYSURF.fill(BGCOLOR)
            drawBoard(board)
            drawStatus(score, level)
            drawNextPiece(nextPiece)
            if fallingPiece != None :
                drawPiece(fallingPiece)
            pygame.display.update()
            FPSLOCK.tick(FPS)
def convertToPixelCoordinates(boxx, boxy) : #convert xy coordinates of baord to xy coordinates of location on screen
    return (XMARGIN + (boxx * BOXSIZE)), (TOPMARGIN + (boxy * BOXSIZE))

def getBlankBoard() : 
    board = []
    for i in range(BOARDWIDTH) :
        board.append([BLANK] * BOARDHEIGHT)
    return board

def makeTextObjects(text, font, color) :
    surf = font.render(text, True, color)
    return surf, surf.get_rect()

def exit() :
    pygame.quit()
    sys.exit()

def checkForQuit() :
    for event in pygame.event.get(QUIT) :
        quit()
    for event in pygame.event.get(KEYUP) :
        if event.key == K_ESCAPE:
            exit()
        pygame.event.post(event)

def showTextScreen(text) :
    #creates game home screen awaiting player input
    titleSurf, titleRect = makeTextObjects(text, BIGFONT, TEXTSHADOWCOLOR)
    titleRect.center = (int(WINDOWWIDTH / 2), int(WINDOWHEIGHT / 2.5))
    DISPLAYSURF.blit(titleSurf, titleRect)

    #draw text
    titleSurf, titleRect = makeTextObjects(text, BIGFONT, TEXTCOLOR)
    titleRect.center = (int(WINDOWWIDTH /2 ), int(WINDOWHEIGHT / 2.5) - 3)
    DISPLAYSURF.blit(titleSurf, titleRect)
def calculateLevelAndFallFrequency(score) :
    #total player score and return what level player is on
    #how many secs until piece falls one space
    level = int(score / 10) + 1
    fallFrequency = 0.25 - (level * 0.25)
    return level, fallFrequency

def getNewPiece() :
    #return a random new piece in a random color and rotation
    shape = random.choice(list(PIECES.keys()))
    newPiece = {'shape' : shape, 'rotation' : random.randint(0, len(PIECES[shape]) -1), 'x' : int(BOARDWIDTH / 2) - int(TEMPLATEWIDTH / 2), 'y' : -2, 'color' : random.randint(0, len(COLORS) -1) }
    return newPiece

def drawBox(boxx, boxy, color, pixelx = None, pixely = None) :
    #draw a single box
    #at x,y coordinates on board. Or for pixel x, y (used for "next" piece)
    if color == BLANK :
        return 
    if pixelx == None and pixely == None: 
        pixelx, pixely = convertToPixelCoordinates(boxx, boxy)
    pygame.draw.rect(DISPLAYSURF, COLORS[color], (pixelx + 1, pixely + 1, BOXSIZE - 1, BOXSIZE - 1))
    pygame.draw.rect(DISPLAYSURF, LIGHTCOLORS[color], (pixelx +1, pixely + 1, BOXSIZE - 4, BOXSIZE - 4))

def isOnBoard(x, y) :
    return x >= 0 and x < BOARDWIDTH and y < BOARDWIDTH

def drawBoard(board) :
    #draw border around board
    pygame.draw.rect(DISPLAYSURF, BORDERCOLOR, (XMARGIN, TOPMARGIN, BOXSIZE * BOARDHEIGHT))
    #draw individual boxes on board
    for x in range(BOARDWIDTH) :
        for y in range(BOARDHEIGHT) :
            drawBox(x, y, board[x][y])

def addToBoard(board, fallingPiece) :

def drawStatus(score, level) :

def removeCompleteLines(board) :

def isValidPosition(board, piece, adjX = 0, adjY = 0) :
    #Return true if the piece is not out of bounds & not colliding with another
    for x in range(TEMPLATEWIDTH) :
        for y in range(TEMPLATEHEIGHT):
            isAboveBoard = y + piece['y'] + adjY < 0
            if isAboveBoard or PIECES[piece['shape']] [piece['rotation']][y][x] == BLANK:
                continue
            if not isOnBoard(x + piece['x'] + adjX, y + piece['y'] + adjY):
                return False
            if board[x + piece['x'] + adjX] [y + piece['y'] + adjY] != BLANK :
                return False
    return True

def drawPiece(piece, pixelx = None, pixely = None) :
    shapeToDraw = PIECES[piece['shape']][piece['rotation']]
    if pixelx == None and pixely == None :
        #if pixelx and pixely hasnt yet been specified, use default location in the "piece" data structure
        for x in range(TEMPLATEWIDTH) :
            for y in range(TEMPLATEHEIGHT) :
                if shapeToDraw[y][x] != BLANK :
                    drawBox(None, None, piece['color'], pixelx + (x * BOXSIZE), pixely + (y * BOXSIZE))

def drawNextPiece(piece) :
    #draw the "next" text
    nextSurf = BASICFONT.render('Next:', True, TEXTCOLOR)
    nextRect = nextSurf.get_rect()
    nextRect.topleft = (WINDOWWIDTH - 120, 80)
    DISPLAYSURF.blit(nextSurf, nextRect)
    #draw the "next" piece
    drawPiece(piece, pixelx = WINDOWWIDTH - 120, pixely = 100)


if __name__ == '__main__' :
    main()




