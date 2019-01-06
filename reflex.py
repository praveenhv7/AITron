import copy
import GameState

def reflexAgent(gameState):

    tron1 = gameState.tronPlayer1
    tron2 = gameState.tronPlayer2

    tronSameMove = copy.deepcopy(tron1)
    tronSameMove.update()

    tronNintyMove = copy.deepcopy(tron1)

    checkIfPosInBody(tronSameMove,tron2)
    if tronSameMove.alive == True:
        tron1.angle = tronSameMove.angle
        return

    else:
        print('Will Die')
        newAngle = (tronNintyMove.angle+90)%360
        print(newAngle)
        tronNintyMove.angle = newAngle
        tronNintyMove.update()
        checkIfPosInBody(tronNintyMove,tron2)
        if tronNintyMove.alive == True:
            tron1.angle = newAngle
            #tron1.update
            return

def checkIfPosInBody(tronNewMove,tron2):
    # checking if update will crash the tron

    if tronNewMove.pos in tron2.body:
        tronNewMove.alive = False
    '''
    for b in tron2.body:
        if tronNewMove.pos == b:
            tronNewMove.alive = False
    '''

