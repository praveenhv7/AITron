import constants
from GameState import *
from NeuralNetwork import *
from Tron_NN import *

def runTron(weights,filePtr):
    max_score = 0
    avg_score = 0
    test_games = 1
    score1 = 0
    steps_per_game = 2500
    score2 = 0

    for _ in range(test_games):
        gameState = GameState()

        count_same_direction = 0
        prev_direction = 0
        score = smartAgent(steps_per_game,gameState, weights, count_same_direction, prev_direction,filePtr)

    return score





def smartAgent(steps_per_game,gameState,weights,count_same_direction,prev_direction,filePtr):
    score = 0
    for _ in range(steps_per_game):


        tronPlayer2 = gameState.tronPlayer2
        tronPlayer1 = gameState.tronPlayer1

        dictLegalMoves = {}
        dictLegalMoves.update({Directions.NORTH:1})
        dictLegalMoves.update({Directions.SOUTH:1})
        dictLegalMoves.update({Directions.EAST:1})
        dictLegalMoves.update({Directions.WEST:1})

        moves = tronPlayer2.getLegalMoves(gameState.walls)
        for move in moves:
            dictLegalMoves[move] = 0

        is_front_blocked = 1
        if tronPlayer2.angle in moves:
            is_front_blocked = 0
        else:
            is_front_blocked = 1

        tron1Pos = [tronPlayer1.pos[0],tronPlayer1.pos[1]]
        tron2Pos = [tronPlayer2.pos[0],tronPlayer2.pos[1]]
        tron2PosPrev = [(tronPlayer2.body[0])[0],(tronPlayer2.body[0])[1]]

        tron2PosDirection = np.array(tron2Pos) - np.array(tron2PosPrev)
        tron12Direction = np.array(tron1Pos) - np.array(tron2Pos)

        norm_of_tron12Direction_vector = np.linalg.norm(tron12Direction)
        norm_of_tron2PosDirection_vector = np.linalg.norm(tron2PosDirection)

        if norm_of_tron12Direction_vector == 0:
            norm_of_tron12Direction_vector = 10
        if norm_of_tron2PosDirection_vector == 0:
            norm_of_tron2PosDirection_vector = 10

        tron12_direction_vector_normalized = tron12Direction / norm_of_tron12Direction_vector
        tron2_direction_vector_normalized = tron2PosDirection / norm_of_tron2PosDirection_vector

        #is tron2 going to collide with tron1
        tronPlayer2Temp = copy.deepcopy(gameState.tronPlayer2)
        #availableMoves = tronPlayer2Temp.getLegalMoves()



        predicted_direction = np.argmax(np.array(forward_propagation(np.array(
            [dictLegalMoves[Directions.WEST], is_front_blocked, dictLegalMoves[Directions.EAST], tron12_direction_vector_normalized[0],
             tron2_direction_vector_normalized[0], tron12_direction_vector_normalized[1],
             tron2_direction_vector_normalized[1]]).reshape(-1, 7), weights))) - 1

        #print('Predicted Direction ',predicted_direction)

        if predicted_direction == prev_direction:
            count_same_direction += 1
        else:
            count_same_direction = 0
            prev_direction = predicted_direction

        if predicted_direction == -1:
            nextDirection = (tronPlayer2.angle-90)%360
        elif predicted_direction == 1:
            nextDirection = (tronPlayer2.angle+90)%360
        else:
            nextDirection = tronPlayer2.angle

        tronPlayer2.angle = nextDirection
        score += playTron(gameState,filePtr)

        if not (gameState.tronPlayer2.alive and gameState.tronPlayer1.alive):
            return score


        if count_same_direction > 8 and predicted_direction != 0:
            score -= 1
        else:
            score += 2
    return score






