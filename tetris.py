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

#               R    G    B
WHITE       = (255, 255, 255)
GRAY        = (185, 185, 185)
BLACK       = (  0,   0,   0)
RED         = (155,   0,   0)
LIGHTRED    = (175,  20,  20)
GREEN       = (  0, 155,   0)
LIGHTGREEN  = ( 20, 175,  20)
BLUE        = (  0,   0, 155)
LIGHTBLUE   = ( 20,  20, 175)
YELLOW      = (155, 155,   0)
LIGHTYELLOW = (175, 175,  20)

BORDERCOLOR = WHITE
BGCOLOR = BLACK
TEXTCOLOR = WHITE
TEXTSHADOWCOLOR = GRAY
COLORS      = (     BLUE,      GREEN,      RED,      YELLOW)
LIGHTCOLORS = (LIGHTBLUE, LIGHTGREEN, LIGHTRED, LIGHTYELLOW)
assert len(COLORS) == len(LIGHTCOLORS)

TEMPLATEWIDTH = 5
TEMPLATEHEIGHT = 5

F_TEMPLATE = [['.....',
               '..OO.',
               '.OO..',
               '..O..',
               '.....'],
              ['.....',
               '..O..',
               '.OOO.',
               '...O.',
               '.....'],
              ['.....',
               '..O..',
               '..OO.',
               '.OO..',
               '.....'],
              ['.....',
               '.O...',
               '.OOO.',
               '..O..',
               '.....']]
RF_TEMPLATE = [['.....',
                '.OO..',
                '..OO.',
                '..O..',
                '.....'],
               ['.....',
                '...O.',
                '.OOO.',
                '..O..',
                '.....'],
               ['.....',
                '..O..',
                '.OO..',
                '..OO.',
                '.....'],
               ['.....',
                '..O..',
                '.OOO.',
                '.O...',
                '.....']]
I_TEMPLATE = [['..O..',
               '..O..',
               '..O..',
               '..O..',
               '..O..'],
              ['.....',
               '.....',
               'OOOOO',
               '.....',
               '.....']]
L_TEMPLATE = [['..O..',
               '..O..',
               '..O..',
               '..OO.',
               '.....'],
              ['.....',
               '.....',
               '.OOOO',
               '.O...',
               '.....'],
              ['.....',
               '.OO..',
               '..O..',
               '..O..',
               '..O..'],
              ['.....',
               '...O.',
               'OOOO.',
               '.....',
               '.....']]
J_TEMPLATE = [['..O..',
               '..O..',
               '..O..',
               '.OO..',
               '.....'],
              ['.....',
               '.O...',
               '.OOOO',
               '.....',
               '.....'],
              ['.....',
               '..OO.',
               '..O..',
               '..O..',
               '..O..'],
              ['.....',
               '.....',
               'OOOO.',
               '...O.',
               '.....']]
N_TEMPLATE = [['.....',
               '.OO..',
               '..OOO',
               '.....',
               '.....'],
              ['.....',
               '...O.',
               '..OO.',
               '..O..',
               '..O..'],
              ['.....',
               '.....',
               'OOO..',
               '..OO.',
               '.....'],
              ['..O..',
               '..O..',
               '.OO..',
               '.O...',
               '.....']]
RN_TEMPLATE = [['.....',
                '..OO.',
                'OOO..',
                '.....',
                '.....'],
               ['..O..',
                '..O..',
                '..OO.',
                '...O.',
                '.....'],
               ['.....',
                '.....',
                '..OOO',
                '.OO..',
                '.....'],
               ['.....',
                '.O...',
                '.OO..',
                '..O..',
                '..O..']]
P_TEMPLATE = [['.....',
               '..OO.',
               '..OO.',
               '..O..',
               '.....'],
              ['.....',
               '.....',
               '.OOO.',
               '..OO.',
               '.....'],
              ['.....',
               '..O..',
               '.OO..',
               '.OO..',
               '.....'],
              ['.....',
               '.OO..',
               '.OOO.',
               '.....',
               '.....']]
