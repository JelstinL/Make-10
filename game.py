from cmu_graphics import *
from random import randint
import os
import copy
import random
from cmu_cpcs_utils import rounded


def loadBestScore():
    try:
        with open('bestscore.txt', 'r') as f:
            return int(f.read().strip())
    except:
        return 0
    
def saveBestScore(score):
    with open('bestscore.txt', 'w') as f:
        f.write(str(score))
        


class Apple:
    def __init__(self, cx, cy, r, value):
        self.cx = cx
        self.cy = cy
        self.r = r
        self.value = value
        self.selected = False

class BombingApple(Apple):
    def __init__(self, cx, cy, r, value):
        super().__init__(cx, cy, r, value)
        self.exploded = False
        
        
class FreezeApple(Apple):
    def __init__(self, cx, cy, r, value):
        super().__init__(cx,cy,r,value)
        self.frozen = False


def onAppStart(app):
    
    app.bestScore = loadBestScore()
    
    app.screen = 'start'
    
    app.stepsPerSecond = 1
    
    # apple
    app.apples = [ ]
    app.rows = 9
    app.cols = 18
    app.appleRadius = 21
    
    app.spacing = 2.5 * app.appleRadius
    app.marginTop = 2.5 * app.spacing
    app.marginBottom = 1.5 * app.spacing
    app.marginSide = 1.2 * app.marginTop

    # timer
    app.timerCx = app.width/2 - 150
    app.timerCy = app.spacing
    app.timerR = 18
    app.timerCount = 112
    app.timerCountCx = app.timerCx + 60
    app.timerBarLeft = app.timerCountCx + 40
    app.timerBarTop = app.timerCy - 12
    app.timerBarWidth = 250
    app.timerBarHeight = 25
    
    # scoreBoard
    app.scoreLeft = (3/4) * app.width
    app.scoreTop = 25
    app.scoreWidth = 165
    app.scoreHeight = 55
    app.scoreCx = app.scoreLeft + 60
    app.scoreCy = app.scoreTop + 25
    app.score = 0 
    
    #selection
    app.selecting = False
    app.selectX = 0
    app.selectY = 0
    app.mouseX = 0
    app.mouseY = 0
    
    #powerup menu
    app.powerupMode = False
    app.freezeTimer = 0
    
    for row in range(app.rows):
        for col in range(app.cols):
            cx = app.marginSide + col * app.spacing
            cy = app.marginTop + row * app.spacing
            apple = Apple(cx,cy, app.appleRadius,randint(1,9))
            app.apples.append(apple)



def redrawAll(app):
    if app.screen == 'start':
        drawStartScreen(app)
    elif app.screen == 'game':
        drawGameScreen(app)
    elif app.screen == 'gameover':
        drawGameOverScreen(app)
    
def drawStartScreen(app):
    drawRect(0,0, app.width, app.height, fill=rgb(207,230,206))
    for apple in app.apples:
        drawCircle(apple.cx, apple.cy, apple.r, fill = rgb(255, 61, 10),
               opacity = 40)
        drawOval(apple.cx + 3, apple.cy - 20, 10, 20, 
             fill='green',rotateAngle=45, opacity=40)
        drawLabel(apple.value, apple.cx, apple.cy, 
              fill='white', bold=True, size=20, opacity=40)
    
    # main card
    cardW = 380
    cardH = 420
    cardX = app.width/2 - cardW/2
    cardY = app.height/2 - cardH/2
    
    #card shadow
    drawRect(cardX + 6, cardY + 6, cardW, cardH,
             fill = 'black', opacity = 15)
    
    #card background
    drawRect(cardX, cardY, cardW, cardH, fill='white')
    
    drawRect(cardX, cardY, cardW, 90, fill=rgb(255,182,182))
    drawLabel('Make 10', app.width/2, cardY + 45,
              size=48, bold = True, fill=rgb(220,80,80))
            
    #best score section
    drawLabel('BEST', app.width/2 - 60, cardY + 130,
              size = 16, fill = 'gray')
    drawLabel(f'{app.bestScore}', app.width/2 - 60, cardY + 165,
              size = 48, bold = True, fill = rgb(60,60,60))
              
    # leaderboard icon
    podiumCx = app.width/2 + 60
    podiumCy = cardY + 155
    drawRect(podiumCx - 30, podiumCy - 10, 22, 30,
             fill=rgb(180,180,180))
    drawRect(podiumCx - 4, podiumCy -25, 22, 45,
             fill=rgb(140,140,140))
    drawRect(podiumCx + 22, podiumCy -5, 22, 25,
             fill=rgb(180,180,180))
    drawLabel('1', podiumCx+7,podiumCy-32, size=11, fill='white',bold=True)
    drawLabel('2', podiumCx-19,podiumCy-17, size=11, fill='white',bold=True)
    drawLabel('3', podiumCx+33,podiumCy-12, size=11, fill='white',bold=True)
    
    drawLine(cardX + 20, cardY + 210, cardX + cardW - 20, cardY + 210,
             fill = rgb(220, 220, 220), lineWidth =1)
             
    drawLabel('All numbers are random.', app.width/2, cardY + 260,
              size = 18, fill=rgb(100,100,100))
    
    # play button
    btnW = 260
    btnH = 58
    btnX = app.width/2 - btnW/2
    btnY = cardY + 310
    drawRect(btnX, btnY, btnW, btnH,
             fill=rgb(230,230,255), border=rgb(150,150,200), borderWidth=2)
    drawLabel('PLAY', app.width/2, btnY + 29,
              size=32, bold=True, fill=rgb(80,80,80))
            
    
    

