#!bin/python
#-*-coding:utf-8-*-

import numpy as np
from tkinter import *
import math
from graphviz import Digraph
from GUI import NetworkGUI
import csv


class Network(NetworkGUI):

    def __init__(self,*args):
        self.compartments  = {}
        self.results = {}

        self.t = None
        self.T = None
        self.res = None
        self.dt = None

        if len(args) == 1:
            self.t = int(args[0]["t"])
            self.T = int(args[0]["T"])
            self.res = float(args[0]["res"])
            self.dt = float(args[0]["dt"]) / self.res


    def setSimParam(self, simParam):
        self.t = int(simParam["t"])
        self.T = int(simParam["T"])
        self.res = float(simParam["res"])
        self.dt = float(simParam["dt"]) / self.res

    #Run simulation methods
    def runSim(self):
        currT = self.t
        tempResults=[[],[]]
        #self.setRecorders()
        while (currT < self.T*self.res):
            # print(currT)
            print(float(self.compartments["wake"].F))
            #self.recorders()

            tempResults[0].append(currT)
            tempResults[1].append(self.getHypno())

            self.nextStep()
            currT += 1

        print(tempResults)
        self.writeInFile(tempResults)

    def nextStep(self): #call next step method in each compartments
        for c in self.compartments .values():
            c.setNextStep(self.dt)

    #---------Hypno----------------

    def getHypno(self):
        if self.compartments["wake"].C < 0.4 :
            print(0.5)
            return 0.5
        elif self.compartments["REM"].C > 0.4 :
            print(0)
            return 0
        else :
            print(1)
            return 1


    def writeInFile(self,data):
        with open('hypno.csv', 'w') as f:
            writer = csv.writer(f, delimiter='\t')
            writer.writerows(zip(data[0],data[1]))
        quit()

    #---------Recorders-----------------

    def setRecorders(self):
        self.results["wake_F"] =[]
        self.results["NREM_F"] =[]


    def getRecordersParam(self):
        # param =[]
        # for c in self.compartements:
        #     param.append()
        return [["wake","F"],["NREM","F"]]

    def recorders(self):
        for var in self.getRecordersParam():
            key = var[0]+"_"+var[1]
            self.results.setdefault(key, []).append(float(getattr(self.compartments[var[0]],var[1])))


    #Network modification methods

    def addNP(self, populationParam):
        self.compartments [populationParam["name"]] = NeuronalPopulation(populationParam)

    def addHSD(self, cycleParam):
        self.compartments ['HSD'] = HomeostaticSleepDrive(cycleParam)

    def addNPConnection(self, type, sourceName, targetName, weight):
        self.compartments [targetName].connections.append(Connection(type, self.compartments [sourceName],self.compartments [targetName],weight))

    #Debugging methods

    def printAttrType(self,compID):
        for attr, value in self.compartments [compID].__dict__.items():
            print(attr," ",value," ",type(value))

    def displayConnections(self):
        for attr, value in self.compartments .items():
            for conn in value.connections:
                print("Connection type: ",conn.type,"  ", conn.source.name,"--",conn.weight,"-->",conn.target.name)






class NeuronalPopulation :
    # creation of the class NeuronalPopulation using the dictionnaries populations and concentrations

    def __init__(self,myPopulation) :
        self.name = myPopulation["name"]

        #List of 'Connection' objects
        self.connections = []

        #initial conditions
        self.F = float(myPopulation["F"])   ## variable
        self.C  = float(myPopulation["C"])   ## variable

        #Firing rate parameters
        self.F_max = float(myPopulation["F_max"])
        self.beta = myPopulation["beta"]
        self.alpha = float(myPopulation["alpha"])
        self.tau_pop = float(myPopulation["tau_pop"])

        #Neurotransmitter Concentration parameters
        self.concentration = myPopulation["concentration"]
        self.gamma = float(myPopulation["gamma"])
        self.tau_NT = float(myPopulation["tau_NT"])

        print('NeuronalPopulation object: ', self.name, ' created')


    def setNextStep(self, dt):
        self.F = self.F+dt*self.getFR()
        self.C = self.C+dt*self.getC()


    def getFR(self): #differential equation of the firing rate
        return ((self.F_max *(0.5*(1 + np.tanh((self.getI() - self.getBeta())/self.alpha)))) - self.F  )/self.tau_pop
    def getI(self):
        result = 0
        for c in self.connections:
            if c.type == "NP-NP":
                result += c.getConnectVal()
        return result

    def getC(self): #differential equation of the neurotransmitter concentration released by the population
        return np.tanh((self.F/self.gamma) - self.C)/self.tau_NT

    def getBeta(self): #used to handle the homeostatic sleep drive
        if len(self.beta) == 2 :
            for c in self.connections:
                if c.type == "HSD-NP":
                    return c.getConnectVal()

        return int(float(self.beta[0]))

class HomeostaticSleepDrive:
    # creation of the class HomeostaticSleepDrive using the dictionnary cycles  => création objet cycle ??

    def __init__(self, myCycle):
        self.name = "HSD"

        self.h = float(myCycle["h"])
        self.H_max = float(myCycle["H_max"])
        self.tau_hw = float(myCycle["tau_hw"])
        self.tau_hs = float(myCycle["tau_hs"])
        #self.f_X = myCycle["f_X"]
        self.theta_X = float(myCycle["theta_X"])

        self.connections = []

        print('HomeostaticSleepDrive object: ', self.name, ' created')


    def setNextStep(self, dt):
        self.h = self.h+dt*self.getH()


    def getH(self):
        return (self.H_max-self.h)/self.tau_hw*self.heaviside(self.getSourceFR()-self.theta_X) - self.h/self.tau_hs*self.heaviside(self.theta_X-self.getSourceFR())

    def getSourceFR(self):
        if len(self.connections) > 0:
            return self.connections[0].getConnectVal()

    def heaviside(self,X):
        if(X >= 0):
            return 1
        else:
            return 0


