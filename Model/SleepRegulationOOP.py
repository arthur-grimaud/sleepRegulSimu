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
        self.results = [[],[]]

        self.t = None
        self.T = None
        self.res = None
        self.dt = None

        if len(args) == 1:
            self.t = int(args[0]["t"])
            self.T = int(args[0]["T"])
            self.res = float(args[0]["res"])
            self.dt = 1E3 / self.res


    def setSimParam(self, simParam):
        self.t = int(simParam["t"])
        self.T = int(simParam["T"])
        self.res = float(simParam["res"])
        self.dt = 1E3 / self.res

    #Run simulation methods
    def runSim(self):
        self.initResults()

        while (self.t < self.T*self.res):
            if self.t%20000 == 0:
                print(math.floor((100*self.t)/(self.T*self.res)),"%")
                self.results[0].append(self.t)
                self.results[1].append(self.getHypno())
                self.getAndSaveRecorders()

            self.nextStep()
            self.t += 1

        self.writeInFile(self.results)

    def nextStep(self): #call next step method in each compartments
        for c in self.compartments .values():
            c.setNextStep(self.dt, "Euler")


    #-------------Hypno------------------
    def getHypno(self):
        if self.compartments["wake"].C < 0.4 :
            return 0.5
        elif self.compartments["REM"].C > 0.4 :
            return 0
        else :
            return 1

    #--------------write------------------
    def writeInFile(self,data):
        with open('results.csv', 'w') as f:
            writer = csv.writer(f, delimiter='\t')
            writer.writerows(zip(*data))

        f.close()

    #---------Recorders-----------------
    def initResults(self):
        for c in self.compartments.values():
            for var in c.recorder():
                self.results.append([])

    def getAndSaveRecorders(self):
        i=2
        for c in self.compartments.values():
            for var in c.recorder():
                self.results[i].append(var)
                i+=1


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

        #Equation for RK4

        # self.dF = RK4(lambda t, y: t*getFR(y))
        # self.dF = RK4(lambda t, y: t*getI(y))

        print('NeuronalPopulation object: ', self.name, ' created')

    def RK4(self, f):
        return lambda y, dt: (
                lambda dy1: (
                lambda dy2: (
                lambda dy3: (
                lambda dy4: (dy1 + 2*dy2 + 2*dy3 + dy4)/6
            )( dt * f( y + dy3   ) )
    	    )( dt * f( y + dy2/2 ) )
    	    )( dt * f( y + dy1/2 ) )
    	    )( dt * f( y         ) )

    def setNextStep(self, dt, method):

        if method == "Euler":
            self.F = self.F+dt*self.getFR()
            self.C = self.C+dt*self.getC()
        if method == "RK4":
            self.dF = self.RK4(lambda y: self.getFR())
            self.dC = self.RK4(lambda y: self.getC())

            self.F = self.F+self.dF( self.F, dt )
            self.C = self.C+self.dC( self.C, dt )


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

    def recorder(self):
        return [self.F,self.C]

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

        # self.dh = RK4(lambda t, y: t*getH(y))

        print('HomeostaticSleepDrive object: ', self.name, ' created')


    def RK4(self, f):
        return lambda y, dt: (
                lambda dy1: (
                lambda dy2: (
                lambda dy3: (
                lambda dy4: (dy1 + 2*dy2 + 2*dy3 + dy4)/6
            )( dt * f( y + dy3   ) )
    	    )( dt * f( y + dy2/2 ) )
    	    )( dt * f( y + dy1/2 ) )
    	    )( dt * f( y         ) )

    def setNextStep(self, dt, method):
        if method == "Euler":
            self.h = self.h+dt*self.getH()
        if method == "RK4":
            self.dh = self.RK4(lambda y: self.getH())
            self.h = self.dh( self.h, dt )


    def getH(self):
        return float((self.H_max-self.h)/self.tau_hw*self.heaviside(self.getSourceFR()-self.theta_X) - self.h/self.tau_hs*self.heaviside(self.theta_X-self.getSourceFR()))

    def getSourceFR(self):
        if len(self.connections) > 0:
            return self.connections[0].getConnectVal()

    def heaviside(self,X):
        if(X >= 0):
            return 1
        else:
            return 0

    def recorder(self):
        return [self.h]


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
