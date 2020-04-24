from data import data

b = data['kN'] * l / (data['kN'] - data['k0'])
a = - b * data['k0'] 
d = data['alphaN'] * l / (data['alphaN'] - data['alpha0'])
c = - b * data['alpha0'] 
h = data['h']

def K(x):
    return a / (x - b)

def Alpha(x):
    return c / (x - d)

def P(x):
    return 2/data['R'] * Alpha(x)

def f(x):
    return 2*data['T0']/data['R'] *Alpha(x)

def KHIminus12(x):
    return 2*k(x)*k(x-h)/(k(x) + k(x-h))

def KHIplus12(x):
    return 2*k(x)*k(x+h)/(k(x) + k(x+h))


def calculate(): 

   
    xstart = 0
    xend = data['l']

    //левые
    
    p0 = P(xstart)
    p1 = P(xstart + h)
    p12 = (p0+p1)/2

    f0 = f(xstart)
    f1 = f(xstart+h)
    f12 = (f0+f1)/2

    //правые

    pn = P(xend)
    pn1 = P(xend - h)
    pn12 = (pn+pn1)/2

    fn = f(xend)
    fn1 = f(xend-h)
    fn12 = (fn0+fn1)/2



