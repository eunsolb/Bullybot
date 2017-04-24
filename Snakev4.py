# snake-demo.py

# Note: there is a snake tutorial from previous semesters here:
#    http://www.kosbie.net/cmu/fall-11/15-112/handouts/snake/snake.html
# But this is different in two key ways:
#    1) This uses this semester's framework (run function, and in Python3)
#    2) This uses a list of tuples to represent the snake
# You should understand both solutions, and be able to adapt that
# tutorial to use this semester's framework.

from tkinter import *
import random
import time
from tkinter import messagebox
import csv
import datetime

def init(data):
    print("initialize")
    data.rows = 20
    data.cols = 20
    data.margin = 20 # margin around grid
    data.snake = [(data.rows/2, data.cols/2)]
    data.direction = (0, +1) # (drow, dcol)
    placeFood(data)
    #data.timerDelay = 250
    data.gameOver = False
    data.time = 0.0

    data.score = 0
    data.timer = 300
    data.keycountup=0
    data.keycountdown = 0
    data.keycountleft = 0
    data.keycountright = 0
    data.keytimer = 0
    data.keytimerfired = False
    data.keystrokes = 0
    data.start = time.time()
    data.keydowntime = 0.0
    data.keyuptime = 0.0
    data.logging = True

    data.date = datetime.datetime.now()
    data.path = '%s-%s-%s_%s-%s-%s-%s.csv' % (data.date.year, data.date.month, data.date.day,
                                              data.date.hour, data.date.minute, data.date.second, data.date.microsecond)
    f = open(data.path, "w+")
    f.close()
    csv_writer(['Key', 'Unregistered Keys', 'Key Down Time', 'Key Up Time', 'Up/Down Time Difference', 'Time Duration',
               'Start Time', 'End Time', 'Game Over'], data.path)

    data.mode = "splashScreen"

    data.pressedKeys = {}
    data.timeDelay = 2 # initial time period delay
    data.timeStart = time.time()
    data.timePeriod = data.timeStart + data.timeDelay
    data.maxDelayTime = 2 #[sec]
    data.annoy = False




# getCellBounds from grid-demo.py
def getCellBounds(row, col, data):
    # aka "modelToView"
    # returns (x0, y0, x1, y1) corners/bounding box of given cell in grid
    gridWidth  = data.width - 2*data.margin
    gridHeight = data.height - 2*data.margin
    x0 = data.margin + gridWidth * col / data.cols
    x1 = data.margin + gridWidth * (col+1) / data.cols
    y0 = data.margin + gridHeight * row / data.rows
    y1 = data.margin + gridHeight * (row+1) / data.rows
    return (x0, y0, x1, y1)

def mousePressed(event, data):
    if data.gameOver == True:
        data.gameOver = False


def keyPressed(event, data):
    if (data.mode == "splashScreen") : splashScreenKeyPressed(event,data)
    elif (data.mode == "playGame") : playGameKeyPressed(event,data)

def timerFired(data):
    if data.mode == "splashScreen" : splashScreenTimerFired(data)
    elif data.mode == "playGame" :
        playGametimerFired(data)

def redrawAll(canvas,data):
    if(data.mode == "splashScreen") : splashScreenRedrawAll(canvas,data)
    elif (data.mode == "playGame"): playGameRedrawAll(canvas,data)

### splash Screen###

def splashScreenKeyPressed(event,data):
    if (event.keysym == "s"):
        data.pressedKeys[event.keysym] = time.time()
        data.mode = "playGame"

def splashScreenTimerFired(data):
    pass

def splashScreenRedrawAll (canvas,data):

    canvas.create_text(data.width/2, data.height/2, text = "To start the game, press S", font="Arial 26 bold")


###Play mode###

def playGameKeyPressed(event,data):
    data.mode = "playGame"

    # if (event.keysym == "s"):
    data.pressedKeys[event.keysym] = time.time()

    if (data.gameOver):
        data.timeDelay = 0
        data.timePeriod = time.time()
        if (event.keysym=="s"):
            data.mode = "gameReset"
        return

    if (data.pressedKeys[event.keysym] < data.timePeriod) and data.annoy:
        return

    if (event.keysym == "Up") :
        data.direction=(-1,0)
        data.keytimerfired = False
        data.keytimer = 0
        data.keycountup = 0


    elif (event.keysym == "Down"):
        # data.keycountdown += 1
        # keycountsetdown = {2,3,5,6,8,9,11,14,15}
        # if data.keycountdown in keycountsetdown: pass
        data.direction = (+1, 0)
    elif (event.keysym == "Left"):

        data.direction = (0, -1)
    elif (event.keysym == "Right"):
        data.direction = (0, +1)
    # for debugging, take one step on any keypress
    takeStep(data)