RP_TEMPLATE = [['.....',
                '.OO..',
                '.OO..',
                '..O..',
                '.....'],
               ['.....',
                '..OO.',
                '.OOO.',
                '.....',
                '.....'],
               ['.....',
                '..O..',
                '..OO.',
                '..OO.',
                '.....'],
               ['.....',
                '.....',
                '.OOO.',
                '.OO..',
                '.....']]
T_TEMPLATE = [['.....',
               '.OOO.',
               '..O..',
               '..O..',
               '.....'],
              ['.....',
               '...O.',
               '.OOO.',
               '...O.',
               '.....'],
              ['.....',
               '..O..',
               '..O..',
               '.OOO.',
               '.....'],
              ['.....',
               '.O...',
               '.OOO.',
               '.O...',
               '.....']]
U_TEMPLATE = [['.....',
               '.O.O.',
               '.OOO.',
               '.....',
               '.....'],
              ['.....',
               '..OO.',
               '..O..',
               '..OO.',
               '.....'],
              ['.....',
               '.....',
               '.OOO.',
               '.O.O.',
               '.....'],
              ['.....',
               '.OO..',
               '..O..',
               '.OO..',
               '.....']]
V_TEMPLATE = [['..O..',
               '..O..',
               '..OOO',
               '.....',
               '.....'],
              ['.....',
               '.....',
               '..OOO',
               '..O..',
               '..O..'],
              ['.....',
               '.....',
               'OOO..',
               '..O..',
               '..O..'],
              ['..O..',
               '..O..',
               'OOO..',
               '.....',
               '.....']]
W_TEMPLATE = [['.....',
               '.O...',
               '.OO..',
               '..OO.',
               '.....'],
              ['.....',
               '..OO.',
               '.OO..',
               '.O...',
               '.....'],
              ['.....',
               '.OO..',
               '..OO.',
               '...O.',
               '.....'],
              ['.....',
               '...O.',
               '..OO.',
               '.OO..',
               '.....']]
X_TEMPLATE = [['.....',
               '..O..',
               '.OOO.',
               '..O..',
               '.....']]
Y_TEMPLATE = [['.....',
               '..O..',
               'OOOO.',
               '.....',
               '.....'],
              ['..O..',
               '..O..',
               '..OO.',
               '..O..',
               '.....'],
              ['.....',
               '.....',
               '.OOOO',
               '..O..',
               '.....'],
              ['.....',
               '..O..',
               '.OO..',
               '..O..',
               '..O..']]
RY_TEMPLATE = [['.....',
                '.....',
                'OOOO.',
                '..O..',
                '.....'],
               ['..O..',
                '..O..',
                '..OO.',
                '..O..',
                '.....'],
               ['.....',
                '.....',
                '.OOOO',
                '..O..',
                '.....'],
               ['.....',
                '..O..',
                '.OO..',
                '..O..',
                '..O..']]
Z_TEMPLATE = [['.....',
               '.OO..',
               '..O..',
               '..OO.',
               '.....'],
              ['.....',
               '...O.',
               '.OOO.',
               '.O...',
               '.....']]
RZ_TEMPLATE = [['.....',
                '..OO.',
                '..O..',
                '.OO..',
                '.....'],
               ['.....',
                '.O...',
                '.OOO.',
                '...O.',
                '.....']]



SHAPES = {'F': F_TEMPLATE,
          'RF': RF_TEMPLATE,
          'I': I_TEMPLATE,
          'L': L_TEMPLATE,
          'J': J_TEMPLATE,
          'N': N_TEMPLATE,
          'RN': RN_TEMPLATE,
          'P': P_TEMPLATE,
          'RP': RP_TEMPLATE,
          'T': T_TEMPLATE,
          'U': U_TEMPLATE,
          'V': V_TEMPLATE,
          'W': W_TEMPLATE,
          'X': X_TEMPLATE,
          'Y': Y_TEMPLATE,
          'RY': RY_TEMPLATE,
          'Z': Z_TEMPLATE,
          'RZ': RZ_TEMPLATE}


