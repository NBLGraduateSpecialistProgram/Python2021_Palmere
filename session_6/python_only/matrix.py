#!/usr/bin/env python3

import numpy as np
import time

class Matrix(object):

    def __init__(self):
        self.mat = np.zeros(25).reshape(5,5)
        print(self.mat)

    def display(self):
        for i in self.mat:
            print('')
            for j in i:
                print(j, end=' ')

    def random_binary(self):
        self.mat = np.random.randint(2, size=(5,5))


if __name__ == '__main__':
    
    count = 0
    times = []
    m = Matrix()
    while True:
        count += 1
        start = time.time()
        m.random_binary()
        m.display()
        stop = time.time()
        t = stop - start
        times.append(str(t))
        if count == 1000:
            break

    with open('timed.txt', 'w') as fp:
        for t in times:
            fp.write(t+'\n')

