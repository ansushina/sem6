from const import ItK, Tsigma, data, graph4, graph3, graph2, graph1
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
        yResult = y1 + ((xValue - x1) / (x2 - x1)) * (y2 - y1);   
    else:
        if (xValue < table[0][xIndex]):
            yResult = table[0][yIndex]
        if (xValue > table[len(table) - 1][xIndex]):
            yResult = table[len(table) - 1][yIndex]
            
    return yResult;

def getTz(T0, m, r):
    z = r / data['R'];
    return (data['Tw'] - T0) * math.pow(z, m) + T0

def siqmaFunc(I, z):
    m = interpolate(ItK, I, 0, 2)
    T0 = interpolate(ItK, I, 0, 1)
    Tz = getTz(T0, m, z)
    siqma = interpolate(Tsigma, Tz, 0, 1)
    return siqma

def integrateSimpson(I):
    n = 40
    integrateBegin = 0
    integrateEnd = 1
    width = (integrateEnd - integrateBegin) / n
    result = 0
    for step in range(n):
        x1 = integrateBegin + step * width
        x2 = integrateBegin + (step + 1) * width
        result += (x2 - x1) / 6.0 * (siqmaFunc(I, x1) + 4.0 * siqmaFunc(I, 0.5 * (x1 + x2)) + siqmaFunc(I, x2))
    return result

def calculateRp(I):
    R = data['R']
    integral = integrateSimpson(I)
    return data['Le'] / (2 * math.pi * R * R * integral)

def functionF(xn, yn, zn):
    Rp = calculateRp(yn)
    graph3[0].append(xn)
    graph3[1].append(Rp)
    graph4[0].append(xn)
    graph4[1].append(yn*Rp)
    return ((zn - (data['Rk'] + Rp) * yn) / data['Lk'])

def functionPHI(xn, yn, zn):
    return -1 / data['Ck'] * yn


def RungeKutta4(xn, yn, zn, hn):
    k1 = functionF(xn, yn, zn)
    q1 = functionPHI(xn, yn, zn)

    k2 = functionF(xn + hn / 2, yn + k1 * hn / 2, zn + q1 * hn / 2)
    q2 = functionPHI(xn + hn / 2, yn + k1 * hn / 2, zn + q1 * hn / 2)

    k3 = functionF(xn + hn / 2, yn + k2 * hn / 2, zn + q2 * hn / 2)
    q3 = functionPHI(xn + hn / 2, yn + k2 * hn / 2, zn + q2 * hn / 2)

    k4 = functionF(xn + hn / 2, yn + k3 * hn, zn + q3 * hn)
    q4 = functionPHI(xn + hn / 2, yn + k3 * hn, zn + q3 * hn)

    yn_1 = yn + hn * (k1 + 2 * k2 + 2 * k3 + k4) / 6
    zn_1 = zn + hn * (q1 + 2 * q2 + 2 * q3 + q4) / 6
    return yn_1, zn_1

def RungeKutta2(xn, yn, zn, hn):
    alpha = 1;
    yn_1 = (yn + hn * ((1 - alpha) * functionF(xn, yn, zn) +
            alpha * functionF(xn + hn / (2 * alpha), yn + hn / (2 * alpha), zn + hn / (2 * alpha)) *
            functionF(xn, yn, zn)))
    zn_1 = (yn + hn * ((1 - alpha) * functionPHI(xn, yn, zn) +
            alpha * functionPHI(xn + hn / (2 * alpha), yn + hn / (2 * alpha), zn + hn / (2 * alpha)) *
            functionPHI(xn, yn, zn)))
    return yn_1, zn_1

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