#import matplotlib.pyplot as plt

def deCasteljau(points, u, k = None, i = None, dim = None):
    """Return the evaluated point by a recursive deCasteljau call
    Keyword arguments aren't intended to be used, and only aid
    during recursion.

    Args:
    points -- list of list of floats, for the control point coordinates
              example: [[0.,0.], [7,4], [-5,3], [2.,0.]]
    u -- local coordinate on the curve: $u \in [0,1]$

    Keyword args:
    k -- first parameter of the bernstein polynomial
    i -- second parameter of the bernstein polynomial
    dim -- the dimension, deduced by the length of the first point
    """
    if k == None: # topmost call, k is supposed to be undefined
        # control variables are defined here, and passed down to recursions
        k = len(points)-1
        i = 0
        dim = len(points[0])

    # return the point if downmost level is reached
    if k == 0:
        return points[i]

    # standard arithmetic operators cannot do vector operations in python,
    # so we break up the formula
    a = deCasteljau(points, u, k = k-1, i = i, dim = dim)
    b = deCasteljau(points, u, k = k-1, i = i+1, dim = dim)
    result = []

    # finally, calculate the result
    for j in range(dim):
        result.append((1-u) * a[j] + u * b[j])

    return result


def bCurve (time1, value1, time2, value2, ccX, ccY, q):
    points = {}
    deltaTime = time2 - time1
    deltaValue = value2 - value1
    pointsNum = int(deltaTime / (q))
    P = [[time1, value1], [time1 + ccX * deltaTime , value1 + ccY * deltaValue], [time1 + deltaTime * ccX, value1 + ccY * deltaValue], [time2, value2]]
    x =[]
    y =[]
    for point in range(0, pointsNum):
        p = point / pointsNum
        coor = deCasteljau(P, p)
        points[point] = {'Time': float(coor[0]), 'Value': int(coor[1])}
        #print(point, points[point])
        x.append(coor[0])
        y.append(coor[1])

    # verification graphique
    #plt.plot(x, y, marker='o')
    #plt.show()

    return points

def affine (time1, value1, time2, value2, q):
    points = {}
    a = float((float(value2) - float(value1))/(float(time2)-float(time1)))
    b = value1 - a * time1
    #print('coefficient:', a)
    #print('test: a * {} = {}'.format(time1, a*time1))

    deltaTime = time2 - time1
    pointsNum = int(deltaTime / q)
    for point in range(1, pointsNum + 1):
        p = point * deltaTime / pointsNum + time1
        #print('test: a * {} = {}'.format(p, a * p))
        points[point]= {'Time' : float(p), 'Value' : int(a * p + b)}
        #print(point, points[point])

    #print('test: a * {} = {}'.format(time2, a * time2))
    #print('time:', time, 'nombre de points générés:', pointsNum,"\n")

    return points


#bCurve(0,0,4,127,0,1,0.25)