def playGameKeyReleased(event,data):
    keyuptime = time.time()
    keydowntime = data.pressedKeys[event.keysym]
    timedifference = keyuptime - keydowntime

    kd = '%.4f ' % (keydowntime)
    ku = '%.4f ' % (keyuptime)
    ud = '%.4f' % (timedifference)
    td = '%.4f' % (data.timeDelay)
    st = '%.4f ' % (data.timeStart)
    et = '%.4f ' % (data.timePeriod)

    values = [event.keysym, str(data.annoy), kd, ku, ud, td, st, et, str(data.gameOver)]
    csv_writer(values, data.path)

def playGametimerFired(data):
    if (data.gameOver): return
    takeStep(data)
    data.timer -=1
    if data.timer <= 0 : data.gameOver = True
    if data.keytimerfired == True: data.keytimer += 1



def takeStep(data):
    if (data.timePeriod < time.time()):
        data.timeDelay = random.random() * data.maxDelayTime
        data.timeStart = time.time()
        data.timePeriod = data.timeStart + data.timeDelay
        data.annoy = bool(random.randint(0, 1))

    (drow, dcol) = data.direction
    (headRow, headCol) = data.snake[0]
    (newRow, newCol) = (headRow+drow, headCol+dcol)
    if ((newRow < 0) or (newRow >= data.rows) or
        (newCol < 0) or (newCol >= data.cols) or
        ((newRow, newCol) in data.snake)):
        data.gameOver = True
    else:
        data.snake.insert(0, (newRow, newCol))
        if (data.foodPosition == (newRow, newCol)):
            placeFood(data)
            data.score += 1
        else:
            # didn't eat, so remove old tail (slither forward)
            data.snake.pop()

def placeFood(data):
    data.foodPosition = None
    row0 = random.randint(0, data.rows-1)
    col0 = random.randint(0, data.cols-1)
    for drow in range(data.rows):
        for dcol in range(data.cols):
            row = (row0 + drow) % data.rows
            col = (col0 + dcol) % data.cols
            if (row,col) not in data.snake:
                data.foodPosition = (row, col)
                return


def drawBoard(canvas, data):
    for row in range(data.rows):
        for col in range(data.cols):
            (x0, y0, x1, y1) = getCellBounds(row, col, data)
            canvas.create_rectangle(x0, y0, x1, y1, fill="white")

def drawSnake(canvas, data):
    for (row, col) in data.snake:
        (x0, y0, x1, y1) = getCellBounds(row, col, data)
        canvas.create_oval(x0, y0, x1, y1, fill="green")

def drawFood(canvas, data):
    if (data.foodPosition != None):
        (row, col) = data.foodPosition
        (x0, y0, x1, y1) = getCellBounds(row, col, data)
        canvas.create_oval(x0, y0, x1, y1, fill="red")

def drawGameOver(canvas, data):
    if (data.gameOver):
        canvas.create_text(data.width/2, data.height/2-data.margin, text="Game over!",
                           font="Arial 26 bold")
        canvas.create_text(data.width / 2, data.height / 2+data.margin, text="To restart the game, press S",
                           font="Arial 26 bold")

def gameRestartredrawAll(canvas,data):
    data.mode = "playGame"
    data.gameOver = False
    print("In game restart all")
    init(data)
    playGameRedrawAll(canvas,data)




def playGameRedrawAll(canvas, data):

    canvas.create_text(4*data.margin, data.margin/2, text="Time remaining: %d " %data.timer, font = "helvetica 15")
    canvas.create_text(data.width-2*data.margin, data.margin/2, text="score : %d" %data.score, font="helvetica 15")

    drawBoard(canvas, data)
    drawSnake(canvas, data)
    drawFood(canvas, data)
    drawGameOver(canvas, data)




def csv_writer(data, path):
    """
    Write data to a CSV file path
    """
    with open(path, "a", newline='') as csv_file:
        writer = csv.writer(csv_file, delimiter=',')
        datalist = []
        for line in data:
            # print(line)
            datalist.append(line)
        writer.writerow(datalist)


####################################
# use the run function as-is
####################################

def run(width=300, height=300):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        canvas.create_rectangle(0, 0, data.width, data.height,
                                fill='white', width=0)
        redrawAll(canvas, data)
        canvas.update()

    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data)
        if (data.gameOver and data.mode == "gameReset" and event.keysym == "s"):
            gameRestartredrawAll(canvas, data)
        else:
            redrawAllWrapper(canvas, data)

    def timerFiredWrapper(canvas, data):

        timerFired(data)

        redrawAllWrapper(canvas, data)
        # pause, then call timerFired again
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)

    def keyReleasedWrapper(event, canvas, data):
        playGameKeyReleased(event, data)
        redrawAllWrapper(canvas, data)

    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    data.timerDelay = 200 # milliseconds
    init(data)
    # create the root and the canvas
    root = Tk()
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.pack()
    # set up events
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    root.bind("<KeyRelease>", lambda  event:
                            keyReleasedWrapper(event, canvas, data))
    timerFiredWrapper(canvas, data)
    # and launch the app
    root.mainloop()  # blocks until window is closed
    print("bye!")

run(600, 600)