def main() :
    global FPSCLOCK, DISPLAYSURF, BASICFONT, BIGFONT
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    BASICFONT = pygame.font.Font('freesansbold.ttf', 18)
    BIGFONT = pygame.font.Font('freesansbold.ttf', 100)
    pygame.display.set_caption('Tetromino')

    showTextScreen('I LOVE U')
    while True: #Game Loop
        #if random.randint(0, 1) == 0:
            #pygame.mixer.music.load('tetrisb.mid')
        #else :
            #pygame.mixer.music.load('tetrisc.mid')
        #pygame.mixer.music.play(-1, 0.0)
        runGame()
        #pygame.mixer.music.stop()
        showTextScreen('You Lost')

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
            #start new piece at top
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
                    DISPLAYSURF.fill(BLUE)
                    #pygame.mixer.music.stop()
                    showTextScreen('Paused') #Paused until key press
                    #pygame.mixer.music.play(-1, 0.0)
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
                    fallingPiece['rotation'] = (fallingPiece['rotation'] + 1) % len(SHAPES[fallingPiece['shape']])
                    if not isValidPosition(board, fallingPiece):
                        fallingPiece['rotation'] = (fallingPiece['rotation'] - 1) % len(SHAPES[fallingPiece['shape']])
                elif (event.key == K_q) : #rotate in the opposite direction
                    fallingPiece['rotation'] = (fallingPiece['rotation'] - 1) % len(SHAPES[fallingPiece['shape']]) 
                    if not isValidPosition(board, fallingPiece) :
                            fallingPiece['rotation'] = (fallingPiece['rotation'] + 1) % len(SHAPES[fallingPiece['shape']])

                    #Accelerating falling speed with down key
                elif (event.key == K_DOWN or event.key == K_s):
                        movingDown = True
                        if isValidPosition(board, fallingPiece, adjY = 1) :
                            fallingPiece['y'] += 1
                            lastMoveDownTime = time.time()
                #move falling piece all the way down           
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
            #has piece landed?
            if not isValidPosition(board, fallingPiece, adjY = 1) :
                #set falling piece on the board
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
        drawTetrisBoard(board)
        drawStatus(score, level)
        drawNextPiece(nextPiece)
        if fallingPiece != None :
            drawPiece(fallingPiece)

        pygame.display.update()
        FPSCLOCK.tick(FPS)

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

def checkForKeyPress() :
    #go through event queue and search for KEYUP event
    #grab KEYDOWN events to remove from queue
    checkForQuit()

    for event in pygame.event.get([KEYDOWN, KEYUP]) :
        if event.type == KEYDOWN :
            continue
        return event.key
    return None

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

def showTextScreen(text):
    # This function displays large text in the
    # center of the screen until a key is pressed.
    # Draw the text drop shadow
    titleSurf, titleRect = makeTextObjects(text, BIGFONT, TEXTSHADOWCOLOR)
    titleRect.center = (int(WINDOWWIDTH / 2), int(WINDOWHEIGHT / 2))
    DISPLAYSURF.blit(titleSurf, titleRect)

    # Draw the text
    titleSurf, titleRect = makeTextObjects(text, BIGFONT, TEXTCOLOR)
    titleRect.center = (int(WINDOWWIDTH / 2) - 3, int(WINDOWHEIGHT / 2) - 3)
    DISPLAYSURF.blit(titleSurf, titleRect)

    # Draw the additional "Press a key to play." text.
    pressKeySurf, pressKeyRect = makeTextObjects('Press a key to play.', BASICFONT, TEXTCOLOR)
    pressKeyRect.center = (int(WINDOWWIDTH / 2), int(WINDOWHEIGHT / 2) + 100)
    DISPLAYSURF.blit(pressKeySurf, pressKeyRect)

    while checkForKeyPress() == None:
        pygame.display.update()
        FPSCLOCK.tick()


def calculateLevelAndFallFrequency(score) :
    #total player score and return what level player is on
    #how many secs until piece falls one space
    level = int(score / 10) + 1
    fallFrequency = 0.25 - (level * 0.02)
    return level, fallFrequency

def getNewPiece() :
    #return a random new piece in a random color and rotation
    shape = random.choice(list(SHAPES.keys()))
    newPiece = {'shape' : shape, 'rotation' : random.randint(0, len(SHAPES[shape]) -1), 'x' : int(BOARDWIDTH / 2) - int(TEMPLATEWIDTH / 2), 'y' : -2, 'color' : random.randint(0, len(COLORS) -1) }
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

