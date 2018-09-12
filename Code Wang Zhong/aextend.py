#!/usr/bin/env python3
'''
    Author:Zhong Wang
    Email: zhong.wang@postgrad.manchester.ac.uk
    Time:  23/06/2018 22:32
    File:  aextend
    Encoding:UTF-8
'''

import numpy as np
import Smooth_tool

data = Smooth_tool.readpgm('yconstant/yconstant150.pgm')
map = np.reshape(data[0],data[1])
new_map = Smooth_tool.pgm_extend(map,4)
[m,n] = new_map.shape

savefile = open('xconstant2/y150extend4.pgm','w')
savefile.write('P2\n' + str(n) +' ' + str(m) +'\n' + str(data[2]) + '\n')
for i in range(0,m):
    for j in range(0,n):
        savefile.write(str(int(new_map[i][j]))+'\n')
savefile.close()