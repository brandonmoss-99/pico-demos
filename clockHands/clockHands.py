from picographics import PicoGraphics, DISPLAY_PICO_DISPLAY_2, PEN_P4
import math

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

RED = display.create_pen(255,0,0)
GREEN = display.create_pen(0,255,0)
BLACK = display.create_pen(0, 0, 0)
BLUE = display.create_pen(0,200,255)
D_GRAY = display.create_pen(80,80,80)
L_GRAY = display.create_pen(200,200,200)

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

def calculateHands():
    # Calculate new angle for each hand
    secondHand.rotateEnd(angleIncSec)
    minuteHand.rotateEnd(angleIncMin)
    hourHand.rotateEnd(angleIncHr)

    # Draw to the framebuffer
    display.set_pen(D_GRAY)
    display.circle(cWidth, cHeight, faceRadius)
    display.set_pen(BLUE)
    display.line(secondHand.x1, secondHand.y1, int(secondHand.x2), int(secondHand.y2))
    display.set_pen(GREEN)
    display.line(minuteHand.x1, minuteHand.y1, int(minuteHand.x2), int(minuteHand.y2))
    display.set_pen(RED)
    display.line(hourHand.x1, hourHand.y1, int(hourHand.x2), int(hourHand.y2))
    display.set_pen(L_GRAY)
    display.circle(cWidth, cHeight, handRadius)


# Clear display on start
clear()
while True:
    # Draw to the framebuffer
    calculateHands()
    # Draw framebuffer to the screen
    display.update()
    clear()
