import copy
import GameState
import random


def randomAgent(gameState, player):
    tron = gameState.tronPlayer1 if player is "One" else gameState.tronPlayer2
    legalmoves = tron.getLegalMoves(gameState.walls)
    tron.angle = random.choice(legalmoves) if bool(legalmoves) else 90