class Connection:
    # creation of the connections class, which manages the connections between the different populations (manages the concentrations and associated weights)

    def __init__(self, type, source, target, weight) :
        self.type = type
        self.source = source
        self.target = target
        self.weight = float(weight)

        print('Connection object',self.source.name ,'-',self.target.name ,'created')

    def getConnectVal(self):
        if self.type == "NP-NP":
            return self.source.C * self.weight
        if self.type == "HSD-NP":
            return self.source.h * self.weight
        if self.type == "NP-HSD":
            return self.source.F


class NetworkGUI:
    def __init__(self) :
        pass

    def displayCompParam(self,window):

        i = 0
        objFrame = Frame (window)
        for comp in self.compartments.values():
            i += 1
            self.getCompartmentFrame(comp,objFrame).grid(column=i, row=0)
        return objFrame


    def getCompartmentFrame(self, comp, frame):

        i = 0
        compFrame = Frame (frame)

        lbl = Label(compFrame, text=comp.name)
        lbl.config(font=("Courier", 15))
        lbl.grid(column=0, row=0)

        for attr, value in comp.__dict__.items():

            if isinstance(value, list) and len(value) > 0 and isinstance(value[0], Connection): #Si liste de connection
                for c in value:
                    i += 1
                    lbl = Label(compFrame, text="connection: ")
                    lbl.grid(column=0, row=i)
                    txt = Entry(compFrame, width=10)
                    txt.insert(END, c.source.name)
                    txt.grid(column=1, row=i)
                    txt = Entry(compFrame, width=10)
                    txt.insert(END, c.target.name)
                    txt.grid(column=2, row=i)
                    txt = Entry(compFrame, width=10)
                    txt.insert(END, c.weight)
                    txt.grid(column=3, row=i)
            else:
                i += 1
                lbl = Label(compFrame, text=attr)
                lbl.grid(column=0, row=i)
                txt = Entry(compFrame, width=10)
                txt.insert(END, value)
                txt.grid(column=1, row=i)


        return compFrame


    def displayCompVar(self,window):

        i = 0
        frame = Frame (window)
        for comp in self.compartments.values():
            i += 1
            lbl = Label(frame, text=comp.name)
            lbl.grid(column=0, row=i)
            cb = Checkbutton(frame, text = "FiringRate", width = 20)
            cb.grid(column=1, row=i)
            cb = Checkbutton(frame, text = "Concentration", width = 20)
            cb.grid(column=2, row=i)

        return frame


    def getCreationWindow(self):   #Temporary implementation

        creaWin = Tk()

        i = 0

        for attr, value in self.compartments["NREM"].__dict__.items():
            i+=1
            lbl = Label(creaWin, text=attr)
            lbl.grid(column=0, row=i)
            txt = Entry(creaWin, width=10)
            txt.insert(END, "0")
            txt.grid(column=1, row=i)


        b = Button(creaWin, text="Create Compartment", command=lambda: self.CreateObjFromCreationWindow(creaWin),width=25)
        b.grid(column=2, row=0)

        creaWin.mainloop()


    def getCreationWindowConnect(self):   #Temporary implementation

        creaWin = Tk()

        #source
        lbl = Label(creaWin, text="source")
        lbl.grid(column=0, row=0)
        txt = Entry(creaWin, width=10)
        txt.insert(END, "0")
        txt.grid(column=1, row=0)
        #target
        lbl = Label(creaWin, text="target")
        lbl.grid(column=0, row=1)
        txt = Entry(creaWin, width=10)
        txt.insert(END, "0")
        txt.grid(column=1, row=1)
        #weight
        lbl = Label(creaWin, text="weight")
        lbl.grid(column=0, row=2)
        txt = Entry(creaWin, width=10)
        txt.insert(END, "0")
        txt.grid(column=1, row=2)
        #type
        lbl = Label(creaWin, text="type")
        lbl.grid(column=0, row=3)
        txt = Entry(creaWin, width=10)
        txt.insert(END, "0")
        txt.grid(column=1, row=3)


        b = Button(creaWin, text="Create Connection", command=lambda: self.CreateObjFromCreationWindowConnect(creaWin),width=25)
        b.grid(column=0, row=5)

        creaWin.mainloop()


    def CreateObjFromCreationWindow(self, window):   #Temporary implementation

        allWidgets = window.winfo_children() #get all widgets from the Object creation window
        popParam = {}
        for w in range(0, len(allWidgets)-2, 2):
            popParam[(allWidgets[w]['text'])] = allWidgets[w+1].get()
            print(allWidgets[w], allWidgets[w+1])
        self.addNP(popParam)

        window.destroy()


    def CreateObjFromCreationWindowConnect(self, window):   #Temporary implementation

        allWidgets = window.winfo_children() #get all widgets from the Object creation window
        popParam = {}
        for w in range(0, len(allWidgets)-1, 2):
            popParam[(allWidgets[w]['text'])] = allWidgets[w+1].get()
            print(allWidgets[w], allWidgets[w+1])
        self.addNP(popParam)

        window.destroy()




    def displayGraph(self):
        dot = Digraph()

        for cName in self.compartments .keys():
            dot.node(str(cName),str(cName))

        for cObj in self.compartments .values():
            for conn in cObj.connections:
                    if conn.weight < 0:
                        dot.edge(str(conn.source.name),str(conn.target.name), constraint='true',directed='false',arrowhead='tee')
                    if conn.weight > 0:
                        dot.edge(str(conn.source.name),str(conn.target.name), constraint='true',directed='false')

        dot.render('test-output.gv', view=True)
