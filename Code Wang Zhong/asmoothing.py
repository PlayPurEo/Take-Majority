#!/usr/bin/env python3
'''
    Author:Zhong Wang
    Email: zhong.wang@postgrad.manchester.ac.uk
    Time:  23/06/2018 16:31
    File:  asmoothing
    Encoding:UTF-8
'''

import numpy as np
import Smooth_tool
import time

data = Smooth_tool.readpgm('xconstant2/y150extend4.pgm')
map = np.reshape(data[0],data[1])
start = time.clock()

new_map = Smooth_tool.take_majority(map,5)

end = time.clock()

print(end-start)
[m,n] = new_map.shape

savefile = open('xconstant2/y150by5.pgm','w')
savefile.write('P2\n' + str(n) +' ' + str(m) +'\n' + str(data[2]) + '\n')
for i in range(0,m):
    for j in range(0,n):
        savefile.write(str(int(new_map[i][j]))+'\n')
savefile.close()