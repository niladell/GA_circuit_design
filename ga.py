__author__ = 'Nil & Jordi'

from fitness import *
import math
from random import random, randint
from random import seed
from random import normalvariate as normal
from random import choice

import numpy as np


# target = [[0, 0, 0, 1, 0, 1, 0, 1]]
# target = [[1, 1, 0, 0, 0, 0, 0, 1]]
# target = [[0, 1, 1, 0, 0, 0, 0, 1]]
target = [[0, 1, 1, 1, 0, 0, 0, 1]]
#
# target = [[0, 1, 1, 0, 0, 1, 1, 0],
#           [0, 0, 0, 1, 0, 0, 0, 1]]
# target = [[1, 0, 0, 1, 0, 1, 0, 1],
#           [1, 0, 1, 1, 1, 0, 1, 1],
#           [0, 1, 0, 0, 1, 1, 0, 1]]

circuit_number = 'B'

# Number optimization parameters
gates = 10

# Limits of opt. parameters values
min_val = 2  # (2): inputs a,b,c -> [0,1,2] are the first options
max_val = min_val + gates

# Population
pop = 1000

# Mutation rate (for each nucleotide -> i.e. input of any gate)
mutation = 0.01927317  # 0.002

# Swapping position with other random position
swap_prob = 0.00764858  # 0.0007

# Insert or delete ratio
insert = 0.00180419  # 0.001
delete = 0.03341547  # 0.0009

# (Randomized) ratio of [ random added circuits / all new circuits ]  during crossover
newbies_ratio = 0.3

# Probability of reproducing with crossover
crossover_prob = 0.6

# fraction of surviving population
selection = 0.4


# Iteration values (max iteration and tolerance)
max_it = 50
# tol = 10 ** -8

# Number of survivors
survive = math.ceil(pop * selection)
'''
###################################
# END OF PARAMETRISE
###################################
'''


X_raw = []

for j in range(pop):
    X_raw.append(np.array([k for i in range(abs(round(normal(gates, 5)))) for k in
                           [randint(0, i + min_val), randint(0, i + min_val)]]))

# Initiate fitness

loop = 0

# --fitness maxima
max_fit = []
max_cost = []
solution_reach = -1

'''
#####################
GENETIC ALGORITHM LOOP

#####################'''

