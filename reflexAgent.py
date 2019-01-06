import copy
import GameState
import random
def reflexAgent(gameState, player, defAction):

    tron = gameState.tronPlayer1 if player is "One" else gameState.tronPlayer2

    if tron.isWallNextPos(gameState.walls):
        if defAction is "RANDOM":
            #print("BEFORE", tron.angle)
            #print("ALL", tron.getLegalMoves(gameState.walls))
            legalmoves = tron.getLegalMoves(gameState.walls)
            newAngle = random.choice(legalmoves) if bool(legalmoves) else 90

            #print("After", newAngle)
        else:
            delta = 90 if defAction is "LEFT" else -90
            #print(gameState.walls)
            newAngle = (delta + tron.angle) % 360
        #print ("Next Pos wall")
        tron.angle = newAngle

