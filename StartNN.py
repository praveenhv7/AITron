from Tron_NN import *
from  GameState import *
from GeneticImplementation import *
from constants import *



new_population = np.random.choice(np.arange(-1, 1, step=0.01), size=GENTICSOLUTION.POP_SIZE, replace=True)
filePtr = open("GameInfo.txt", "a")
filePtr.write("Tron Analysis")

for generation in range(GENTICSOLUTION.NUM_GENERATIONS):
    fitness = cal_pop_fitness(new_population,filePtr)
    print('#######  fittest chromosome in gneneration ' + str(generation) + ' is having fitness value:  ',
    np.max(fitness))
    filePtr.write('#######  fittest chromosome in gneneration ' + str(generation) + ' is having fitness value:  '+
    str(np.max(fitness)))

    # Selecting the best parents in the population for mating.
    parents = select_mating_pool(new_population, fitness, GENTICSOLUTION.NUM_PARENTS_MATCHING)

    # Generating next generation using crossover.
    offspring_crossover = crossover(parents, offspring_size=(GENTICSOLUTION.POP_SIZE[0] - parents.shape[0], NEURALNET.NO_OF_WEIGHTS))

    # Adding some variations to the offsrping using mutation.
    offspring_mutation = mutation(offspring_crossover)

    # Creating the new population based on the parents and offspring.
    new_population[0:parents.shape[0], :] = parents
    new_population[parents.shape[0]:, :] = offspring_mutation
filePtr.close()