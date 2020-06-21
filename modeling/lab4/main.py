import matplotlib.pyplot as plt 
import data as const
from functions import get_result

from tkinter import *
root = Tk()

varList = {
    "k0": StringVar(),
    "kN": StringVar(),
     'a1' : StringVar(),
    'b1' : StringVar(),
    'c1' : StringVar(),
    'm1': StringVar(),
    'a2': StringVar(),
    'b2': StringVar(),
    'c2': StringVar(),
    'm2': StringVar(),
    "Alpha0": StringVar(),
    "AlphaN": StringVar(),
    "l": StringVar(),
    "t0": StringVar(),
    "R": StringVar(),
    "F0": StringVar(),
    "h": StringVar(),
    't': StringVar(),
}

def create_grid(root):
    i = 0
    for var in varList.keys(): 
        label = Label(root, text=var)
        label.grid(row=i, column=0, sticky="e")
        entry = Entry(root,width=10,textvariable=varList[var])
        entry.grid(row=i, column=1)
        entry.insert(0, str(const.resetData[var]))
        i+=1

def check_is_num():
    for var in varList.values():
        try:
            float(var.get())
        except ValueError:
            return False
    return True    


def start_work(Event):
    if not check_is_num():
        print("WARNING NOT DIGIT")
        return
    for var in varList.keys():
        const.data[var] = float(varList[var].get())
    res, x, te = get_result()


    plt.subplot(1, 2, 1)

    step1 = 0 
    for i in res:
        if (step1 % 2 == 0):
            plt.plot(x, i[:-1])
        step1 +=1

    plt.title('T(x)')
    plt.plot(x , res[-1][:-1])
    plt.xlabel("x, sm")
    plt.ylabel("T, K")
    plt.grid()


    plt.subplot(1, 2, 2)
    h = const.data['h']
    step2 = 0 
    while (step2 < 2):
        point =  [j[int(step2 / h)] for j in res] 
        plt.plot(te, point[:-1])
        step2 += 0.1
    plt.xlabel("t, sec")
    plt.ylabel("T, K")
    plt.grid()
    plt.show()

    

if __name__ == '__main__':
    
    btn = Button(root, text="START") 
    create_grid(root)

    btn.bind("<Button-1>", start_work)       
    btn.grid(column=1, padx=10, pady=10)                          
    root.mainloop()