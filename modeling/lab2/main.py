import matplotlib.pyplot as plt 
import const
from functions import computeResult

from tkinter import *
root = Tk()

varList = {
    "R": StringVar(),
    "Le": StringVar(),
    "Lk": StringVar(),
    "Ck": StringVar(),
    "Rk": StringVar(),
    "Uc0": StringVar(),
    "I0": StringVar(),
    "Tw": StringVar(),
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


def clear_graphs(): 
    const.graph1[0].clear()
    const.graph1[1].clear()
    const.graph2[0].clear()
    const.graph2[1].clear()
    const.graph3[0].clear()
    const.graph3[1].clear()
    const.graph4[0].clear()
    const.graph4[1].clear()
    const.graph1_1[0].clear()
    const.graph1_1[1].clear()
    const.graph2_1[0].clear()
    const.graph2_1[1].clear()
    const.graph3_1[0].clear()
    const.graph3_1[1].clear()
    const.graph4_1[0].clear()
    const.graph4_1[1].clear()
    const.graph5[0].clear()
    const.graph5[1].clear()

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
    
    plt.title('I ')
    plt.subplot(2, 3, 2)
    plt.plot(const.graph2_1[0], const.graph2_1[1])
    plt.plot(const.graph2[0], const.graph2[1])
    
    plt.title('UC' )
    plt.subplot(2, 3, 4)
    plt.plot(const.graph3_1[0], const.graph3_1[1])
    plt.plot(const.graph3[0], const.graph3[1])
    
    plt.title('Rp')
    plt.subplot(2, 3, 5)
    plt.plot(const.graph4_1[0], const.graph4_1[1])
    plt.plot(const.graph4[0], const.graph4[1])
    
    plt.title('I * Rp')
    plt.subplot(2, 3, 3)
    plt.plot(const.graph5[0], const.graph5[1])
    plt.title('T0')
    plt.show()


if __name__ == '__main__':
    
    btn = Button(root, text="START") 
    create_grid(root)

    btn.bind("<Button-1>", start_work)       
    btn.grid(column=1, padx=10, pady=10)                          
    root.mainloop()