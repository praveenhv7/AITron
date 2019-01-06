import logging

from constants import *
from Player import Player
import copy
import random
import numpy as np
class GameState(object):

    def __init__(self):

        # self.tronPlayer1 = Player(GAME.PLAYER1_XPOS, GAME.PLAYER1_YPOS, COLOR.BLUE)
        # self.tronPlayer2 = Player(GAME.PLAYER2_XPOS, GAME.PLAYER2_YPOS, COLOR.RED)
        self.tronPlayer1 = Player(int(random.randint(0,GAME.SCREEN_WIDTH)/16)*16, int(random.randint(0,GAME.PLAY_AREA_HEIGHT)/16)*16, COLOR.BLUE)
       # self.tronPlayer2 = Player(int(random.randint(0, GAME.SCREEN_WIDTH)/16)*16, int(random.randint(0, GAME.PLAY_AREA_HEIGHT)/16)*16,
       #                           COLOR.RED)
        #self.tronPlayer1 = Player(160, 304, COLOR.BLUE)
        self.tronPlayer2 = Player(320, 304,COLOR.RED)
        self.tronPlayer2.body = [(320,300),(320,296)]
        #self.tronPlayer1.angle = 270
        #self.tronPlayer2.angle = 90
        self.MAX_WIDTH = GAME.SCREEN_WIDTH
        self.MAX_HEIGHT = GAME.PLAY_AREA_HEIGHT
        self.MOVE_LENGTH = GAME.MOVE_LENGTH
        self.walls = set()
        self.qValues = {}
        self.visitedCoOrds = []
        self.regions = 1
        self.pathToOtherHead = []
        self.p1SpaceLeft = 0
        self.p2SpaceLeft = 0
        self.score = 0
        self.walls.add(self.tronPlayer1.pos)
        self.walls.add(self.tronPlayer2.pos)
        self.clockTick = 0

    def getScore(self):
        return self.score

    def getPlayer(self, player):
        return self.tronPlayer1 if player is "One" else self.tronPlayer2

    def getMinPlayer(self, player):
        return self.tronPlayer2 if player is "One" else self.tronPlayer1

    def reset(self):
        self.tronPlayer1.reset(GAME.PLAYER1_XPOS, GAME.PLAYER1_YPOS)
        self.tronPlayer2.reset(GAME.PLAYER2_XPOS, GAME.PLAYER2_YPOS)
        self.walls.add(self.tronPlayer1.pos)
        self.walls.add(self.tronPlayer2.pos)
        self.tronPlayer2.alive=True
        self.tronPlayer1.alive=True
        self.tronPlayer2.angle=0
        self.tronPlayer1.angle=0
        self.clockTick = 0
        self.clear()

    def moveTron(self, player):
        if player is "One":
            self.tronPlayer1.update(self.walls)
        else:
            self.tronPlayer2.update(self.walls)

    def isGameOver(self):
        return not (self.tronPlayer1.alive and self.tronPlayer2.alive)

    def checkCollision(self):
        if self.tronPlayer2.pos in self.tronPlayer1.body:
            self.tronPlayer2.alive = False
        if self.tronPlayer1.pos in self.tronPlayer2.body:
            self.tronPlayer1.alive = False

    def clear(self):
        self.visitedCoOrds.clear()
        self.regions = 1
        self.pathToOtherHead.clear()
        self.p1SpaceLeft = 0
        self.p2SpaceLeft = 0
        self.walls.clear()


    def setGameState(self,tronPlayer1,tronPlayer2):
        self.tronPlayer1 = tronPlayer1
        self.tronPlayer2 = tronPlayer2

    def minimaxEvaluate(self,gameState, player):
        if gameState.tronPlayer1.isWallNextPos(gameState.walls) \
                or gameState.tronPlayer2.isWallNextPos(gameState.walls):
            if self.checkNumberOfRegionsAstar() == 2:
                gameState.player1SpaceCount()
                gameState.player2SpaceCount()
                if player is "One":
                    return 2 if self.p1SpaceLeft > self.p2SpaceLeft else -1
                else:
                    return -1 if self.p1SpaceLeft > self.p2SpaceLeft else 2
        return 1

    '''
    def checkNumberOfRegionsAstar(self):
        #check if player1 is reachable from player2
        # tron1 can reach tron2
        position1 = self.tronPlayer1.pos
        position2 = self.tronPlayer2.pos
        walls = self.tronPlayer1.body + self.tronPlayer2.body

        stackDFS = []
        regions = 1 #both trons are in same region
        stackDFS.append(position1)

        #exit condition empty stack or reached tron2 head
        #can be used to reach tron head too

        if walls is None:
            self.regions = 1
            return 1

        if self.regions == 2:
            return 2

        rootNode = NodeTree()
        rootNode.setParent(None)
        rootNode.setNode(position1)
        visitedCords = []
        while len(stackDFS) != 0:

            pos = stackDFS.pop(0)

            nextNode = NodeTree()
            nextNode.setNode(pos)
            nextNode.setParent(rootNode)

            if pos in visitedCords:
                continue
            else:
                visitedCords.append(pos)

            if pos == position2:
                self.regions = 1
                while nextNode.parent != None:
                    self.pathToOtherHead.append(nextNode.getNode())
                    nextNode = nextNode.parent
                return 1

            x,y = pos
            xinc = x+16
            xdec = x-16
            yinc = y+16
            ydec = y-16

            if xinc >= self.MAX_WIDTH:
                xinc = x
            if xdec < 0:
                xdec = x
            if yinc >= self.MAX_HEIGHT:
                yinc = y
            if ydec < 0:
                ydec = y

            if (xinc, y) not in walls:
                self.setAdd(stackDFS, (xinc, y))

            if (xdec, y) not in walls:
                self.setAdd(stackDFS, (xdec, y))

            if (x, yinc) not in walls:
                self.setAdd(stackDFS, (x, yinc))

            if (x, ydec) not in walls:
                self.setAdd(stackDFS, (x, ydec))

        regions = 2
        self.regions = 2

        self.visitedCoOrds = visitedCords
        return regions
    '''

    def checkNumberOfRegionsAstar(self):
        from util import PriorityQueue
        from util import PriorityQueueWithFunction
        nodeTrack = NodeTree()
        nodeList = []
        pQueueObj = PriorityQueue()
        walls = self.tronPlayer1.body + self.tronPlayer2.body
        # pQueueFuncObj = PriorityQueueWithFunction(heuristic)

        visitedNode = []
        finalState = None

        nodeTrack.setNode(self.tronPlayer1.pos)
        nodeTrack.setParent(None)
        nodeTrack.setCost(0)
        pQueueObj.push(nodeTrack, nodeTrack.getHeuristicCost())

        while (not (pQueueObj.isEmpty())):
            node = pQueueObj.pop()
            pos = node.getNode()

            if (pos in visitedNode):
                continue
            else:
                visitedNode.append(pos)

            if (pos == self.tronPlayer2.pos):
                return 1
            else:
                x, y = pos
                xinc = x + 16
                xdec = x - 16
                yinc = y + 16
                ydec = y - 16

                if xinc >= self.MAX_WIDTH:
                    xinc = x
                if xdec < 0:
                    xdec = x
                if yinc >= self.MAX_HEIGHT:
                    yinc = y
                if ydec < 0:
                    ydec = y

                if (xinc, y) not in walls:
                    createNewNodeAndAddToQueue(node, (xinc,y), self.tronPlayer2.pos,pQueueObj)

                if (xdec, y) not in walls:
                    createNewNodeAndAddToQueue(node, (xdec, y), self.tronPlayer2.pos, pQueueObj)

                if (x, yinc) not in walls:
                    createNewNodeAndAddToQueue(node, (x, yinc), self.tronPlayer2.pos, pQueueObj)

                if (x, ydec) not in walls:
                    createNewNodeAndAddToQueue(node, (x, ydec), self.tronPlayer2.pos, pQueueObj)
        self.regions = 2
        return 2


    def setAdd(self,list,elem):
            if elem in list:
                return
            else:
                list.append(elem)

    def calculateSpaceLeft(self,player):
        position2 = player.pos
        walls = self.tronPlayer1.body + self.tronPlayer2.body

        stackDFS = []
        regions = 1  # both trons are in same region
        visitedCords = []
        stackDFS.append(position2)
        while len(stackDFS) != 0:
            pos = stackDFS.pop(0)

            if pos in visitedCords:
                continue
            else:
                visitedCords.append(pos)

            x, y = pos
            xinc = x + 16
            xdec = x - 16
            yinc = y + 16
            ydec = y - 16

            if xinc >= self.MAX_WIDTH:
                xinc = x
            if xdec < 0:
                xdec = x
            if yinc >= self.MAX_HEIGHT:
                yinc = y
            if ydec < 0:
                ydec = y

            if (xinc, y) not in walls:
                self.setAdd(stackDFS, (xinc, y))

            if (xdec, y) not in walls:
                self.setAdd(stackDFS, (xdec, y))

            if (x, yinc) not in walls:
                self.setAdd(stackDFS, (x, yinc))

            if (x, ydec) not in walls:
                self.setAdd(stackDFS, (x, ydec))
        return len(visitedCords)

    def player1SpaceCount(self):
        self.p1SpaceLeft = self.calculateSpaceLeft(self.tronPlayer1)
    def player2SpaceCount(self):
        self.p2SpaceLeft = self.calculateSpaceLeft(self.tronPlayer2)

    def scoreForTrappingAndHavingMoreFreeSpace(self):

        if self.regions == 2:
            return 100

        self.player1SpaceCount()
        self.player2SpaceCount()

        return 100 if self.p1SpaceLeft < self.p2SpaceLeft else 0

