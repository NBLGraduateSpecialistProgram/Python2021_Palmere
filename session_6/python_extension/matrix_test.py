#!/usr/bin/env python3

'''
Introduction to C++ in Python script to test if our Matrix class works
Note - You must have ran ./setup.py build and ./setup.py install for this to work

Robert Palmere, 2021
'''


from matrix import Matrix # <-- We made this in C++ :)

myMatrix = Matrix()


while True:
    myMatrix.random_binary()
    myMatrix.display()

