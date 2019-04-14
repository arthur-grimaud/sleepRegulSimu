#!bin/python
#-*-coding:utf-8-*-

from tkinter import *

from manage_parameters import *
from SleepRegulationOOP import NeuronalPopulation
from SleepRegulationOOP import HomeostaticSleepDrive
from SleepRegulationOOP import Network



pop,cycle,sim,conn=read_parameters()
network = Network(sim)
network.addNP(pop["wake"])
network.addNP(pop["NREM"])
network.addNP(pop["REM"])
network.addHSD(cycle["homeostatic"])

network.addNPConnection("NP-NP","wake","NREM",10)
network.addNPConnection("HSD-NP","HSD","NREM",10)
network.addNPConnection("NP-HSD","NREM","HSD",None)



network.displayConnections()

network.printAttrType("wake")




#network.runSim()











#----------------------------------------




# window = Tk()
# window.title("SR sim")
# window.geometry()
#
#
# b = Button(window, text="load model", command=lambda: readAndAdd())
# b.grid(column=0, row=0)
#
# b2 = Button(window, text="run sim", command=lambda: network.runSim())
# b2.grid(column=0, row=1)
#
#
#
# window.mainloop()

#network.displayCompParam("NREM")

#network.runSim()


#modele = setClasses(populations,concentrations,cycles,simulation_parameters)


# window = Tk()
# window.title("Model Parameters")
# window.geometry()
#
# i = 0
# objFrame = Frame (window)
# for attr, value in network.compartements[0].__dict__.items():
#     i+=1
#     lbl = Label(objFrame, text=attr)
#     lbl.grid(column=0, row=i)
#     txt = Entry(objFrame,width=10)
#     txt.insert(END, value)
#     txt.grid(column=1, row=i)
# objFrame.grid(column=0, row=0)
#
#
#
# window.mainloop()
