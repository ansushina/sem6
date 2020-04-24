import matplotlib.pyplot as plt 
import const
from functions import computeResult

from tkinter import *
root = Tk()

varList = {
    "k0": StringVar(),
    "kN": StringVar(),
    "Alpha0": StringVar(),
    "AlphaN": StringVar(),
    "l": StringVar(),
    "T0": StringVar(),
    "R": StringVar(),
    "F0": StringVar(),
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


def clear_graphs(): 
    const.graph1[0].clear()
    const.graph1[1].clear()

def start_work(Event):
    clear_graphs()
    if not check_is_num():
        print("WARNING NOT DIGIT")
        return
    for var in varList.keys():
        const.data[var] = float(varList[var].get())
    computeResult()

    plt.subplot(2, 3, 1)
    plt.plot(const.graph1_1[0], const.graph1_1[1])
    plt.plot(const.graph1[0], const.graph1[1])
    

if __name__ == '__main__':
    
    btn = Button(root, text="START") 
    create_grid(root)

    btn.bind("<Button-1>", start_work)       
    btn.grid(column=1, padx=10, pady=10)                          
    root.mainloop()