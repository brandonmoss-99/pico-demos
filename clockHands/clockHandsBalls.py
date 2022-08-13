from picographics import PicoGraphics, DISPLAY_PICO_DISPLAY_2, PEN_P4
import math, _thread, random

display = PicoGraphics(display=DISPLAY_PICO_DISPLAY_2, pen_type=PEN_P4)
w, h = display.get_bounds()
cWidth = w >> 1
cHeight = h >> 1

# sets up a handy function we can call to clear the screen
def clear():
    display.set_pen(BLACK)
    display.clear()

# Set brightness of display
display.set_backlight(0.8)

# RGB colours to be used
RED = display.create_pen(135,0,0)
ORANGE = display.create_pen(135,8,0)
YELLOW = display.create_pen(135,135,0)
GREEN = display.create_pen(0,135,0)
CYAN = display.create_pen(0,135,135)
BLUE = display.create_pen(0,0,135)
VIOLET = display.create_pen(50,0,135)
PINK = display.create_pen(135,0,50)
BLACK = display.create_pen(0,0,0)
D_GRAY = display.create_pen(80,80,80)
L_GRAY = display.create_pen(200,200,200)

CLOCK_RED = display.create_pen(255,0,0)
CLOCK_GREEN = display.create_pen(0,255,0)
CLOCK_CYAN = display.create_pen(0,255,255)


colours = [RED, ORANGE, YELLOW, GREEN, CYAN, BLUE, VIOLET, PINK]

class Ball:
    def __init__(self, x, y, r, dx, dy, colour):
        self.x = x
        self.y = y
        self.r = r
        self.dx = dx
        self.dy = dy
        self.colour = colour

class Line:
    def __init__(self, x1, y1, length, angle):
        self.x1 = x1
        self.y1 = y1
        self.length = length
        self.angle = math.radians(angle)
        # Set the X/Y positions to reflect the initial desired angle
        self.x2 = x1 + (length * math.sin(self.angle))
        self.y2 = y1 - (length * math.cos(self.angle))
    def rotateEnd(self, incAngle):
        # Change the line's angle by the given angle. Modulo by 360 to ensure 
        # the angle goes back to 0 after a full circular rotation, instead of 
        # continually increasing until the value encounters an overflow
        self.angle = (self.angle + math.radians(incAngle)) % 360
        # Update the end X/Y positions to reflect the new angle
        self.x2 = self.x1 + (self.length * math.sin(self.angle))
        self.y2 = self.y1 - (self.length * math.cos(self.angle))


faceRadius = 120
handRadius = 3

# Create the lines representing the clock hands
hourHand = Line(cWidth, cHeight, faceRadius-60, 0)
minuteHand = Line(cWidth, cHeight, faceRadius-30, 0)
secondHand = Line(cWidth, cHeight, faceRadius-20, 0)

# Angle to increment each time per hand
angleIncSec = 15
angleIncMin = angleIncSec/60
angleIncHr = angleIncSec/720

# Init stuff for balls
ballCount = 100
balls = []

# Create many balls with random size, random X and Y speed, and random colour
for i in range(0, ballCount):
    radius = random.randint(5,15)
    startX = random.randrange(radius+1,w-radius)
    startY = random.randrange(radius+1,h-radius)
    startDx = random.choice([-3,-2,-1,1,2,3])
    startDy = random.choice([-3,-2,-1,1,2,3])
    startColour = random.randrange(0, len(colours))
    balls.append(
        Ball(startX, startY, radius, startDx, 
            startDy, startColour)
    )


def calculateHands():
    # Calculate new angle for each hand
    secondHand.rotateEnd(angleIncSec)
    minuteHand.rotateEnd(angleIncMin)
    hourHand.rotateEnd(angleIncHr)

    # Draw to the framebuffer
    display.set_pen(CLOCK_CYAN)
    display.line(secondHand.x1, secondHand.y1, int(secondHand.x2), int(secondHand.y2))
    display.set_pen(CLOCK_GREEN)
    display.line(minuteHand.x1, minuteHand.y1, int(minuteHand.x2), int(minuteHand.y2))
    display.set_pen(CLOCK_RED)
    display.line(hourHand.x1, hourHand.y1, int(hourHand.x2), int(hourHand.y2))
    display.set_pen(L_GRAY)
    display.circle(cWidth, cHeight, handRadius)

# Do the calculations for every ball, and draw the shapes in the framebuffer
def calculateBallPositions():
    for ball in balls:
        # If edge of ball radius touches an edge, should bounce
        ballXMin = ball.r
        ballXMax = w - ball.r
        ballYMin = ball.r
        ballYMax = h - ball.r

        # If there's a collision on the X or Y axis, reverse the ball's 
        # respective direction, and change its colour to another randomly
        if ball.x <= ballXMin or ball.x >= ballXMax:
            ball.dx *= -1
        if ball.y <= ballYMin or ball.y >= ballYMax:
            ball.dy *= -1
        ball.x += ball.dx
        ball.y += ball.dy

        # Draw to the framebuffer
        display.set_pen(ball.colour)
        display.circle(ball.x, ball.y, ball.r)

# Clear display on start
clear()

while True:
    calculateBallPositions()
    calculateHands()
    display.update()
    clear()
