#!bin/python
#-*-coding:utf-8-*-

import numpy as np
from tkinter import *
import math
from graphviz import Digraph


class Network:

    def __init__(self,simParam):
        self.compartements = {}
        #self.connections = {}

        self.t = int(simParam["t"])
        self.T = int(simParam["T"])
        self.res = float(simParam["res"])
        self.dt = float(simParam["dt"]) / self.res

        self.results = {}


    #Run simulation methods
    def runSim(self):
        currT = 0
        while (self.t < self.T*self.res):
            print(currT)
            print(self.compartements["NREM"].F)
            self.nextStep()
            currT+=1


    def nextStep(self): #call next step method in each compartements
        for c in self.compartements.values():
            c.nextStep(self.dt)

    #Network modification methods

    def addNP(self, populationParam):
        self.compartements[populationParam["name"]] = NeuronalPopulation(populationParam)

    def addHSD(self, cycleParam):
        self.compartements['HSD'] = HomeostaticSleepDrive(cycleParam)

    def addNPConnection(self, type, sourceName, targetName, weight):
        self.compartements[targetName].connections.append(Connection(type, self.compartements[sourceName],self.compartements[targetName],weight))

    #Display methods

    def displayCompParam(self,compID):
        window = Tk()
        window.title("Model Parameters")
        window.geometry()
        i = 0
        objFrame = Frame (window)
        for attr, value in self.compartements[compID].__dict__.items():
            i+=1
            lbl = Label(objFrame, text=attr)
            lbl.grid(column=0, row=i)
            txt = Entry(objFrame,width=10)
            txt.insert(END, value)
            txt.grid(column=1, row=i)
        objFrame.grid(column=0, row=0)
        window.mainloop()

    def displayGraph(self):
        dot = Digraph()

        for cName in self.compartements.keys():
            dot.node(str(cName),str(cName))

        for cObj in self.compartements.values():
            for conn in cObj.connections:
                    if conn.weight < 0:
                        dot.edge(str(conn.source.name),str(conn.target.name), constraint='true',directed='false',arrowhead='tee')
                    if conn.weight > 0:
                        dot.edge(str(conn.source.name),str(conn.target.name), constraint='true',directed='false')

        dot.render('test-output.gv', view=True)

    #Debugging methods

    def printAttrType(self,compID):
        for attr, value in self.compartements[compID].__dict__.items():
            print(attr, type(value))

    def displayConnections(self):
        for attr, value in self.compartements.items():
            for conn in value.connections:
                print("Connection type: ",conn.type,"  ", conn.source.name,"--",conn.weight,"-->",conn.target.name)






class NeuronalPopulation :
    # creation of the class NeuronalPopulation using the dictionnaries populations and concentrations

    def __init__(self,myPopulation) :
        self.name = myPopulation["name"]
        #initial conditions
        self.F = float(myPopulation["f"])   ## variable
        self.C  = float(myPopulation["C"])   ## variable
        #Firing rate parameters
        self.F_max = float(myPopulation["F_max"])

        self.beta = myPopulation["beta"]
        self.alpha = float(myPopulation["alpha"])
        self.tau_pop = float(myPopulation["tau_pop"])
        #parameters for getI method # both should be lists
        #self.g_NT_pop_list = myPopulation["g_NT_pop_list"]
        #self.pop_list = myPopulation["pop_list"]

        self.connections = []

        #Neurotransmitter Concentration parameters
        self.concentration = myPopulation["concentration"]
        self.gamma = float(myPopulation["gamma"])
        self.tau_NT = float(myPopulation["tau_NT"])

        print('Neuronal population object', self.name, 'created')


    def nextStep(self, dt):
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

        print('Object created')


    def nextStep(self, dt):
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
        self.weight = weight

        print('Connection object',self.source,'-',self.target,'created')

    def getConnectVal(self):
        if self.type == "NP-NP":
            return self.source.C * self.weight
        if self.type == "HSD-NP":
            return self.source.h * self.weight
        if self.type == "NP-HSD":
            return self.source.F
