from picographics import PicoGraphics, DISPLAY_PICO_DISPLAY_2, PEN_P4
import math 

display = PicoGraphics(display=DISPLAY_PICO_DISPLAY_2, pen_type=PEN_P4)
w, h = display.get_bounds()
cWidth = w >> 1
cHeight = h >> 1
# Set brightness of display
display.set_backlight(0.8)

BLACK = display.create_pen(0,0,0)
GREEN = display.create_pen(0,255,0)
RED = display.create_pen(255,0,0)

# Function to clear the screen
def clear():
    display.set_pen(BLACK)
    display.clear()


class Point:
    def __init__(self, x=0, y=0, z=0):
        self.x, self.y, self.z = x, y, z

class Triangle:
    def __init__(self, p1, p2, p3):
        self.points = [p1, p2, p3]

class Quad:
    def __init__(self, p1, p2, p3, p4):
        self.points = [p1, p2, p3, p4]


def draw(shape):
    # Size of the shape, based off the length of the shape's points structure
    shapeSize = len(shape.points)-1
    # Draw all but the last 'connecting' line
    for p in range(0,shapeSize):
        display.line(int(shape.points[p].x), int(shape.points[p].y), int(shape.points[p+1].x), int(shape.points[p+1].y))
    # Draw the final connecting line back to the first point on the shape
    display.line(int(shape.points[shapeSize].x), int(shape.points[shapeSize].y), int(shape.points[0].x), int(shape.points[0].y))

# Rotate about a pivot Point(x,y), for a given angle
def rotate(shape, angle, pivot):
    # Convert from degrees to radians
    angle = math.radians(angle)
    for p in range(0, len(shape.points)):
        # Shift the pivot point to the origin, and the Triangle's point
        xShifted = shape.points[p].x - pivot.x
        yShifted = shape.points[p].y - pivot.y
        # Calculate the point's rotation from the origin, and then shift back
        shape.points[p].x = pivot.x + (xShifted * math.cos(angle) - yShifted * math.sin(angle))
        shape.points[p].y = pivot.y + (xShifted * math.sin(angle) + yShifted * math.cos(angle))

# Shift the object by x,y
def shift(shape, x, y):
    for p in range(0, len(shape.points)):
        shape.points[p].x += x
        shape.points[p].y += y

# Scale the object by a scale factor, from origin Point(x,y)
def scale(shape, scale, origin):
    for p in range(0, len(shape.points)):
        # Shift the pivot point to the origin, and the Triangle's point
        xShifted = shape.points[p].x - origin.x
        yShifted = shape.points[p].y - origin.y
        # Calculate the point's rotation from the origin, and then shift back
        shape.points[p].x = origin.x + (xShifted * scale)
        shape.points[p].y = origin.y + (yShifted * scale)


newTriangle = Triangle(Point(cWidth, cHeight), Point(cWidth+50, cHeight+20), Point(cWidth - 80, cHeight+90))
square1 = Quad(Point(10, 10), Point(80, 10), Point(80, 80), Point(10, 80))
square2 = Quad(Point(200, 200), Point(230, 200), Point(230, 230), Point(200, 230))


# Clear display on start
clear()
while True:
    display.set_pen(GREEN)
    rotate(newTriangle, 1, Point(cWidth,cHeight))
    draw(newTriangle)

    display.set_pen(RED)
    rotate(square1, 5, Point(80,80))
    draw(square1)

    rotate(square2, -10, Point(215, 215))
    draw(square2)
    
    display.update()
    clear()
