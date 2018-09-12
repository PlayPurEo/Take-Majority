#!/usr/bin/env python3
'''
    Author:Zhong Wang
    Email: zhong.wang@postgrad.manchester.ac.uk
    Time:  10/03/2018 16:26
    File:  Smooth_tool
    Encoding:UTF-8
'''
import numpy as np
import time

def readpgm(name):
    with open(name) as f:
         lines = f.readlines()

    # Ignores commented lines
    for l in list(lines):
        if l[0] == '#':
            lines.remove(l)

    # Makes sure it is ASCII format (P2)
    assert lines[0].strip() == 'P2'

    # Converts data to a list of integers
    data = []
    for line in lines[1:]:
        data.extend([int(c) for c in line.split()])
    f.close()
    return (np.array(data[3:]),(data[1],data[0]),data[2])


def pgm_extend(image,t):
    [m,n] = image.shape
    new_map = np.zeros((m*t,n*t))
    for i in range(0,m):
        for j in range(0,n):
            for p in range(i*t,i*t+t):
                for q in range(j*t,j*t+t):
                    new_map[p][q] = image[i][j]

    return new_map

def take_majority(image,n):  #n is the size of take-majority filter
    [row, column] = image.shape #get row and column
    map_zero = np.zeros((row,column)) #matrix which stores data after smoothing
    add_row = add_column = int((n-1)/2) #solve the border problem
    newimage = np.zeros((row+add_row*2, column+add_column*2)) #matrix which is used to smooth data of the original image

    for i in range(add_row,row+add_row):
        for j in range(add_column,column+add_column):
            newimage[i][j] = image[i-add_row][j-add_column] #read original data from original matrix


    for i in range(add_row,row+add_row):
        for j in range(add_column,column+add_column):
            list = [0] * 101 #count times of each pixel occurs in the filter
            number = 0
            temp = 0
            for p in range(-add_row,add_row+1):
                for q in range(-add_column,add_column+1):
                    list[int(newimage[i+p][j+q])] += 1

            for k in range(0,101):
                if list[k] > number:
                    number = list[k]
                    temp = k #get the value that occurs most frequently

            map_zero[i - add_row][j - add_column] = int(temp)
    return map_zero

def insertMissedPixel1(map,new_map):
    # map is the matrix before smoothing, new_map is the matrix after smoothing, they must have same size
    [m,n] = new_map.shape
    for i in range(0,m):
        originalList = sorted(set(map[i]), key=list(map[i]).index)
        afterList = sorted(set(new_map[i]), key=list(new_map[i]).index)
        listBeside = []
        if len(originalList)>len(afterList):    #finding missed pixels
            listDiffer = sorted(set(originalList).difference(set(afterList)), key=originalList.index)
            listBesideSame = []
            for k in listDiffer:
                frontPixel = 999
                behindPixel = 999
                pixelIndex1 = 0
                pixelIndex2 = 0
                for h in range(1,n-1):
                    if map[i][h] == k and map[i][h-1] != k:
                        frontPixel = map[i][h-1]
                        pixelIndex1 = h
                    if map[i][h] == k and map[i][h+1] != k:
                        behindPixel = map[i][h+1]
                        pixelIndex2 = h
                        if frontPixel != behindPixel:
                            listBeside.append(frontPixel)
                            listBeside.append(behindPixel)
                        if frontPixel!=999 and behindPixel!=999 and frontPixel == behindPixel:
                            listBesideSame.append((pixelIndex1+pixelIndex2)/2)
                        break
            for j in range(0,n-1):
                if listBesideSame!=[] and j == listBesideSame[0]:
                    new_map[i][j] = map[i][j]
                    listDiffer.remove(listDiffer[0])
                    listBesideSame.remove(listBesideSame[0])
                if listBeside!=[] and listDiffer!=[] and new_map[i][j] == listBeside[0] and new_map[i][j+1]==listBeside[1]:
                    new_map[i][j+1] = listDiffer[0]
                    listBeside.remove(listBeside[0])
                    listBeside.remove(listBeside[0])
                    listDiffer.remove(listDiffer[0])

        originalList = sorted(set(map[i]), key=list(map[i]).index)
        afterList = sorted(set(new_map[i]), key=list(new_map[i]).index)
        listFront = []
        if len(originalList)>len(afterList):    #要找出缺失的像素值
            listDiffer = sorted(set(originalList).difference(set(afterList)), key=originalList.index)
            for k in listDiffer:
                for h in range(0,len(originalList)):
                    if originalList[h] == k:
                        listFront.append(originalList[h-1])
            for j in range(0,n-1):
                if listFront!=[] and listDiffer!=[] and new_map[i][j] == listFront[0] and new_map[i][j+1]!=listFront[0]:
                    new_map[i][j+1] = listDiffer[0]
                    listFront.remove(listFront[0])
                    listDiffer.remove(listDiffer[0])
    return new_map

