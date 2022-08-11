from picographics import PicoGraphics, DISPLAY_PICO_DISPLAY_2, PEN_P4
import random

# Use P4 colour mode, we don't need more than 16 colours. Saves on RAM
display = PicoGraphics(display=DISPLAY_PICO_DISPLAY_2, pen_type=PEN_P4)
display.set_backlight(0.5)
w, h = display.get_bounds()

# Store the centre of the display X,Y
cWidth = w >> 1
cHeight = h >> 1

# RGB colours to be used
RED = display.create_pen(255,0,0)
ORANGE = display.create_pen(255,128,0)
YELLOW = display.create_pen(255,255,0)
GREEN = display.create_pen(0,255,0)
CYAN = display.create_pen(0,255,255)
BLUE = display.create_pen(0,0,255)
VIOLET = display.create_pen(170,0,255)
PINK = display.create_pen(255,0,170)
BLACK = display.create_pen(0,0,0)

colours = [RED, ORANGE, YELLOW, GREEN, CYAN, BLUE, VIOLET, PINK]


# Method to clear the screen
def clear():
    display.set_pen(BLACK)
    display.clear()


class Ball:
    def __init__(self, x, y, r, dx, dy, colour):
        self.x = x
        self.y = y
        self.r = r
        self.dx = dx
        self.dy = dy
        self.colour = colour

ballCount = 100
balls = []


# Create many balls with random size, random X and Y speed, and random colour
for i in range(0, ballCount):
    radius = random.randint(5,15)
    startX = random.randrange(radius+1,w-radius)
    startY = random.randrange(radius+1,h-radius)
    startDx = random.randint(-10,10)
    startDy = random.randint(-10,10)
    startColour = random.randrange(0, len(colours))
    balls.append(
        Ball(startX, startY, radius, startDx, 
            startDy, startColour)
    )


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
            ball.colour = random.randrange(0, len(colours))
        if ball.y <= ballYMin or ball.y >= ballYMax:
            ball.dy *= -1
            ball.colour = random.randrange(0, len(colours))
        ball.x += ball.dx
        ball.y += ball.dy

        display.set_pen(ball.colour)
        display.circle(ball.x, ball.y, ball.r)


while True:
    clear()
    calculateBallPositions()
    display.update()