while loop < max_it:
    seed()  # Start the pseudo-random generator --Necessari? Dins o fora del loop?]
    fit = np.zeros(len(X_raw))
    X = []
    actual_cost = []

    # Evaluate circuit
    for i in range(pop):
        if len(X_raw[i]) > 85:
            fit[i] = 0
        else:
            fit[i] = fitness(X_raw[i], target) ** 2

    max_fit.append(max(fit))

    # Cost of the circuit evaluation
    if int(max(fit)) == 1:
        if solution_reach == -1:
            solution_reach = loop
        for i in range(len(fit)):
            a = X_raw[i]
            X_raw[i] = finals(a[:], len(target))

            if fit[i] < 0.95:
                fit[i] = 0.001
            else:
                fit[i] = cost((X_raw[i]))
        max_cost.append(max(fit))

    # Ensure the best circuit not to be lost
    X.append(X_raw[fit.argmax()])
    fit = fit.cumsum() / sum(fit)

    # Sort circuit using probabilistic roulette
    for i in range(1, len(X_raw)):
        a = random()
        for j in range(len(X_raw)):
            if a < fit[j]:
                X.append(X_raw[j])
                break

    """
    ###################
    CROSSOVER

    ###################
    """

    # Number of randomly new added circuits
    newbies = randint(0, math.floor((pop - survive) * newbies_ratio))

    # One-Point Crossover
    for i in range(0, pop - survive - newbies, 2):
        # If no newbies and chromosome is odd kill last iteration
        if i >= pop - survive - 2:
            break
            # Partners choosing
        father = randint(0, survive - 1)
        mother = randint(0, survive - 1)

        if random() < crossover_prob:
            # We firstly used two cutting points, one for the mother and another for the father, but it did not
            # converge so we replaced it by a just a one point Crossover:
            cut1 = randint(0, math.ceil(len(X[father]) / 2) * 2)
            cut2 = cut1
            X[survive + i] = np.concatenate((X[father][:cut1], X[mother][cut2:]))
            X[survive + i + 1] = np.concatenate((X[mother][:cut2], X[father][cut1:]))
        else:
            # print(survive + i, ' -- ', father, ' ', mother)

            X[survive + i] = np.copy(X[father])
            X[survive + i + 1] = np.copy(X[mother])

    '''
    ############
    BIT MUTATIONS, INSERTIONS AND DELETIONS

    ###########
    '''
    for k in range(survive, pop - newbies):
        if not len(X[k]) > 0:
            X[k] = choice(X)
        for l in range(len(X[k])):
            # Single input mutation
            if random() < mutation:
                X[k][l] = randint(0, math.floor(l / 2) + 2)
            # Swapping two inputs
            if random() < swap_prob:
                loc = randint(0, len(X[k]) - 1)
                X[k][l], X[k][loc] = X[k][loc], X[k][l]
            # Inserting gates
            if random() < insert:
                np.insert(X[k], l, (randint(0, l), randint(0, l)))
            # Deleting gates
            if random() < delete:
                np.delete(X[k], l)
                if l + 1 < len(X[k]):
                    np.delete(X[k], l + 1)
            if X[k][l] > (l / 2 + 2):
                X[k][l] = randint(0, math.floor(l / 2) + 2)

    '''
    ############
    NEWBIES (COMPLETE RANDOM CIRCUITS ADDED)

    ###########
    '''

    # Add newbies at the end
    for i in range(newbies):
        X[pop - newbies + i] = np.array([k for i in range(len(choice(X))) for k in
                                         [randint(0, i + min_val), randint(0, i + min_val)]])

    X_raw = [i for i in X]

    loop += 1

    print(loop, X[0], fitness(X[0], target), cost(X[0]), len(X[0]))


a = fitness(X[0], target)  # Argmax needed
mx = 0
for i in range(1, len(X)):
    if len(X[i]) > 0 and fitness(X[i], target) > 0.95:
        b = fitness(X[i], target)
        if b > a:
            a = b
            mx = i

print(X[mx], '  - fit: ', a)

from output import *

# print('\n', output(X[mx]))
print('\nMax reach: ', max_fit)
import matplotlib.pyplot as pl

pl.figure(1)
if solution_reach > 0:
    pl.plot(np.arange(0,solution_reach+1), max_fit[:solution_reach+1])
    # pl.plot(np.arange(0, solution_reach), max_cost[:solution_reach],'-g')
    pl.plot(np.arange(0,solution_reach+1), [0 if not i == solution_reach else max_cost[0] for i in range(solution_reach+1)],
            'g', linestyle='dashed', alpha=0.7)
    if solution_reach < max_it:
        print(solution_reach, max_it, len(max_cost))
        pl.plot(np.arange(solution_reach, max_it), max_cost,'g')
        pl.plot(np.arange(solution_reach-1, max_it), max_fit[solution_reach-1:], color='blue', linestyle='dashed', alpha=0.7)
pl.axis([0,max_it,0, 1.3])
pl.xlabel('Generation')
pl.ylabel('Fitness value')
pl.title('Fitness over generations - crss: ' + str(crossover_prob))
# pl.legend('Circuit Fitness', 'Circuit Cost')
# pl.savefig('fitness_' + circuit_number)
import networkx as nx

C = nx.DiGraph()

for i in range(0, len(X[mx])):
    node = math.ceil(2.1 + i / 2)
    C.add_edge(int(X[mx][i]), node)
print()
print(C.nodes(), C.edges())

# pl.figure(2)

# pos = nx.circular_layout(C)
# nx.draw_networkx_labels(C, pos)
# nx.draw_circular(C)
# pl.title('Circuit ' + circuit_number)
# pl.savefig('circuit_' + circuit_number)

import pygraphviz as pgh
# nx.draw_graphviz(C)
'''

pl.show()


C_grph = nx.to_agraph(C)
pgh.
C_grph.layout(prog='dot')
C_grph.write('Try.png')
C_grph.draw('Try.png')'''