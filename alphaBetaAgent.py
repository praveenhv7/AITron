import copy
import GameState
from reflexAgent import reflexAgent
from GameState import generateSuccessorState
import sys

def alphaBetaAgent(gameState, depth, player):
    if gameState.regions == 2:
        reflexAgent(gameState, player, "LEFT")
        return
    tron = gameState.getPlayer(player)
    legalActions = tron.getLegalMoves(gameState.walls)
    if len(legalActions) is 0:
        tron.angle = 90
    else:
        scores = maxValue(gameState, depth, player, -sys.maxsize -1, sys.maxsize)
        tron.angle = legalActions[scores.index(max(scores))]
    return


def isTerminalState(gameState, depth):
    tron1Moves = gameState.tronPlayer1.getLegalMoves(gameState.walls)
    tron2Moves = gameState.tronPlayer2.getLegalMoves(gameState.walls)
    return depth == 0 or gameState.isGameOver() or len(tron1Moves) == 0 or len(tron2Moves) ==0

def maxValue(gameState, depth,  player, alpha, beta):
    """If Terminal state then return score"""
    if isTerminalState(gameState, depth):
        return [gameState.minimaxEvaluate(gameState,player)]

    tron = gameState.getPlayer(player)
    scores = []
    '''For each legal action for Tron calculate next game state and pass it to minimiser'''
    legalMoves = tron.getLegalMoves(gameState.walls)
    '''Initialise v to very low value'''
    v = -sys.maxsize -1
    for action in legalMoves:
        newGameState = copy.deepcopy(gameState)
        maxTron = newGameState.tronPlayer1 if player is "One" else newGameState.tronPlayer2
        generateSuccessorState(maxTron, action, newGameState.walls)
        scores.append(minValue(newGameState, depth, player, alpha, beta))
        v = max(v, max(scores))
        '''if v is the max the maximiser has seen so far return v'''
        if v > beta: return scores
        ''' assign highest of v and alpha to alpha '''
        alpha = max(alpha, v)
    return scores
    
def minValue(gameState, depth, player, alpha, beta):
    """If Terminal state then return score"""
    if isTerminalState(gameState, depth ):
        return gameState.minimaxEvaluate(gameState, player)

    tron = gameState.getMinPlayer(player)
    scores = []
    legalActions = tron.getLegalMoves(gameState.walls)
    '''initialise value to high number'''
    v = sys.maxsize
    for action in legalActions:
        newGameState = copy.deepcopy(gameState)
        minTron = newGameState.getMinPlayer(player)
        generateSuccessorState(minTron, action, newGameState.walls)
        v = max(maxValue(newGameState, depth - 1, player, alpha, beta))
        scores.append(v)
        '''if v is smallest minimiser has seen so far return v'''
        if v < alpha: return v
        '''assign minimum of v and beta to beta'''
        beta = min(beta, v)
    return min(scores)