def insertMissedPixel2(map,new_map):
    map = np.transpose(map)
    new_map = np.transpose(new_map)
    [m,n] = new_map.shape

    for i in range(0,m):
        originalList = sorted(set(map[i]), key=list(map[i]).index)
        afterList = sorted(set(new_map[i]), key=list(new_map[i]).index)
        listBeside = []
        if len(originalList)>len(afterList):
            listDiffer = sorted(set(originalList).difference(set(afterList)), key=originalList.index)
            listBesideSame = []
            for k in listDiffer:
                frontPixel = 999
                behindPixel = 999
                pixelIndex1 = 0
                pixelIndex2 = 0
                for h in range(1,n-1):
                    if map[i][h] == k and map[i][h-1] != k:
                        frontPixel = map[i][h-1]
                        pixelIndex1 = h
                    if map[i][h] == k and map[i][h+1] != k:
                        behindPixel = map[i][h+1]
                        pixelIndex2 = h
                        if frontPixel != behindPixel:
                            listBeside.append(frontPixel)
                            listBeside.append(behindPixel)
                        if frontPixel!=999 and behindPixel!=999 and frontPixel == behindPixel:
                            listBesideSame.append((pixelIndex1+pixelIndex2)/2)
                        break
            for j in range(0,n-1):
                if listBesideSame!=[] and j == listBesideSame[0]:
                    new_map[i][j] = map[i][j]
                    listDiffer.remove(listDiffer[0])
                    listBesideSame.remove(listBesideSame[0])
                if listBeside!=[] and listDiffer!=[] and new_map[i][j] == listBeside[0] and new_map[i][j+1]==listBeside[1]:
                    new_map[i][j+1] = listDiffer[0]
                    listBeside.remove(listBeside[0])
                    listBeside.remove(listBeside[0])
                    listDiffer.remove(listDiffer[0])

        originalList = sorted(set(map[i]), key=list(map[i]).index)
        afterList = sorted(set(new_map[i]), key=list(new_map[i]).index)
        listFront = []
        if len(originalList)>len(afterList):
            listDiffer = sorted(set(originalList).difference(set(afterList)), key=originalList.index)
            for k in listDiffer:
                for h in range(0,len(originalList)):
                    if originalList[h] == k:
                        listFront.append(originalList[h-1])
            for j in range(0,n-1):
                if listFront!=[] and listDiffer!=[] and new_map[i][j] == listFront[0] and new_map[i][j+1]!=listFront[0]:
                    new_map[i][j+1] = listDiffer[0]
                    listFront.remove(listFront[0])
                    listDiffer.remove(listDiffer[0])

    new_map = np.transpose(new_map)
    return new_map

def smoothness(image,new_image): #image is the matrix before smoothing, new_image is the matrix after smoothing, they must have same size
    [m, n] = new_image.shape
    a = 0
    for i in range(0, m):
        for j in range(0,n):
            if image[i][j] != new_image[i][j]:
                a = a + 1

    smoothness = a/(m*n)
    print("The number of changed pixels are" + str(a))
    print("Smoothness is "+ str(smoothness))

