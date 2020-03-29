from const import ItK, Tsigma, data, graph4, graph3, graph2, graph1, graph1_1, graph2_1, graph3_1, graph4_1
import math
import numpy

def LinearInterpolate(a, b, x):
    return a*(1-x) + b*x 

def interpolate(table, xValue, xIndex, yIndex):
    interpolateIndexFound = False
    x1 = 0
    x2 = 0
    y1 = 0
    y2 = 0
    yResult = 0
    for i in range(len(table) - 1):
        if (table[i][xIndex] <= xValue and table[i + 1][xIndex] >= xValue):
            y1 = table[i][yIndex]
            y2 = table[i + 1][yIndex]
            x1 = table[i][xIndex]
            x2 = table[i + 1][xIndex]
            interpolateIndexFound = True
    if (interpolateIndexFound):
        yResult = y1 + ((xValue - x1) / (x2 - x1)) * (y2 - y1)
    else:
        if (xValue < table[0][xIndex]):
            yResult = table[0][yIndex]
        if (xValue > table[len(table) - 1][xIndex]):
            yResult = table[len(table) - 1][yIndex]
            
    return yResult

def getTz(T0, m, r):
    z = r / data['R']
    return (data['Tw'] - T0) * math.pow(z, m) + T0

def siqmaFunc(I, z):
    m = interpolate(ItK, I, 0, 2)
    T0 = interpolate(ItK, I, 0, 1)
    Tz = getTz(T0, m, z)
    siqma = interpolate(Tsigma, Tz, 0, 1)
    return siqma

def integrateSimpson(I):
    n = 40
    begin = 0
    end = 1
    width = (end - begin) / n
    result = 0
    for step in range(n):
        x1 = begin + step * width
        x2 = begin + (step + 1) * width
        result += (x2 - x1) / 6.0 * (siqmaFunc(I, x1) + 4.0 * siqmaFunc(I, 0.5 * (x1 + x2)) + siqmaFunc(I, x2))
    return result

def calculateRp(I):
    R = data['R']
    integral = integrateSimpson(I)
    return data['Le'] / (2 * math.pi * R * R * integral)

def functionF_4(t, I, U):
    Rp = calculateRp(I)
    graph3[0].append(t)
    graph3[1].append(Rp)
    graph4[0].append(t)
    graph4[1].append(I*Rp)
    return ((U - (data['Rk'] + Rp) * I) / data['Lk'])

def functionF_2(t, I, U):
    Rp = calculateRp(I)
    graph3_1[0].append(t)
    graph3_1[1].append(Rp)
    graph4_1[0].append(t)
    graph4_1[1].append(I*Rp)
    return ((U - (data['Rk'] + Rp) * I) / data['Lk'])

def functionPHI(t, I, U):
    return -1 / data['Ck'] * I


def RungeKutta4(xn, yn, zn, hn):
    hn2 = hn / 2

    k1 = hn * functionF_4(xn, yn, zn)
    q1 = hn * functionPHI(xn, yn, zn)

    k2 = hn * functionF_4(xn + hn2, yn + k1 / 2, zn + q1 / 2)
    q2 = hn * functionPHI(xn + hn2, yn + k1 / 2, zn + q1 / 2)

    k3 = hn * functionF_4(xn + hn2, yn + k2 / 2, zn + q2 / 2)
    q3 = hn * functionPHI(xn + hn2, yn + k2 / 2, zn + q2 / 2)

    k4 = hn * functionF_4(xn + hn, yn + k3, zn + q3)
    q4 = hn * functionPHI(xn + hn, yn + k3, zn + q3)

    yn_1 = yn + (k1 + 2 * k2 + 2 * k3 + k4) / 6
    zn_1 = zn + (q1 + 2 * q2 + 2 * q3 + q4) / 6
    return yn_1, zn_1

def RungeKutta2(x0, y0, z0, h):

    alpha = 0.5
    nh = h / (2 * alpha)
    k1 = functionF_2(x0, y0, z0)
    q1 = functionPHI(x0, y0, z0)
    k2 = functionF_2(x0 + nh, y0 + nh * k1, z0 + nh * q1)
    q2 = functionPHI(x0 + nh, y0 + nh * k1, z0 + nh * q1)
    y1 = y0 + h * ((1 - alpha) * k1 + alpha * k2)
    z1 = z0 + h * ((1 - alpha) * q1 + alpha * q2)
    return y1, z1

def computeResult():
    t = data['Tbegin']
    tmax = data['Tend']
    I = data['I0']
    Uc = data['Uc0']
    hn = data['Tstep']

    I_1 = 0
    U_1 = 0

    for i in numpy.arange(t, tmax, hn):
        graph1[0].append(i)
        graph1[1].append(I) 
        graph2[0].append(i)
        graph2[1].append(Uc)
        I_1, U_1 = RungeKutta4(i, I, Uc, hn)
        I = I_1
        Uc = U_1

    I_1 = 0
    U_1 = 0
    t = data['Tbegin']
    tmax = data['Tend']
    I = data['I0']
    Uc = data['Uc0']
    hn = data['Tstep']


    for i in numpy.arange(t, tmax, hn):
        graph1_1[0].append(i)
        graph1_1[1].append(I) 
        graph2_1[0].append(i)
        graph2_1[1].append(Uc)
        I_1, U_1 = RungeKutta2(i, I, Uc, hn)
        I = I_1
        Uc = U_1

