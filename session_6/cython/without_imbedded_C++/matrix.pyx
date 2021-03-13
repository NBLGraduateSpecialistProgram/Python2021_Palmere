#!/usr/bin/env python3

import numpy as np
import time

class Matrix(object):

    def __init__(self):
        self.mat = np.zeros(25).reshape(5,5)
        print(self.mat)

    def display(self):
        for i in self.mat:
            print('\n')
            for j in i:
                print(j)

    def random_binary(self):
        self.mat = np.random.randint(2, size=(5,5))

