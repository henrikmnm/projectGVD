__author__ = 'henrikmnm'
import math


# Class for holding information about the board that is drawn in the main-class.
class Board:
    width = 0
    length = 0
    xStart = 0
    zStart = 0
    pieces = []

    def __init__(self, width, length, xStart, zStart):
        self.length = length
        self.width = width
        self.xStart = xStart
        self.zStart = zStart


    def getLength(self):
        return self.length

    def getWidth(self):
        return self.width

    def getXStart(self):
        return self.xStart

    def getZStart(self):
        return self.zStart

    def addPiece(self, piece):
        self.pieces.append(piece)

    def getPieces(self):
        return self.pieces

    # Method for checking whether there is a piece at a given location.
    def pieceAtPos(self, x, y):
        for p in self.pieces:
            if self.roundOff(p.getX()) == x and self.roundOff(p.getY()) == y:
                return True
        return False

    def roundOff(self,x):
        recidual = x%1

        if recidual > 0.5:
            return math.ceil(x)
        else:
            return math.floor(x)

    def setPieces(self, x):
        self.pieces = x