def generateSuccessorState(tron, direction, walls):
    tron.angle = direction
    tron.update(walls)









class NodeTree:
    def __init__(self):
        self.node = None
        self.parent = None
        self.cost = 0
        self.hCost = 0

    def setParent(self,parent):
        self.parent = parent

    def setNode(self,node):
        self.node = node

    def getParent(self):
        return self.parent

    def getNode(self):
        return self.node

    def getCost(self):
        return self.cost

    def setCost(self,cost):
        if(self.parent is not None):
            self.cost = self.parent.cost + cost
        else:
            self.cost = cost

    def setHeuristicCost(self,heuristicVal):
        if (self.parent is not None):
            self.hCost = self.cost + heuristicVal
        else:
            self.hCost = self.cost+heuristicVal

    def getHeuristicCost(self):
        return self.hCost


def manhattanDistance( xy1, xy2 ):
    "Returns the Manhattan distance between points xy1 and xy2"
    return abs( xy1[0] - xy2[0] ) + abs( xy1[1] - xy2[1] )

def createNewNodeAndAddToQueue(parent,initialPos,targetPos,pQueueObj):
    childNode = NodeTree()
    childNode.setParent(parent)
    childNode.setNode(initialPos)
    childNode.setCost(16)
    childNode.setHeuristicCost(manhattanDistance(initialPos, targetPos))
    pQueueObj.push(childNode, childNode.getHeuristicCost())