def drawBoard(board):
    # draw the border around the board
    pygame.draw.rect(DISPLAYSURF, BORDERCOLOR, (XMARGIN - 3, TOPMARGIN - 7, (BOARDWIDTH * BOXSIZE) + 8, (BOARDHEIGHT * BOXSIZE) + 8), 5)

    # fill the background of the board
    pygame.draw.rect(DISPLAYSURF, BGCOLOR, (XMARGIN, TOPMARGIN, BOXSIZE * BOARDWIDTH, BOXSIZE * BOARDHEIGHT))
    # draw the individual boxes on the board
    for x in range(BOARDWIDTH):
        for y in range(BOARDHEIGHT):
            drawBox(x, y, board[x][y])

def isOnBoard(x, y) :
    return x >= 0 and x < BOARDWIDTH and y < BOARDWIDTH

def drawTetrisBoard(board) :
    #draw border around board
    pygame.draw.rect(DISPLAYSURF, BORDERCOLOR, (XMARGIN - 3, TOPMARGIN - 7, (BOARDWIDTH * BOXSIZE) + 8, (BOARDHEIGHT * BOXSIZE) + 8), 5)

    #fill background
    pygame.draw.rect(DISPLAYSURF, BORDERCOLOR, (XMARGIN, TOPMARGIN, BOXSIZE + BOARDWIDTH, BOXSIZE * BOARDHEIGHT))

    #draw individual boxes on board
    for x in range(BOARDWIDTH) :
        for y in range(BOARDHEIGHT) :
            drawBox(x, y, board[x][y])

def addToBoard(board, piece) :
    for x in range(TEMPLATEWIDTH):
        for y in range(TEMPLATEHEIGHT):
            if SHAPES[piece['shape']][piece['rotation']][y][x] != BLANK:
                board[x + piece['x']][y + piece['y']] = piece['color']

def drawStatus(score, level) :
    scoreSurf = BASICFONT.render('Score: %s' % score, True, TEXTCOLOR)
    scoreRect = scoreSurf.get_rect()
    scoreRect.topleft = (WINDOWWIDTH - 150, 20)
    DISPLAYSURF.blit(scoreSurf, scoreRect)
    #draw level text
    levelSurf = BASICFONT.render('Level: %s' % level, True, TEXTCOLOR)
    levelRect = levelSurf.get_rect()
    levelRect.topleft = (WINDOWWIDTH - 150, 50)
    DISPLAYSURF.blit(levelSurf, levelRect)

def removeCompleteLines(board) :
    #remove completed lines of blocks on board
    numOfLinesRemoved = 0
    y = BOARDHEIGHT - 1
    while y >= 0:
        if isCompleteLine(board, y) :
            for pullDownY in range(y, 0, -1) :
                for x in range(BOARDWIDTH) :
                    board[x][pullDownY] = board[x][pullDownY - 1]
            for x in range(BOARDWIDTH) :
                board[x][0] = BLANK
            numOfLinesRemoved += 1
            #y is same value on next iteration
        else :
            y -= 1
        return numOfLinesRemoved

def isCompleteLine(board, y) :
    #return true if line is filled by blocks with no gaps
    for x in range(BOARDWIDTH) :
        if board[x][y] == BLANK :
            return False
    return True


def isValidPosition(board, piece, adjX=0, adjY=0):

     # Return True if the piece is within the board and not colliding

     for x in range(TEMPLATEWIDTH):
        for y in range(TEMPLATEHEIGHT):
            isAboveBoard = y + piece['y'] + adjY < 0
            if isAboveBoard or SHAPES[piece['shape']][piece['rotation']][y][x] == BLANK:
                continue
            if not isOnBoard(x + piece['x'] + adjX, y + piece['y'] + adjY):
                return False
            if board[x + piece['x'] + adjX][y + piece['y'] + adjY] != BLANK:
                return False
        return True

def drawPiece(piece, pixelx = None, pixely = None) :
    #draw the shape of the block pieces
    shapeToDraw = SHAPES[piece['shape']][piece['rotation']]
    if pixelx == None and pixely == None :
        #if pixelx and pixely hasnt yet been specified, use default location in the "piece" data structure
        pixelx, pixely = convertToPixelCoordinates(piece['x'], piece['y'])
    # draw each of the blocks that make up the piece
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




