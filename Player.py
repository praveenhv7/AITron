
from constants import *

class Player(object):


    # Called when Snake() is called
    def __init__(self, posx, posy, color):
        self.pos = (posx, posy)  # Position of the snake's head
        self.body = []  # List holding the coordinates of the snake's body
        self.length = 3  # Length of the snake
        self.angle = 0  # Direction that the snake is facing
        self.alive = True  # Is he alive, or dead?
        self.color = color
        self.hitOwnBody = False

    def reset(self, posx, posy):
        self.pos = (posx, posy)  # Position of the snake's head
        self.body.clear()
        self.angle = 0  # Direction that the snake is facing
        self.alive = True  # Is he alive, or dead?

    def getLegalMoves(self, walls):
        legalmoves = []
        x, y = self.pos

        if self.isLegalMove(self.getPositionInFront(self.angle), walls):
            legalmoves.append(self.angle)
        if self.isLegalMove(self.getPositionInFront((self.angle + 90) % 360),walls):
            legalmoves.append((self.angle + 90) % 360)
        if self.isLegalMove(self.getPositionInFront((self.angle - 90) % 360), walls):
            legalmoves.append((self.angle - 90) % 360)
        return legalmoves

    def isLegalMove(self, pos, walls):
        if pos[0] > GAME.SCREEN_WIDTH - GAME.MOVE_LENGTH or pos[0] < 0 :
            return False
        elif pos[1] > GAME.PLAY_AREA_HEIGHT or pos[1] < 0:
            return  False
        elif pos in walls:
            return False
        return True

    def isWallNextPos(self, walls):
        return not self.isLegalMove(self.getPositionInFront(self.angle), walls)

    def getPositionInFront(self, angle):
        x, y = self.pos
        if angle == Directions.NORTH:
            y -= GAME.MOVE_LENGTH
        if angle == Directions.EAST:
            x -= GAME.MOVE_LENGTH
        if angle == Directions.SOUTH:
            y += GAME.MOVE_LENGTH
        if angle == Directions.WEST:
            x += GAME.MOVE_LENGTH
        return (x, y)

    # Called once every frame
    def update(self, walls):

        # Insert the new position of the snake's head
        self.body.insert(0, self.pos)
        # Move 16 pixels according to the angle
        x, y = self.pos
        if self.angle == Directions.NORTH:
            y -= GAME.MOVE_LENGTH
        if self.angle == Directions.EAST:
            x -= GAME.MOVE_LENGTH
        if self.angle == Directions.SOUTH:
            y += GAME.MOVE_LENGTH
        if self.angle == Directions.WEST:
            x += GAME.MOVE_LENGTH
        self.pos = (x, y)

        walls.add(self.pos)
        #print(self.pos)

        # If your head ran into your body, die!
        if self.pos in self.body:
            self.alive = False
            self.hitOwnBody = True


        # If your body is not in the 320x320 screen area, die!
        if self.pos[0] > GAME.SCREEN_WIDTH - GAME.MOVE_LENGTH or self.pos[0] < 0:
            self.alive = False
        elif self.pos[1] > GAME.PLAY_AREA_HEIGHT or self.pos[1] < 0:
            self.alive = False



    # Draws the character
    def draw(self, surf):

        # Draw the head
        surf.fill(self.color, (self.pos[0], self.pos[1], GAME.MOVE_LENGTH, GAME.MOVE_LENGTH))

        # Draw the body
        for b in self.body:
            surf.fill(self.color, (b[0], b[1], GAME.MOVE_LENGTH, GAME.MOVE_LENGTH))