def threedtrans():
    threedlist = []
    max = -1
    head0 = 'origin/'
    head = 'v1_00'
    tail = '.pgm'
    for i in range(14, 300):
        if i < 100:
            path = head0 + head + '0' + str(i) + tail
            data = readpgm(path)
            if max < data[2]:
                max = data[2]
            map = np.reshape(data[0], data[1])
            threedlist.append(map)
        else:
            path = head0 + head + str(i) + tail
            data = readpgm(path)
            if max < data[2]:
                max = data[2]
            map = np.reshape(data[0], data[1])
            threedlist.append(map)

    threedarray = np.array(threedlist)  # 3D array
    print(threedarray.shape)

    xconstant = np.transpose(threedarray, (2, 0, 1))
    print(xconstant.shape)

    [k, m, n] = xconstant.shape

    for i in range(0, k):
        outpath = 'yconstant/yconstant' + str(i) + '.pgm'
        savefile = open(outpath, 'w')
        savefile.write('P2\n' + str(n) + ' ' + str(m) + '\n' + str(max) + '\n')
        for r in range(0, m):
            for c in range(0, n):
                savefile.write(str(int(xconstant[i][r][c])) + '\n')
        savefile.close()


if __name__ == '__main__':
    path = input("Please input the path of the image: ")
    data = readpgm(path)
    matrix = np.reshape(data[0],data[1])
    matrixB = matrix.copy()
    [mo,no] = matrix.shape
    times = input("Please input the times(t) you want to increase, new size will be (m+t)*(n+t): ")
    times = int(times)
    matrixB = pgm_extend(matrix, times)
    print("Increasing the size is finished!")
    print("original size is " + str(mo) + ' x ' + str(no))
    [m,n] = matrixB.shape
    print("up-scaled size is " + str(m) + ' x ' + str(n))

    filtersize = input("Please input the size of the filter to do smoothing (must be odd number): ")
    filtersize = int(filtersize)
    print("waiting for smoothing.....")
    start = time.clock()
    matrixC = take_majority(matrixB,filtersize)
    end = time.clock()
    print("done!!  time cost is " + str(end-start) + ' second')
    path = input("Please input the name of new image (path could be input together): ")
    savefile = open(path,'w')
    savefile.write('P2\n' + str(n) + ' ' + str(m) + '\n' + str(data[2]) + '\n')
    for i in range(0, m):
        for j in range(0, n):
            savefile.write(str(int(matrixC[i][j])) + '\n')
    savefile.close()
    print("Congratulations! new image is produced!")

    missedLine = 0
    for i in range(0, m):
        originalLen = sorted(set(matrixB[i]))
        afterLen = sorted(set(matrixC[i]))
        if len(originalLen) > len(afterLen):
            missedLine = missedLine + 1

    if missedLine == 0:
        print("Congratulations! There is no missed pixels.")
    else:
        print("Number of lines that missed values after smoothing is " + str(
            missedLine) + ", please insert missed pixels.")

    newMatrix = insertMissedPixel1(matrixB, matrixC)
    missedLineInsert = 0
    for i in range(0, m):
        originalLen = set(matrixB[i])
        afterLen = set(newMatrix[i])
        if len(originalLen) > len(afterLen):
            missedLineInsert = missedLineInsert + 1

    print("Insertion on X-constant direction is finished")

    newMatrix_tran = np.transpose(newMatrix)
    Matrix_tran = np.transpose(matrixB)
    [m2, n2] = newMatrix_tran.shape  # m2 == n, n2 == m
    missedLine = 0
    for i in range(0, m2):
        originalLen = sorted(set(Matrix_tran[i]), key=list(Matrix_tran[i]).index)
        afterLen = sorted(set(newMatrix_tran[i]), key=list(newMatrix_tran[i]).index)
        if len(originalLen) > len(afterLen):
            missedLine = missedLine + 1
    print("Number of lines that missed values after smoothing is " + str(missedLine) + ", please insert missed pixels.")

    newMatrix = insertMissedPixel2(matrixB, newMatrix)

    newMatrix_tran = np.transpose(newMatrix)
    missedLineInsertY = 0
    for i in range(0, m2):
        originalLen = sorted(set(Matrix_tran[i]), key=list(Matrix_tran[i]).index)
        afterLen = sorted(set(newMatrix_tran[i]), key=list(newMatrix_tran[i]).index)
        if len(originalLen) > len(afterLen):
            missedLineInsertY = missedLineInsertY + 1
    print("Insertion on Y-constant direction is finished")

    savefile = open('AfterInsertion.pgm', 'w')
    savefile.write('P2\n' + str(n) + ' ' + str(m) + '\n' + str(data[2]) + '\n')
    for i in range(0, m):
        for j in range(0, n):
            savefile.write(str(int(newMatrix[i][j])) + '\n')
    savefile.close()
    print("Congratulations! The image after inserting missed tissues is produced!")