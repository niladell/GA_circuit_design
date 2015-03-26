__author__ = 'Nil & Jordi'

import numpy as np


def fitness(n, target):
    '''
    Fitness function that evaluates how close is a given circuit "n" to the desired output.
    '''

    fit = 0
    j = 2
    for i in n:
        j += 0.5
        if j < (i + 0.1):  # + 0.1 used to avoid comparison errors
            return 0

    from output import output

    s = set(n)
    ends = []
    for i in range(3+len(n)//2):
        if i not in s:
            ends.append(i)
    if len(ends) < len(target):
        return 0
    for k in range(len(target)):
        o = output(n, ends[-k-1])
        for i in range(len(o)):
            fit += abs(target[k][i] - o[i])
    fit = 1 - 1 / (len(target) * len(target[0])) * fit
    return fit


def finals(n, ends):
    '''
    Deletes all circuits outputs that we don't want. For example, a circuit with only one exit will only have an ending
    gate, the last one, so we kill all other dead end gates.
    '''

    if not len(n) % 2 == 0:
        n = np.delete(n, len(n) - 1)

    s = set(n)
    for j in reversed(range(3, len(n) // 2 +3)):
        # We work with the reversed due to if we were doing it straight we would have to deal whit the shifting that
        # the delete will produce and an extra counter will be needed, it's a similar case with what happens in the
        # next comment
        if j not in s:
            if ends > 0:
                ends -= 1
            else:
                n = np.delete(n, 2 * (j - 3))
                # Due to de delete of the previous number all the vector shifts
                # so len(n)-> len(n)-1, and what should be j+1 becomes j
                n = np.delete(n, 2 * (j - 3))

                for k in range(2*(j-3), len(n)):
                    if n[k] > j:
                        n[k] -= 1
    return n


def cost(n):
    '''
    Simple cost function. For a given circuit "n" return the inverse of the length.
    '''
    return 2/(len(n)+10**-10)