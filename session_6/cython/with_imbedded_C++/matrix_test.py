#!/usr/bin/env python3

import numpy as np
import time
from matrix import Matrix

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

