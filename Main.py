__author__ = 'henrikmnm'


from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math
import Board
import fileHandler
import CheckerPiece as piece
import copy

# The main class which is responsible for setting up the structure of the program and driving the openGL-drawing. Its
# run-method assigns all of the openGL-functions and makes sure that keypresses and drawing is done.

class Main:

    indicatorZ = 0.8
    special_key = None
    key = None

    yRotationAngle = 0.0
    zRotationAngle = 0.0

    window_height = 0
    window_width = 0

    camera = (-10, 10, 0)

    currentPiece = 0

    currentScene = 1

    board = None

    filer = 0

    leftMove = 0

    rightMove = 0

    movementCounter = 0

    def __init__(self):
        pass


    def getBoard(self):
        return self.board

    def handleKeypress(self, key, x ,y ):

        self.key = key

        if key == 'q':
            exit(0)

    def specialPressed(self, key, x, y):
        if self.rightMove or self.leftMove:
            pass
        else:
            self.special_key = key

    def run(self):
        glutInit()
        glutInitDisplayMode(GLUT_RGBA , GLUT_ALPHA , GLUT_DOUBLE , GLUT_DEPTH )

        glutInitWindowSize(800, 600) #Set the window size
        self.window_width = 800
        self.window_height = 600

        self.board = Board.Board(4, 4, -4, -4)

        self.filer = fileHandler.fileHandler("centers3.txt", 4, 4)
        self.filer.readPieces()

        pieces = self.filer.getPecies()


        for p in pieces:
            self.board.addPiece(p)

        self.initialBoard = copy.deepcopy(self.board.getPieces())

        self.currentPiece = self.board.getPieces()[0]

        #Create the window
        glutCreateWindow("Project 2015")

        #Set handler functions for drawing, keypresses, and window resizes

        glutDisplayFunc(self.drawScene)
        glutKeyboardFunc(self.handleKeypress)
        glutReshapeFunc(self.handleResize)
        glutSpecialFunc(self.specialPressed)
        glutIdleFunc(self.Idle)

        glutMainLoop() #Start the main loop

    def Idle(self):

        if self.key == 's':
            print("Pil ned.")

            self.camera = (self.camera[0]+self.camera[0]/4, self.camera[1]+self.camera[1]/4, self.camera[2]+self.camera[2]/4)

        elif self.key == 'w':
            print("Pil opp.")

            self.camera = (self.camera[0]-self.camera[0]/4, self.camera[1]-self.camera[1]/4, self.camera[2]-self.camera[2]/4)

        elif self.key == 'a':
            print("A")
            self.yRotationAngle += 5

        elif self.key == 'd':
            print("D")
            self.yRotationAngle -= 5

        elif self.key == 't':
            self.zRotationAngle += 5

        elif self.key == 'g':
            self.zRotationAngle -= 5


        if self.special_key == GLUT_KEY_LEFT and not self.board.pieceAtPos(self.roundOff(self.currentPiece.getX())+1, self.roundOff(self.currentPiece.getY())-1)  and self.currentPiece.getX()+1 <= self.board.getWidth() and self.currentPiece.getY()-1 >= -self.board.getWidth():
            self.movementCounter = 0
            self.leftMove = True

        elif self.special_key == GLUT_KEY_RIGHT and not self.board.pieceAtPos(self.roundOff(self.currentPiece.getX())+1, self.roundOff(self.currentPiece.getY())+1) and self.currentPiece.getX()+1 <= self.board.getWidth() and self.currentPiece.getY()+1 <= self.board.getWidth():
            self.movementCounter = 0
            self.rightMove = True

        elif self.special_key == GLUT_KEY_LEFT or self.special_key == GLUT_KEY_RIGHT:
            self.currentPiece.setHasMoved()


        if self.currentPiece.getHasMoved():
            self.currentPiece.setNotMoved()
            self.nextPiece()

        self.key = 0
        self.special_key = 0

        glutPostRedisplay()

    def handleResize(self, width, height):

        glViewport(0,0,width, height)

        glMatrixMode(GL_PROJECTION)

        glLoadIdentity()

        gluPerspective(60.0, 4/3, 1,200)

        glMatrixMode(GL_MODELVIEW)

    def drawScene(self):

        glClear(GL_COLOR_BUFFER_BIT, GL_DEPTH_BUFFER_BIT)

        glClearColor(0.0, 0.0,0.0,1.0)

        glLoadIdentity()

        gluLookAt(
            self.camera[0], self.camera[1], self.camera[2],
            0.0, 0.0, 0.0,
            0.0, 1.0, 0.0)

        glRotatef(self.yRotationAngle,0,1,0)

        glRotatef(self.zRotationAngle,0,0,1)


        if self.leftMove:
            if self.movementCounter != 50:
                if self.movementCounter < 25:
                    self.currentPiece.incrementZ()
                    self.indicatorZ += 0.03
                else:
                    self.currentPiece.decrementZ()
                    self.indicatorZ -= 0.03
                self.currentPiece.incrementX()
                self.currentPiece.decrementY()
                self.movementCounter += 1
            else:

                self.currentPiece.setHasMoved()
                self.leftMove = False

        if self.rightMove:
            if self.movementCounter != 50:
                if self.movementCounter < 25:
                    self.currentPiece.incrementZ()
                    self.indicatorZ += 0.03
                else:
                    self.currentPiece.decrementZ()
                    self.indicatorZ -= 0.03
                self.currentPiece.incrementX()
                self.currentPiece.incrementY()
                self.movementCounter += 1
            else:

                self.currentPiece.setHasMoved()
                self.rightMove = False

        self.drawBottom()
        self.drawSides()
        self.drawBoard(4,4)

        self.drawPieces()

        self.drawIndicator()

        glutSwapBuffers()

    def drawBoard(self,width, height ):

        alt = False
        for x in range(-width,width):

            for z in range(-height,height):

                if alt:
                    if z % 2 == 0:
                        glColor4f(1.0,0.0,0.0,1.0)
                    else:
                        glColor4f(0.0,0.0,1.0,1.0)
                else:
                    if z % 2 == 0:
                        glColor4f(0.0,0.0,1.0,1.0)
                    else:
                        glColor4f(1.0,0.0,0.0,1.0)

                self.drawSquare(x, 0, z, x+1, 0, z, x+1, 0, z+1, x, 0, z+1)

            if not alt:
                alt = True
            else:
                alt = False

    def drawSquare(self, x1, y1, z1, x2, y2, z2, x3, y3, z3, x4, y4, z4):
        glBegin(GL_QUADS)
        glVertex3f(x1, y1, z1)
        glVertex3f(x2, y2, z2)
        glVertex3f(x3, y3 ,z3)
        glVertex3f(x4 ,y4 ,z4)
        glEnd()

    def drawSides(self):

        glColor4f(1.0,1.0,1.0,1.0)

        self.drawSquare(self.board.getXStart(), 0, self.board.getZStart(),
                        self.board.getXStart()-0.2, -1, self.board.getZStart()-0.2,
                        self.board.getWidth()+0.2, -1, self.board.getZStart()-0.2,
                        self.board.getWidth(), 0, self.board.getZStart())

        self.drawSquare(self.board.getXStart(), 0, self.board.getZStart(),
                        self.board.getXStart()-0.2, -1, self.board.getZStart()-0.2,
                        self.board.getXStart()-0.2, -1, self.board.getWidth()+0.2,
                        self.board.getXStart(), 0, self.board.getWidth())

        self.drawSquare(self.board.getWidth(), 0, self.board.getWidth(),
                        self.board.getWidth()+0.2, -1, self.board.getWidth()+0.2,
                        self.board.getWidth()+0.2, -1, self.board.getZStart()-0.2,
                        self.board.getWidth(), 0, self.board.getZStart())

        self.drawSquare(self.board.getWidth(), 0, self.board.getWidth(),
                        self.board.getWidth()+0.2, -1, self.board.getWidth()+0.2,
                        self.board.getXStart()-0.2, -1, self.board.getWidth()+0.2,
                        self.board.getXStart(), 0, self.board.getWidth())

    def drawBottom(self):
        glColor3f(0.5,0.7,0.0)

        self.drawSquare(self.board.getXStart()-0.2, -1, self.board.getZStart()-0.2,
                        self.board.getWidth()+0.2, -1, self.board.getZStart()-0.2,
                        self.board.getWidth()+0.2, -1, self.board.getWidth()+0.2,
                        self.board.getXStart()-0.2, -1, self.board.getWidth()+0.2)

    def addPieces(self):
        fHandler = fileHandler.fileHandler("centers.txt")

        fHandler.readPieces()

        pieces = fHandler.getPecies()

        for piece in pieces:
            self.board.addPiece(piece)

    def drawPiece(self, piece):
        x = piece.getX()
        y = piece.getY()
        z = piece.getZ()
        color = piece.getColor()


        if color == 'red':
            glColor3f(1.0,0.0,0.0)
            #Bottom
            self.drawSquare(x-0.3,z,y-0.3,
                            x-0.3,z,y+0.3,
                            x+0.3,z,y+0.3,
                            x+0.3,z,y-0.3)
            #Side 1
            self.drawSquare(x-0.3,z,y-0.3,
                            x-0.3,z+0.5,y-0.3,
                            x-0.3,z+0.5,y+0.3,
                            x-0.3,z,y+0.3)
            #Side 2
            self.drawSquare(x-0.3,z,y-0.3,
                            x-0.3,z+0.5,y-0.3,
                            x+0.3,z+0.5,y+0.3,
                            x+0.3,z,y+0.3)
            #Side 3
            self.drawSquare(x+0.3,z,y-0.3,
                            x+0.3,z+0.5,y-0.3,
                            x+0.3,z+0.5,y+0.3,
                            x+0.3,z,y+0.3)
            #Side 4
            self.drawSquare(x+0.3,z,y+0.3,
                            x+0.3,z+0.5,y+0.3,
                            x-0.3,z+0.5,y+0.3,
                            x-0.3,z,y+0.3)
            #Top
            self.drawSquare(x-0.3,z+0.5,y-0.3,
                            x-0.3,z+0.5,y+0.3,
                            x+0.3,z+0.5,y+0.3,
                            x+0.3,z+0.5,y-0.3)
        else:
            glColor3f(1.0,1.0,1.0)
            #Bottom
            self.drawSquare(x-0.3,z,y-0.3,
                            x-0.3,z,y+0.3,
                            x+0.3,z,y+0.3,
                            x+0.3,z,y-0.3)
            #Side 1
            self.drawTriangle(x-0.3,z,y-0.3,
                              x,z+0.7,y,
                              x-0.3,z,y+0.3)
            #Side 2
            self.drawTriangle(x-0.3,z,y-0.3,
                              x,z+0.7,y,
                              x+0.3,z,y-0.3)
            #Side 3
            self.drawTriangle(x+0.3,z,y-0.3,
                              x,z+0.7,y,
                              x+0.3,z,y+0.3)
            #Side 4
            self.drawTriangle(x+0.3,z,y+0.3,
                              x,z+0.7,y,
                              x-0.3,z,y+0.3)

    def drawPieces(self):

        for piece in self.board.getPieces():
            self.drawPiece(piece)

    def drawTriangle(self,x1, y1, z1, x2, y2, z2, x3, y3, z3):
        glBegin(GL_TRIANGLES)
        glVertex3f(x1,y1,z1)
        glVertex3f(x2,y2,z2)
        glVertex3f(x3,y3,z3)
        glEnd()

    def initBoard(self):
        self.board.addPiece(piece.Piece(-1,-2,1, self.board.getWidth(), self.board.getLength()))
        self.board.addPiece(piece.Piece(-2,-1,1, self.board.getWidth(), self.board.getLength()))
        self.board.addPiece(piece.Piece(-3,-3,2, self.board.getWidth(), self.board.getLength()))
        self.board.addPiece(piece.Piece(-3,-1,2, self.board.getWidth(), self.board.getLength()))
        self.board.addPiece(piece.Piece(-2,2,2, self.board.getWidth(), self.board.getLength()))

    def nextPiece(self):
        for i in range(len(self.board.getPieces())):
            if self.currentPiece == self.board.getPieces()[i] and i < len(self.board.getPieces())-1:
                self.currentPiece = self.board.getPieces()[i+1]
                break
            elif self.currentPiece == self.board.getPieces()[i] and i == len(self.board.getPieces())-1:
                self.currentPiece = self.board.getPieces()[0]
                break

    def drawIndicator(self):
        x = self.currentPiece.getX()
        y = self.currentPiece.getY()

        glColor3f(1,0,1)
        glBegin(GL_LINES)
        glVertex3f(x,self.indicatorZ,y)
        glVertex3f(x,self.indicatorZ+1,y)
        glEnd()

    def roundOff(self,x):
        recidual = x%1

        if recidual > 0.5:
            return math.ceil(x)
        else:
            return math.floor(x)


main = Main()

main.run()
