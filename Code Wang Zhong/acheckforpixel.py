#!/usr/bin/env python3
'''
    Author:Zhong Wang
    Email: zhong.wang@postgrad.manchester.ac.uk
    Time:  23/06/2018 17:39
    File:  acheckforpixel
    Encoding:UTF-8
'''
import numpy as np
import Smooth_tool



data = Smooth_tool.readpgm('b/v1_00188extend5.pgm')
map = np.reshape(data[0],data[1])

data2 = Smooth_tool.readpgm('b/v1_00188by101.pgm')
new_map = np.reshape(data2[0],data2[1])

[m,n] = new_map.shape
missedLine = 0
for i in range(0,m):
    originalLen = sorted(set(map[i]), key=list(map[i]).index)
    afterLen = sorted(set(new_map[i]), key=list(new_map[i]).index)
    if len(originalLen) > len(afterLen):
        missedLine = missedLine+1

if missedLine == 0:
    print("Congratulations! There is no missed pixels.")
else:
    print("Number of lines that missed values after smoothing is " + str(missedLine) + ", please insert missed pixels.")

new_map = Smooth_tool.insertMissedPixel1(map,new_map)
missedLineInsert = 0
for i in range(0,m):
    originalLen = set(map[i])
    afterLen = set(new_map[i])
    if len(originalLen) > len(afterLen):
        print(i)
        print(originalLen)
        print(afterLen)
        missedLineInsert = missedLineInsert+1

print("Insertion on X-constant direction is finished")




new_map_tran = np.transpose(new_map)
map_tran = np.transpose(map)
[m2,n2] = new_map_tran.shape  # m2 == n, n2 == m
missedLine = 0
for i in range(0,m2):
    originalLen = sorted(set(map_tran[i]), key=list(map_tran[i]).index)
    afterLen = sorted(set(new_map_tran[i]), key=list(new_map_tran[i]).index)
    if len(originalLen) > len(afterLen):
        missedLine = missedLine+1
print("Number of lines that missed values after smoothing is " + str(missedLine) + ", please insert missed pixels.")

new_map = Smooth_tool.insertMissedPixel2(map,new_map)

new_map_tran = np.transpose(new_map)
missedLineInsertY = 0
for i in range(0,m2):
    originalLen = sorted(set(map_tran[i]), key=list(map_tran[i]).index)
    afterLen = sorted(set(new_map_tran[i]), key=list(new_map_tran[i]).index)
    if len(originalLen) > len(afterLen):
        print(i)
        print(originalLen)
        print(afterLen)
        missedLineInsertY = missedLineInsertY+1
print("Insertion on Y-constant direction is finished")





savefile = open('b/v1_00188by101insertY.pgm','w')
savefile.write('P2\n' + str(n) +' ' + str(m) +'\n' + str(data[2]) + '\n')
for i in range(0,m):
    for j in range(0,n):
        savefile.write(str(int(new_map[i][j]))+'\n')
savefile.close()