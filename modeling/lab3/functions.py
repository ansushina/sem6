from data import data, graph1
import numpy as np

b = data['kN'] * data['l'] / (data['kN'] - data['k0'])
a = - b * data['k0'] 
d = data['AlphaN'] * data['l'] / (data['AlphaN'] - data['Alpha0'])
c = - b * data['Alpha0'] 
h = data['h']
N = data['l']

def k(x):
    return a / (x - b)

def Alpha(x):
    return c / (x - d) 

def P(x):
    return 2/data['R'] * Alpha(x)

def f(x):
    return 2*data['t0']/data['R'] *Alpha(x)

def KHIminus12(x):
    return 2*k(x)*k(x-h)/(k(x) + k(x-h))
    #return (k(x) + k(x-h)) /2

def KHIplus12(x):
    return 2*k(x)*k(x+h)/(k(x) + k(x+h))
    #return (k(x) + k(x+h))/2

def A(n): 
    return KHIplus12(n)/h

def C(n):
    return KHIminus12(n)/h

def B(n):
    return A(n) + C(n) + P(n)*h

def D(n):
    return f(n) * h


def calculate(): 
    xstart = 0
    xend = data['l']

    #левые
    
    p0 = P(xstart)
    p1 = P(xstart + h)
    p12 = (p0+p1)/2

    f0 = f(xstart)
    f1 = f(xstart+h)
    f12 = (f0+f1)/2

    M0 = -KHIplus12(xstart) + h*h/8*p12
    K0 = KHIplus12(xstart) + h*h/8*p12 + h*h/4*p0
    P0 = h*data['F0'] + h*h/4*(f12 + f0)

    #правые

    pn = P(xend)
    pn1 = P(xend - h)
    pn12 = (pn+pn1)/2

    fn = f(xend)
    fn1 = f(xend-h)
    fn12 = (fn+fn1)/2

    Mn = (-KHIminus12(xend) + h * h * pn12 / 8)
    Kn = (KHIminus12(xend) + data['AlphaN'] * h + h * h * pn12 / 8 + h * h * pn / 4);
    Pn = (data['AlphaN'] * data['t0'] * h + h * h * (fn12 + fn) / 4);


    eps = [0, -M0/K0 ]
    eta = [0, P0/K0]


    x = h
    n = 1
    while x + h < N:
        eps.append(C(x) / (B(x) - A(x) * eps[n]))
        eta.append((A(x) * eta[n] + D(x)) / (B(x) - A(x) * eps[n]))
        n += 1
        x += h
    
    t = [0] * (n + 1)
    
    t[n] = (Pn - Mn * eta[n]) / (Kn + Mn * eps[n]) 
    for i in range(n - 1, -1, -1):
        t[i] = eps[i + 1] * t[i + 1] + eta[i + 1]
    
    graph1[0] =  [i for i in np.arange(0, N, h)]
    graph1[1] = t[:-1]




