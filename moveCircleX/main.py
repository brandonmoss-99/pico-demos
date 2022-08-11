from picographics import PicoGraphics, DISPLAY_PICO_DISPLAY_2, PEN_P4

# Use P4 colour mode, we don't need more than 16 colours. Saves on RAM
display = PicoGraphics(display=DISPLAY_PICO_DISPLAY_2, pen_type=PEN_P4)
display.set_backlight(0.5)
w, h = display.get_bounds()

# Store the centre of the display X,Y
cWidth = w >> 1
cHeight = h >> 1

RED = display.create_pen(255,0,0)
GREEN = display.create_pen(0,255,0)
BLACK = display.create_pen(0,0,0)

def clear():
    display.set_pen(BLACK)
    display.clear()

# Hidden black square following behind the circle being drawn, to clear up 
# it's path, without having to perform a full display clear
def clearPosXMovCircle(x, y, r):
    display.set_pen(BLACK)
    # Start point (X,Y), width and height of rectangle
    display.rectangle(x-2*r, y-r, r*2+1, r*2+1)

# Draw black square to clear up, instead of performing a full display clear
def clearStillCircle(x, y, r):
    display.set_pen(BLACK)
    display.rectangle(x-r, y-r, r*2+1, r*2+1)

clear()
while True:
    for radius in range(5, 100, 25):
        for xPos in range(0, w+radius+1, 5):
            # Clear up trail from previous circle
            clearPosXMovCircle(xPos, cHeight, radius)
            display.set_pen(RED)
            display.circle(cWidth, cHeight, radius)
            display.set_pen(GREEN)
            display.circle(xPos, cHeight, radius >> 1)
            # Push new contents to screen
            display.update()
        # Clear up red circle pre-size change
        clearStillCircle(cWidth, cHeight, radius)
