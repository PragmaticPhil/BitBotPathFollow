# Add your Python code here. E.g.
from microbit import *
import radio

radio.on()

# This app does 2 things:
#   1 = take user input and translate into radio signal
#   2 = record the user input, and later play back over radio
# this means we record path of a robot then replay the same path.

# below are used to infer button (or general event) released:
global buttonAPressed
buttonAPressed = 0
global buttonBPressed
buttonBPressed = 0
global tiltForward
tiltForward = 0
global tiltBack
tiltBack = 0
global shake
shake = 0
# these toggles ensure that only 1 radio alert is sent per event type.

# ones below are for writing path to file:
global movementStartTime
movementStartTime = running_time()
global autonomousMode
autonomousMode = 0
global travelDirection
travelDirection = 0
global movement_file
global numberOfMoves
numberOfMoves = 0

# FILE IO:-----------------------------------------------------------------------
def writeToFile(moveDetails):
    global movement_file
    try:
        movement_file.write(moveDetails)
    except:
        display.show("Ex01 - can't write to file")
        sleep(2000)


def writeMovementToFile(currentMove):
    newMoveData = getMoveDurationStr() + currentMove
    writeToFile(newMoveData)
    addAMove()


# Calculating & padding DURATION & reading from raw file string:----------------------
def getMoveDurationStr():
    global movementStartTime
    moveDuration = str(running_time() - movementStartTime)
    movementStartTime = running_time()
    return padMoveDurationStr(moveDuration)


def padMoveDurationStr(rawDuration):   #always 5 chars, ensures move rec is 6 long
    if(len(rawDuration) > 5):
        return "99999"
    while(len(rawDuration) < 5):
        rawDuration = "0" + rawDuration
    return rawDuration


def getMoveDuration(rawMoveStr):
    durStr = rawMoveStr[1: len(rawMoveStr)]
    try:
        return int(durStr)
    except:
        return 0


# Processing ACCELEROMETER input:------------------------------------
def interpretAccelerometerReading():
    if(accelerometer.is_gesture('shake')):
        return "X"
    tiltY = accelerometer.get_y()
    if(tiltY < -650):
        return "F"
    if(tiltY > 650):
        return "B"
    return "Z"


def processAcceleratorInput(acceleratorInput):
    global tiltForward
    global tiltBack
    global shake
    global travelDirection
    
    if(acceleratorInput == "Z"):
        shake = 0
        tiltForward = 0
        tiltBack = 0
        return

    if(acceleratorInput == "F"):
        if(tiltForward == 0):
            travelDirection = travelDirection + 1
            if(travelDirection >= 1):
                travelDirection = 1
                executeMoveInstruction(acceleratorInput)
                display.show(acceleratorInput)
            else:
                executeMoveInstruction("S")
                display.show("S")
        tiltForward = 1
        return

    if(acceleratorInput == "B"):
        if(tiltBack == 0):
            travelDirection = travelDirection - 1
            if(travelDirection < -1):
                travelDirection = -1
                executeMoveInstruction(acceleratorInput)
                display.show(acceleratorInput)
            else:
                executeMoveInstruction("S")
                display.show("S")
           
        tiltBack = 1


# Processing BUTTON input:---------------------------------------------------
def processButtonInputs():
    global buttonAPressed
    global buttonBPressed
    
    if button_a.is_pressed():               # When button a is pressed, we check if it is in a 'pressed' state:
        if (buttonAPressed == 0):           # 0 here means radio hasn't been sent for this press event
            executeMoveInstruction("L")     # only want to send once - rem - sending to a state machine
            display.show("L")
        buttonAPressed = 1                  # sustained pressing does not trigger radio (but of course avoids else below)
    else:                                   # now the button has been released
        if (buttonAPressed == 1):           # we check if this is the first time the button release has been registered
            returnToOriginalPath()          # if so send the radio note
            display.show("l")
        buttonAPressed = 0                  # and reset counter so next button press is registered afresh.

    if button_b.is_pressed():               # what we do here is only send 2 notes over radio for each button press
        if (buttonBPressed == 0):
            executeMoveInstruction("R")
            display.show("R")
        buttonBPressed = 1
    else:
        if (buttonBPressed == 1):
            returnToOriginalPath()
            display.show("r")
        buttonBPressed = 0


# Functions that enable the path to be read and followerd:-------------------------
def processMove(rawMoveStr):
    directionStr = rawMoveStr[0]
    if(directionStr == "S"):
        return
    duration = getMoveDuration(rawMoveStr)
    radio.send(directionStr)
    sleep(duration)


def retracePath():
    global numberOfMoves
    try:
        pathFile = open('robotPath.txt')
        for i in range(1, numberOfMoves):   # show me a decent while with EOF to use instead pls!
            strBuf = pathFile.read(6)
            processMove(strBuf)
    except:     # donothing - probs just read beyond EOF - not stressing - we're not on mars here ;)
       sleep(1) # cos of course I'm not allowed to do nothing.
    radio.send("E")

def initialisePathFile():   # of course where this is called from means file is always
    global movement_file    # overwritten every time the mb is reset.  TODO
    movement_file = open('robotPath.txt', 'w')
    movement_file.write("S")


# And some uncategorised utilities:----------------------------------
def toggleAutonomousMode():     # AM = 0 means OFF (i.e. robot is steered manually)
    global autonomousMode
    if(autonomousMode == 0):    autonomousMode = 1
    else:                       autonomousMode = 0


def returnToOriginalPath():             # to get the good turn effect the robot
    global travelDirection              # needs to return to its original, 
    if(travelDirection >= 1):           # pre-turn path after turning L or R
        executeMoveInstruction("F")     # on button up when the turn is complete
        return                  
    if(travelDirection <= -1):
        executeMoveInstruction("B")
        return
    executeMoveInstruction("S")


def executeMoveInstruction(moveStr):
    writeMovementToFile(moveStr)
    radio.send(moveStr)


def addAMove():
    global numberOfMoves
    numberOfMoves = numberOfMoves + 1


initialisePathFile()

while True:

    acceleratorInput = interpretAccelerometerReading()
            
    if(acceleratorInput == "X"):
        if(shake == 0):
            toggleAutonomousMode()
        shake = 1

    if(autonomousMode == 0):
        processButtonInputs()
        processAcceleratorInput(acceleratorInput)
    else:
        if button_a.is_pressed():
            movement_file.close()
            retracePath()
        if button_b.is_pressed():
            initialisePathFile()
            toggleAutonomousMode = 0