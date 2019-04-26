#!bin/python
#-*-coding:utf-8-*-

import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import filedialog

from manage_parameters import *
from SleepRegulationOOP import NeuronalPopulation
from SleepRegulationOOP import HomeostaticSleepDrive
from SleepRegulationOOP import Network
from graphique import *
import os

network = Network()

def loadModel():
    global network


    pop,cycle,sim,conn=read_parameters(filedialog.askopenfilename(initialdir = os.getcwd(),title = "Select file",filetypes = (("text files","*.txt"),("all files","*.*"))))
    network = Network(sim)

    for key in pop.keys():
        network.addNP(pop[key])
    print("### Neuronal Populations OK ###\n")

    for key in cycle.keys():
        network.addHSD(cycle[key])
    print("### Homeostatic Sleep Drive OK ###\n")

    # for key in cycle.keys():
    #     network.addNP(conn[key])

    for pop_ext in conn.keys() :
        i = 0
        for pop_source in conn[pop_ext] :
            network.addNPConnection("NP-NP",pop_source,pop_ext,pop[pop_ext]["g_NT_pop_list"][i])
            i+=1
    network.addNPConnection("HSD-NP","HSD","NREM",1.5)
    network.addNPConnection("NP-HSD","wake","HSD",0)
    print("### Connections OK ###\n")

    network.addInjection("NREM",0.8,3600)
    network.getSimParamFrame(runMenu).grid(column = 0, row = 1)


#----------- Window initialization -----------

window = tk.Tk()
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

b = tk.Button(mainMenu, text="Load model", command=lambda: loadModel(),width=25)
b.grid(column=0, row=0)

b = tk.Button(mainMenu, text="Display network", command=lambda: network.displayGraph(),width=25)
b.grid(column=0, row=1)

b = tk.Button(mainMenu, text="Display connections", command=lambda: network.displayConnections(),width=25)
b.grid(column=0, row=2)

txt = tk.Entry(mainMenu,width=25)
txt.insert(END, "Enter compartment name")
txt.grid(column=1, row=3)


b = tk.Button(mainMenu, text="PrintCompParamAndType", command=lambda: network.printAttrType(txt.get()),width=25)
b.grid(column=0, row=3)



#--------------Param menu widgets-------------------

b = tk.Button(paramMenu, text="Display Compartments Parameters", command=lambda: network.displayCompParam(paramMenu).grid(column=0, row=1),width=25)
b.grid(column=0, row=0)

b = tk.Button(paramMenu, text="Add NP (WIP)", command=lambda: network.addObjToModel(network),width=25)
b.grid(column=0, row=4)

b = tk.Button(paramMenu, text="Save Parameters", command=lambda: write_parameters('test.txt',network))
b.grid(column=0, row = 6)
#--------------Run menu widgets-------------------

b = tk.Button(runMenu, text="Run sim", command=lambda: network.runSim(),width=25)
b.grid(column=0, row=0)
b = tk.Button(runMenu, text="Select variables to save(WIP)", command=lambda: network.displayCompVar().grid(column=0, row=2),width=25)
b.grid(column=0, row=2)

#--------------Visualization menu widgets-------------------

b = tk.Button(visuMenu, text="GenerateGraph", command=lambda: createGraph(network.results),width=25).grid(column=0, row=0)

#--------------Visualization menu widgets-------------------

lbl = tk.Label(statMenu, text="Not available yet")
lbl.config(font=("Courier", 30))
lbl.grid(column=0, row=0)


window.mainloop()
