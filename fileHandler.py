__author__ = 'henrikmnm'

import CheckerPiece as piece
import math


# Class for reading coordinates from text file and create checkerPiece-objects for holding this information.
class fileHandler:
    url = 0
    width = 0
    height = 0

    pieces = []

    def __init__(self, url, width, height):
        self.url = url
        self.width = width
        self.height = height

    # Method for reading a file and create checkerPiece-objects of this information. The method also takes care of
    # coordinate conversion, from pixel-values in matlab to board-coordinates in this program.
    def readPieces(self):
        pieces = open(self.url, 'r')

        for line in pieces:
            x = 0
            y = 0
            color = 0
            info = line.split(' ')

            for i in range(len(info)):
                if info[i] == "X:":
                    x = int(info[i+1].strip())
                elif info[i] == "Y:":
                    y = int(info[i+1].strip())
                elif info[i] == "Color:":
                    color = int(info[i+1].strip())

            (x1, y1) = self.translateCoordinates(x, y)

            self.pieces.append(piece.Piece( y1, x1, color, self.width, self.height ))

    def getPecies(self):
        return self.pieces

    # Method for transforming pixel-values to board-coordinates.
    def translateCoordinates(self, x, y):
        if(x > 400):
            x = x - 400
            x = self.roundOff(x/100) + 1
        elif x < 400:
            x = 400 - x
            x = -(self.roundOff(x/100)) - 1

        if y < 100:
            y = 1
        elif y > 100:
            y -= 100
            y = -y/100
            y = self.roundOff(y)


        return x, y

    # Rounding-function.
    def roundOff(self,x):

        if x > 0:
            return math.ceil(x)
        else:
            return math.floor(x)