def drawGameScreen(app):
        # background color
        drawRect(0, 0, app.width, app.height, fill = rgb(207, 230, 206))
        
        for apple in app.apples:
            drawApple(apple, app)
        
        drawTimer(app)
        drawTimerCount(app)
        drawTimerBar(app)
        
        drawScoreBoard(app)
        
        drawSelection(app)
        drawPowerupButton(app)
    
def drawGameOverScreen(app):
    drawRect(0,0,app.width, app.height, fill=rgb(207,230,206))
    drawLabel('Game Over', app.width/2, app.height/3, 
              size = 60, bold=True)
    drawLabel(f'Score: {app.score}', app.width/2, 
              app.height/2 - 40, size = 35)
    # main menu
    drawRect(app.width/4 + 180, app.height/2 + 20, 240, 60, fill='gray')
    drawLabel('Main Menu', app.width/2, app.height/2 + 50, 
              size = 30, fill = 'white')

    

def drawApple(apple, app):
    border = None
    borderWidth = 2
    
    if apple.selected:
        border = 'black'
    elif app.powerupMode and isinstance(apple,BombingApple):
        border = 'yellow'
        borderWidth = 4
    elif app.powerupMode and isinstance(apple, FreezeApple):
        border = rgb(120,220,255)
        borderWidth = 4
    
    drawCircle(apple.cx, apple.cy, apple.r, fill = rgb(255, 61, 10),
               border = border, borderWidth = borderWidth)
    drawOval(apple.cx + 3, apple.cy - 20, 10, 20, 
             fill='green',rotateAngle=45)
    drawLabel(apple.value, apple.cx, apple.cy, 
              fill='white', bold=True, size=20)

            
def drawTimer(app):
    drawCircle(app.timerCx, app.timerCy, app.timerR, fill = 'gray')
    drawLine(app.timerCx, app.timerCy, 
             app.timerCx, app.timerCy - app.timerR + 4,
             fill=rgb(207, 230, 206), lineWidth = 4)
    drawLine(app.timerCx - 2, app.timerCy,
             app.timerCx + app.timerR - 8, app.timerCy,
             fill =rgb(207, 230, 206), lineWidth = 4)
    
def drawTimerCount(app):
    drawLabel(f'{app.timerCount}', app.timerCountCx, app.timerCy, size = 40)


def drawScoreBoard(app):
    drawRect(app.scoreLeft, app.scoreTop, app.scoreWidth, 
             app.scoreHeight, fill = 'lightgray')
    drawLabel('Score', app.scoreCx, app.scoreCy, size = 25)
    drawLabel(f'{app.score}', app.scoreCx + 70, app.scoreCy, 
              size = 40, bold = True)
              
def onStep(app):
    if app.screen == 'game':
        if app.freezeTimer > 0:
            app.freezeTimer -= 1
        elif app.timerCount > 0:
            app.timerCount -= 1
        else:
            app.screen = 'gameover'
        
def drawTimerBar(app):
    drawRect(app.timerBarLeft, app.timerBarTop, 
             app.timerBarWidth, app.timerBarHeight, 
             fill = 'gray', border = 'white')
    
    barWidth = app.timerBarWidth * (app.timerCount / 112)
    
    if barWidth > 0:
        if app.freezeTimer > 0:
            fillColor = rgb(120,220,255)
        else:
            fillColor = 'yellow'
        
        drawRect(app.timerBarLeft, app.timerBarTop, 
                 barWidth, app.timerBarHeight, 
                 fill =fillColor)
    
def onKeyPress(app, key):
    if key == 'p':
        app.timerCount = 0
        app.screen = 'gameover'


   
def onMousePress(app, mouseX, mouseY):
    cardW = 380
    cardH = 420
    cardY = app.height/2 - cardH/2
    btnW = 260
    btnH = 58
    btnX = app.width/2 - btnW/2
    btnY = cardY + 310
    
    
    
    if app.screen == 'start':
         #check if they clicked the start button
        if (btnX <= mouseX <= btnX + btnW and btnY <= mouseY <= btnY + btnH):
            app.screen = 'game'
     
    elif app.screen == 'game':
        if (20 <= mouseX <= 170 and 15 <= mouseY <= 65):
            if app.powerupMode:
                deactivatePowerupMode(app)
            else:
                activatePowerupMode(app)
        else:
            app.selecting = True
            app.selectX = mouseX
            app.selectY = mouseY
            app.mouseX = mouseX
            app.mouseY = mouseY
    elif app.screen == 'gameover':
        #main menu button
        if (app.width/4 + 180 <= mouseX <= app.width/4 + 420 and
            app.height/2 + 20 <= mouseY <= app.height/2 + 80):
            resetGame(app)
            app.screen = 'start'

        
        
    
