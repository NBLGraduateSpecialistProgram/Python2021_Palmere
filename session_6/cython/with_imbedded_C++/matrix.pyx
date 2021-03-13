# distutils: language=c++

import cython
from libc.stdlib cimport rand

# 'cdef' requires for declaration of C variables either local or module level
# Cython does not support variable length arrays so **m won't work here (https://cython.readthedocs.io/en/latest/src/userguide/language_basics.html)

cdef class Matrix:

    cdef public int size # Set these public class attributes in our __cinit__() (acts as the constructor)
    cdef public int m[5][5]

    def __cinit__(self): # All are 'def' because 'cdef' are hidden and cannot be imported 
        self.size = 5
        for i in range(self.size):
            for j in range(self.size):
                self.m[i][j] = 0

    def display(self):
        for i in range(self.size):
            print('')
            for j in range(self.size):
                print(self.m[i][j], end=' ') # <-- print() can be made into iostream by specifying 'cdef extern from "<iostream>"' 

    def random_binary(self):
        for i in range(self.size):
            for j in range(self.size):
                self.m[i][j] = rand() % 2

