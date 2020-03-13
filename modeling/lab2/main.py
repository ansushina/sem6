import matplotlib.pyplot as plt 
import const
from interpolate import computeResult

from tkinter import *
root = Tk()

varList = {
    "R": StringVar(),
    "Tw": StringVar(),
    "Ck": StringVar(),
    "Lk": StringVar(),
    "Rk": StringVar(),
    "Uc0": StringVar(),
    "I0": StringVar(),
    "Le": StringVar(),
    "Tbegin": StringVar(),
    "Tend": StringVar(),
    "Tstep": StringVar(),
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
    print(const.data)
    computeResult()
    print(const.graph1)
    print(const.graph2)
    
    plt.plot(const.graph2[0], const.graph2[1])
    plt.show()


if __name__ == '__main__':
    
    btn = Button(root, text="START") 
    create_grid(root)

    btn.bind("<Button-1>", start_work)       
    btn.grid(column=1, padx=10, pady=10)                          
    root.mainloop()