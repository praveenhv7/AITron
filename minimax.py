import copy
import GameState
from reflexAgent import reflexAgent
from GameState import generateSuccessorState

def minimaxAgent(gameState, depth, player):
    if gameState.regions == 2:
        reflexAgent(gameState,player,"LEFT")
        return
    tron = gameState.getPlayer(player)
    legalActions = tron.getLegalMoves(gameState.walls)
    if len(legalActions) is 0:
        tron.angle = 90
    else:
        scores = maxValue(gameState, depth, player)
        tron.angle = legalActions[scores.index(max(scores))]
    return


def isTerminalState(gameState, depth):
    tron1Moves = gameState.tronPlayer1.getLegalMoves(gameState.walls)
    tron2Moves = gameState.tronPlayer2.getLegalMoves(gameState.walls)
    return depth == 0 or gameState.isGameOver() or len(tron1Moves) == 0 or len(tron2Moves) ==0

def minValue(gameState, depth, player):
    """If Terminal state then return score"""
    if isTerminalState(gameState,depth):
        return gameState.minimaxEvaluate(gameState,player)

    tron = gameState.getMinPlayer(player)
    scores = []
    legalActions = tron.getLegalMoves(gameState.walls)
    '''For each legal action for current ghost calculate next game state and pass it to maximiser/minimiser'''
    for action in legalActions:
        newGameState = copy.deepcopy(gameState)
        minTron = newGameState.getMinPlayer(player)
        generateSuccessorState(minTron, action, newGameState.walls)
        result = max(maxValue(newGameState, depth - 1, player))
        scores.append(result)
    return min(scores)

def maxValue(gameState, depth, player):
    """If Terminal state then return score"""
    if isTerminalState(gameState, depth):
        return [gameState.minimaxEvaluate(gameState,player)]

    tron = gameState.getPlayer(player)
    scores = []
    '''For each legal action for Tron calculate next game state and pass it to minimiser'''
    legalMoves = tron.getLegalMoves(gameState.walls)

    for action in legalMoves:
        newGameState = copy.deepcopy(gameState)
        maxTron = newGameState.tronPlayer1 if player is "One" else newGameState.tronPlayer2
        generateSuccessorState(maxTron, action, newGameState.walls)
        scores.append(minValue(newGameState, depth, player))
    return scores
