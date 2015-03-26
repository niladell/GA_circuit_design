__author__ = 'Nil'


def output(n, out_gate):
    x = [[0, 0, 0],
         [0, 0, 1],
         [0, 1, 0],
         [0, 1, 1],
         [1, 0, 0],
         [1, 0, 1],
         [1, 1, 0],
         [1, 1, 1]]

    for j in range(0, len(n) - 1, 2):
        for k in range(len(x)):
            x[k].append(int (not (x[k][int(n[j])] or x[k][int(n[j + 1])])))
            # print(j)
    o = []

    for k in range(len(x)):
        # print(x[k])
        o.append(x[k][out_gate])
    return o

# n = [0, 1, 2, 2, 3, 4]
# n = [0,0,3,1,3,2,1,1,2,2,0,6,8,7,1,2,4,5,11,9,12,10]
# n = [2, 0, 3, 0, 4, 1, 2, 3, 5, 6]
# print(output(n))
'''
n = [0, 1, 2, 3, 3, 0, 2, 4, 1, 0, 3, 1, 2, 1]
print(output(n))

n = [0, 1, 3, 2, 0, 2]
print(output(n))'''

'''14
[0, 1, 2, 3, 3, 0, 2, 4, 1, 0, 3, 1, 2, 1]
[0, 1, 2, 3, 3, 0, 2, 4, 1, 0, 3, 1, 2, 1]
{0, 1, 2, 3, 4}
5
6
7
8
[0, 1, 3, 2, 0, 2]
'''

# Maravellos sumador
# n =  [1,  1,  2,  1,  1,  2,  4,  2,  6,  3,  6,  3,  7,  4]

# print(output(n, 9), '\n', output(n, 8))