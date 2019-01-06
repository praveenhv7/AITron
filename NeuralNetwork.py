from GameState import *
from constants import *

def get_weights_from_encoded(individual):
    W1 = individual[0:NEURALNET.W1_shape[0] * NEURALNET.W1_shape[1]]
    W2 = individual[NEURALNET.W1_shape[0] * NEURALNET.W1_shape[1]:NEURALNET.W2_shape[0] * NEURALNET.W2_shape[1] + NEURALNET.W1_shape[0] * NEURALNET.W1_shape[1]]
    W3 = individual[NEURALNET.W2_shape[0] * NEURALNET.W2_shape[1] + NEURALNET.W1_shape[0] * NEURALNET.W1_shape[1]:]

    return (
    W1.reshape(NEURALNET.W1_shape[0], NEURALNET.W1_shape[1]), W2.reshape(NEURALNET.W2_shape[0], NEURALNET.W2_shape[1]), W3.reshape(NEURALNET.W3_shape[0], NEURALNET.W3_shape[1]))


def softmax(z):
    s = np.exp(z.T) / np.sum(np.exp(z.T), axis=1).reshape(-1, 1)

    return s


def sigmoid(z):
    s = 1 / (1 + np.exp(-z))

    return s


def forward_propagation(X, individual):
    W1, W2, W3 = get_weights_from_encoded(individual)

    Z1 = np.matmul(W1, X.T)
    A1 = np.tanh(Z1)
    Z2 = np.matmul(W2, A1)
    A2 = np.tanh(Z2)
    Z3 = np.matmul(W3, A2)
    A3 = softmax(Z3)
    return A3