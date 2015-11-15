__author__ = 'henrikmnm'
from time import sleep
import math

# Class for holding the information of a checker-piece. Includes holders for x and y coordinates as well as color of the
# piece itself. The class also implements method for incrementing and decrementing its x, y and z coordinates. This is done
# so that the main class can smoothly animate the checker piece movements.as


class Piece:

    # OpenGL - coordinates
    x = 0
    y = 0
    z = 0

    # Width and height of the checkerboard.
    width = 0
    height = 0
    color = 0

    # Boolean to check whether the piece has moved after being selected.
    hasMoved = False


    def __init__(self, x, y,color, width, height):
        # Coordinate conversion to get pieces to align with center of square on the board.
        if x > 0:
            self.x = x - 0.5
        else:
            self.x = x + 0.5

        if y > 0:
            self.y = y - 0.5
        else:
            self.y = y + 0.5

        # Variables to ensure that the piece never moves outside the board.
        self.width = width
        self.height = height

        # Assign the color of the piece based on what value that is provided to the constructor.
        if color == 1:
            self.color = 'red'
        else:
            self.color = 'white'

    def getX(self):
        return self.x

    def getY(self):
        return self.y

    def getColor(self):
        return self.color

    def incrementX(self):
        self.x += 0.02

    def incrementY(self):
        self.y += 0.02

    def decrementY(self):
        self.y -= 0.02

    def incrementZ(self):
        self.z += 0.03

    def decrementZ(self):
        self.z -= 0.03

    def getHasMoved(self):
        return self.hasMoved

    def setNotMoved(self):
        self.hasMoved = False

    def setHasMoved(self):
        self.hasMoved = True

    def getZ(self):
        return self.z







