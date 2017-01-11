from microbit import *
import radio
import neopixel

global np
np = neopixel.NeoPixel(pin13, 12)

def moveRobot(pin0Val, pin8Val, pin1Val, pin12Val):
    pin0.write_digital(pin0Val)
    pin8.write_digital(pin8Val)
    pin1.write_digital(pin1Val)
    pin12.write_digital(pin12Val)


def goForward():
    moveRobot(1, 0, 1, 0)
def goBackwards():
    moveRobot(0, 1, 0, 1)
def turnRight():
    moveRobot(1, 0, 0, 0)
def turnLeft():
    moveRobot(0, 0, 1, 0)
def stopMoving():
    moveRobot(0, 0, 0, 0)


def executeRightTurn():
    lightUpPixels(6, 12, 50, 200, 50)
    turnRight()
    
def executeLeftTurn():
    lightUpPixels(0, 6, 50, 200, 50)
    turnLeft()

def executeMoveForward():
    lightUpPixels(0, 12, 200, 200, 200)
    goForward()

def executeMoveBackward():
    lightUpPixels(0, 12, 200, 50, 50)
    goBackwards()

def executeStopMoving():
    stopMoving()
    
def processMoveInstruction(moveStr):
    if moveStr == "L":
        executeLeftTurn()
        return
    if moveStr == "R":
        executeRightTurn()
        return
    if moveStr == "F":      # bitbot wheelies when going from B to F.  Below halts the wheelie.
        stopMoving()        # note it is important we don't wheelie - when the bitbot is following
        sleep(15)           # a path the wheelie causes direction to be erratic.
        executeMoveForward()
        return
    if moveStr == "B":
        executeMoveBackward()
        return
    if moveStr == "S":
        executeStopMoving()
        return
    if moveStr == "E":
        stopMoving()
        turnPixelsOff()
        return

def flashLights():
    turnPixelsOff()
    
    for i in range(0, 6):
        np[i]       = (10, 50, 140 + 10*i)
        np[i + 6]   = (10, 50, 140 + 10*i)
        sleep(1000 - 20 * i)

def lightUpPixels(st, fin, r, g, b):
    turnPixelsOff()
    for i in range(st, fin):
        np[i] = (r, g, b)
    np.show()


def turnPixelsOff():
    for i in range(0, 12):
        np[i] = (0, 0, 0)
    np.show()

radio.on()

while True:
    message = radio.receive()
    processMoveInstruction(message)
    