def onMouseDrag(app, mouseX, mouseY):
    if app.screen == 'game':
        app.mouseX = mouseX
        app.mouseY = mouseY
        
        for apple in app.apples:
            apple.selected = isAppleInRect(apple, app)


def onMouseRelease(app, mouseX, mouseY):
    if app.screen == 'game':
        selectedApples = [apple for apple in app.apples if apple.selected]
        if sum(apple.value for apple in selectedApples) == 10:
            toDelete = set()
            
            for apple in selectedApples:
                toDelete.add(id(apple))
                
                if isinstance(apple, BombingApple):
                    for neighbor in getBombNeighbors(apple, app.apples, app.spacing):
                        toDelete.add(id(neighbor))
                if isinstance(apple, FreezeApple):
                    app.freezeTimer = 5
            app.score += len(toDelete)
            app.apples = [apple for apple in app.apples if id(apple) not in toDelete]
        else:
            for apple in app.apples:
                apple.selected = False
        app.selecting = False
    
    if app.score > app.bestScore:
        app.bestScore = app.score
        saveBestScore(app.bestScore)
        

def isAppleInRect(apple, app):
    x = min(app.selectX, app.mouseX)
    y = min(app.selectY, app.mouseY)
    width = abs(app.mouseX - app.selectX)
    height = abs(app.mouseY - app.selectY)
    return (x <= apple.cx <= x + width and
            y <= apple.cy <= y + height)


def drawSelection(app):
    if app.selecting:
        x = min(app.selectX, app.mouseX)
        y = min(app.selectY, app.mouseY)
        width = abs(app.mouseX - app.selectX)
        height = abs(app.mouseY - app.selectY)
        if width > 0 and height > 0:
            drawRect(x, y, width, height,
                     fill = 'gray', borderWidth = 2, opacity = 50)


def resetGame(app):
    app.apples = [ ]
    app.timerCount = 112
    app.score = 0
    app.selecting = False
    app.powerupMode = False
    for row in range(app.rows):
        for col in range(app.cols):
            cx = app.marginSide + col * app.spacing
            cy = app.marginTop + row * app.spacing
            apple = Apple(cx, cy, app.appleRadius, randint(1,9))
            app.apples.append(apple)
    
        

def getBombNeighbors(bombApple, allApples, spacing):
    neighbors = []
    directions = [
        (1,0), (-1,0), (0,1), (0,-1),
        (1,1), (1,-1), (-1,1),(-1,-1)
        ]
    for apple in allApples:
        colDiff = rounded((apple.cx - bombApple.cx) / spacing)
        rowDiff = rounded((apple.cy - bombApple.cy) / spacing)
        if (rowDiff, colDiff) in directions:
            neighbors.append(apple)
    return neighbors


def drawPowerupButton(app):
    fillColor = rgb(230, 190, 60) if app.powerupMode else rgb(100,100,200)
    text = 'Power Mode: ON' if app.powerupMode else 'Power Mode'
    
    drawRect(20, 15, 170, 50, fill=fillColor)
    drawLabel(f'{text}', 105, 40, size=20, bold=True, fill='white')


def activatePowerupMode(app):
    app.powerupMode = True
    
    normalAppleIndices = []
    for i in range(len(app.apples)):
        if isinstance(app.apples[i], Apple) and not isinstance(app.apples[i], BombingApple):
            normalAppleIndices.append(i)
        
    bombCount = min(10, len(normalAppleIndices))
    bombIndices = random.sample(normalAppleIndices, bombCount)
    
    for i in bombIndices:
        apple = app.apples[i]
        app.apples[i] = BombingApple(apple.cx, apple.cy, apple.r, apple.value)
    
    normalAppleIndices = []
    for i in range(len(app.apples)):
        if type(app.apples[i]) == Apple:
            normalAppleIndices.append(i)
    freezeCount = min(10, len(normalAppleIndices))
    freezeIndices = random.sample(normalAppleIndices, freezeCount)
    
    for i in freezeIndices:
        apple = app.apples[i]
        app.apples[i] = FreezeApple(apple.cx, apple.cy, apple.r, apple.value)
        
        
def deactivatePowerupMode(app):
    app.powerupMode = False
    
    for i in range(len(app.apples)):
        apple = app.apples[i]
        if isinstance(apple, BombingApple) or isinstance(apple, FreezeApple):
            app.apples[i] = Apple(apple.cx, apple.cy, apple.r, apple.value)

    
def main():
    runApp(width=1210, height=630)

    
main()
