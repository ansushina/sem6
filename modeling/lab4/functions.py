import numpy as np
from data import data
from math import fabs

a1 = data['a1']
b1 = data['b1']
c1 = data['c1']
m1 = data['m1']
a2 = data['a2']
b2 = data['b2']
c2 = data['c2']
m2 = data['m2']
alpha0 = data['Alpha0']
alphaN = data['AlphaN']
l = data['l']
T0 = data['t0']
R = data['R']
F0 = data['F0']
h = data['h']
t = data['t']


def alpha(x): 
    d = (alphaN * l) / (alphaN - alpha0) 
    c = - alpha0 * d 
    return c / (x - d) 

def KK(x): 
    b = data['kN'] * data['l'] / (data['kN'] - data['k0'])
    a = - b * data['k0'] 
    return a / (T - b)
    
def k(T): 
     return a1 * (b1 + c1 * T ** m1) 
    

def c(T): 
    #return a2 + b2 * T ** m2 - (c2 / T ** 2) 
    return 0

def p(x): 
    return 2 * alpha(x) / R

def f(x): 
    return 2 * alpha(x) * T0 / R

def func_plus_half(x, step, func): 
    return (func(x) + func(x + step)) / 2 

def func_minus_half(x, step, func): 
    return (func(x) + func(x - step)) / 2 

def A(T): 
    return t / h * func_minus_half(T, t, KK) 

def D(T): 
    return t / h * func_plus_half(T, t, KK) 

def B(x, T): 
    return A(T) + D(T) + c(T) * h + p(x) * h * t 

def F(x, T): 
    return f(x) * h * t + c(T) * T * h


def left_condition(y): 
    c0 = c(y[0])
    c12 = func_plus_half(y[0], t, c)
    k12 = func_plus_half(y[0], t, KK)
    p0 = p(0)
    p12 = p(h / 2)

    K0 = h / 8 * c12 + h / 4 * c0 + \
        k12 * t / h + \
        t * h / 8 * p12 + t * h / 4 * p0 
    M0 = h / 8 * c12 - \
        k12 * t / h + \
        t * h * p12 / 8 
    P0 = h / 8 * c12 * (y[0] + y[1]) + \
        h / 4 * c0 * y[0] + \
        F0 * t + t * h / 8 * (3 * f(0) + f(h)) 
    return K0, M0, P0 

def right_condition(y): 
    cn12 = func_minus_half(y[-1], t, c)
    cn = c(y[-1])
    kn12 = func_minus_half(y[-1], t, KK)
    pn12 = p(l - h / 2)
    pn = p(l)
    fn = f(l) 
    fn12 =  f(l - h / 2)


    KN = h / 8 * cn12 + h / 4 * cn + \
        kn12 * t / h + t * alphaN + \
        t * h / 8 * pn12 + t * h / 4 * pn 
    MN = h / 8 * cn12 - \
        kn12 * t / h + \
        t * h * pn12 / 8 
    PN = h / 8 * cn12 * (y[-1] + y[-2]) + \
        h / 4 * cn * y[-1] + t * alphaN * T0 + \
        t * h / 4 * (fn + fn12) 
    return KN, MN, PN 


def calculate(prev): 
    K0,M0,P0 = left_condition(prev)
    KN,MN,PN = right_condition(prev)

    eps = [0, -M0 / K0] 
    eta = [0,  P0 / K0]
     
    x = h 
    n = 1 
    while (x + h < l): 
        new_eps = D(prev[n]) / (B(x, prev[n]) - A(prev[n]) * eps[n])
        new_eta = (F(x, prev[n]) + A(prev[n]) * eta[n]) / (B(x, prev[n]) - A(prev[n]) * eps[n])

        eps.append(new_eps) 
        eta.append(new_eta) 
        n += 1 
        x += h 

    y = [0] * (n + 1) 
    y[n] = (PN - MN * eta[n]) / (KN + MN * eps[n]) 

    for i in range(n - 1, -1, -1): 
        y[i] = eps[i + 1] * y[i + 1] + eta[i + 1] 
    return y

def get_result():
    step1 = int(l / h)
    T = [T0] * (step1 + 1)
    T_new = [0] * (step1 + 1)
    ti = 0
    res = []
    res.append(T)
    lent = len(T)
    while True:
        prev = T
        while True: 
            T_new = calculate(prev)
            max = fabs((T[0] - T_new[0]) / T_new[0])
            for step2, j in zip(T, T_new): 
                d = fabs(step2 - j) / j 
                if d > max: 
                    max = d 
            if max < 1: 
                break 
            
            prev = T_new 
        res.append(T_new) 
        ti += t

        check_eps = 0 
        for i, j in zip(T, T_new): 
            if fabs((i - j) / j) > 1e-2: 
                check_eps = 1 
        if check_eps == 0: 
            break 
        T = T_new

    x = [i for i in np.arange(0, l, h)]
    te = [i for i in range(0, ti, t)]
    return res, x, te
