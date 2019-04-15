#!bin/python
#-*-coding:utf-8-*-

from tkinter import *
from tkinter import ttk
from tkinter import filedialog

from manage_parameters import *
from SleepRegulationOOP import NeuronalPopulation
from SleepRegulationOOP import HomeostaticSleepDrive
from SleepRegulationOOP import Network
import os





network = Network()


def loadModel():
    global network


    pop,cycle,sim,conn=read_parameters(filedialog.askopenfilename(initialdir = os.getcwd(),title = "Select file",filetypes = (("text files","*.txt"),("all files","*.*"))))
    network = Network(sim)

    for key in pop.keys():
        network.addNP(pop[key])

    for key in cycle.keys():
        network.addHSD(cycle[key])

    # for key in cycle.keys():
    #     network.addNP(conn[key])

    network.addNPConnection("NP-NP","wake","REM",-4)
    network.addNPConnection("NP-NP","REM","wake",1)
    network.addNPConnection("NP-NP","REM","REM",1.6)
    network.addNPConnection("NP-NP","NREM","REM",-1.3)
    network.addNPConnection("NP-NP","wake","NREM",-2)
    network.addNPConnection("NP-NP","NREM","wake",-1.68)
    network.addNPConnection("HSD-NP","HSD","NREM",1.5)
    network.addNPConnection("NP-HSD","NREM","HSD",0)



#----------- Window initialization -----------

window = Tk()
window.title("SR sim")
window.geometry()


n = ttk.Notebook(window)   # Creation of tab system
n.pack()

mainMenu = ttk.Frame(n)       # Add main tab
mainMenu.pack()

paramMenu = ttk.Frame(n)       # Add parameters tab
paramMenu.pack()

runMenu = ttk.Frame(n)       # Add run tab
runMenu.pack()

visuMenu = ttk.Frame(n)       # Add visualization tab
visuMenu.pack()

statMenu = ttk.Frame(n)       # Add statistics tab
statMenu.pack()

n.add(mainMenu, text='Main')
n.add(paramMenu, text='Parameters')
n.add(runMenu, text='Run')
n.add(visuMenu, text='Visualization')
n.add(statMenu, text='Statistics')



#-----------Main menu widgets---------------

b = Button(mainMenu, text="Load model", command=lambda: loadModel(),width=25)
b.grid(column=0, row=0)

b = Button(mainMenu, text="Display network", command=lambda: network.displayGraph(),width=25)
b.grid(column=0, row=1)

b = Button(mainMenu, text="Display connections", command=lambda: network.displayConnections(),width=25)
b.grid(column=0, row=2)

txt = Entry(mainMenu,width=25)
txt.insert(END, "Enter compartment name")
txt.grid(column=1, row=3)


b = Button(mainMenu, text="PrintCompParamAndType", command=lambda: network.printAttrType(txt.get()),width=25)
b.grid(column=0, row=3)



#--------------Param menu widgets-------------------

b = Button(paramMenu, text="Display Compartments Parameters", command=lambda: network.displayCompParam(paramMenu).grid(column=0, row=1),width=25)
b.grid(column=0, row=0)

#--------------Run menu widgets-------------------

b = Button(runMenu, text="Run sim", command=lambda: network.runSim(),width=25)
b.grid(column=0, row=0)
b = Button(runMenu, text="Select variables to save(WIP)", command=lambda: network.displayCompVar(runMenu).grid(column=0, row=2),width=25)
b.grid(column=0, row=1)

#--------------Visualization menu widgets-------------------

lbl = Label(visuMenu, text="Not available yet")
lbl.config(font=("Courier", 30))
lbl.grid(column=0, row=0)

#--------------Visualization menu widgets-------------------

lbl = Label(statMenu, text="Not available yet")
lbl.config(font=("Courier", 30))
lbl.grid(column=0, row=0)


window.mainloop()
