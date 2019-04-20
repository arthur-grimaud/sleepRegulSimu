#!bin/python
#-*-coding:utf-8-*-

#######################IMPORTATIONS########################

#Calculation
import numpy as np
import math
#GUI generation
from GUI import NetworkGUI
#Saving data
import csv

########################NETWORK############################
#This class is used to manage the simulation    ....      #
###########################################################

class Network(NetworkGUI):

    #-----------------------------------Constructor------------------------------------#
    def __init__(self,*args):


        self.compartments  = {} #Ditionnary containing all the compartments objects
        self.results = []  #Data storage

        #Simulation parameters
        self.t = None # Used to store the number of time steps done
        self.T = None # Simulation time in seconds
        self.res = None # Iterations per seconds
        self.dt = None # Time step in milliseconds

        if len(args) == 1: #If the parameters dictionnary has been given to the constructor
            self.t = int(args[0]["t"])
            self.T = int(args[0]["T"])
            self.res = float(args[0]["res"])
            self.dt = 1E3 / self.res

    #-----------------------------------Setter------------------------------------#

    def setSimParam(self, simParam):  #Set the simulation parameters from a dictionnary
        self.t = int(simParam["t"])
        self.T = int(simParam["T"])
        self.res = float(simParam["res"])
        self.dt = 1E3 / self.res

    #------------------------------Run simulation----------------------------------#

    def runSim(self):
        self.initResults()

        while (self.t < self.T*self.res): # Main loop
            if self.t%20000 == 0: #Each x milliseconds
                print(math.floor((100*self.t)/(self.T*self.res)),"%")
                self.getAndSaveRecorders() # variable storage

            self.nextStep() # call next step
            self.t += 1 #

        self.writeInFile(self.results) # Write results in a file

    def nextStep(self): #call next step method in each compartments
        for c in self.compartments .values():
            c.setNextStep(self.dt, "Euler")

    #-----------------------------Hypnogram--------------------------------------#

    def getHypno(self): #Return the current state of the model
        if self.compartments["wake"].C < 0.4 :
            return 0.5
        elif self.compartments["REM"].C > 0.4 :
            return 0
        else :
            return 1

    #-------------------------------Write----------------------------------------#

    def writeInFile(self,data):
        with open('results.csv', 'w') as f:
            writer = csv.writer(f, delimiter='\t')
            writer.writerows(zip(*data))

        f.close()

    #-----------------------------Recorders--------------------------------------#

    def initResults(self): #Set the correct number of Sublist in self.results in function of the number of variable to be saved
        for v in self.recorder():
            self.results.append([])
        for c in self.compartments.values():
            for var in c.recorder():
                self.results.append([])

    def getAndSaveRecorders(self): #Call the recorders in each compartements
        i=0
        for var in self.recorder():
            self.results[i].append(var)
            i+=1
        for c in self.compartments.values():
            for var in c.recorder():
                self.results[i].append(var)
                i+=1

    def recorder(self):
        return[self.t,self.getHypno()]

    #-------------------------Network modification methods------------------------------#

    def addNP(self, populationParam): #Add an instance of NeuronalPopulation to the compartments dictionnary
        self.compartments [populationParam["name"]] = NeuronalPopulation(populationParam)

    def addHSD(self, cycleParam): #Add an instance of HomeostaticSleepDrive to the compartments dictionnary
        self.compartments ['HSD'] = HomeostaticSleepDrive(cycleParam)

    def addNPConnection(self, type, sourceName, targetName, weight): #Add a connection object to the concerned compartment
        self.compartments [targetName].connections.append(Connection(type, self.compartments [sourceName],self.compartments [targetName],weight))

    #-------------------------------Debugging methods----------------------------------#

    def printAttrType(self,compID): #Print name,value,type of all attributs of a compartment.
        for attr, value in self.compartments [compID].__dict__.items():
            print(attr," ",value," ",type(value))

    def displayConnections(self): #Print all connections wich are in a compartment informations
        for attr, value in self.compartments .items():
            for conn in value.connections:
                print("Connection type: ",conn.type,"  ", conn.source.name,"--",conn.weight,"-->",conn.target.name)



########################NeuronalPopulation ############################
#Class representing a neuronal population    ....                  #
#######################################################################


class NeuronalPopulation :

    #-----------------------------------Constructor------------------------------------#

    # creation of the class NeuronalPopulation using the dictionnary "population"
    def __init__(self,myPopulation) :
        self.name = myPopulation["name"]

        #List of 'Connection' objects
        self.connections = []

        #initial conditions (Variables)
        self.F = float(myPopulation["F"])
        self.C  = float(myPopulation["C"])

        #Firing rate parameters (Constants used in the FiringRate equation)
        self.F_max = float(myPopulation["F_max"])
        self.beta = myPopulation["beta"]
        self.alpha = float(myPopulation["alpha"])
        self.tau_pop = float(myPopulation["tau_pop"])

        #Neurotransmitter Concentration parameters (Constants used in the Neurotransmitter concentration equation)
        self.concentration = myPopulation["concentration"]
        self.gamma = float(myPopulation["gamma"])
        self.tau_NT = float(myPopulation["tau_NT"])

        #Equation for RK4

        # self.dF = RK4(lambda t, y: t*getFR(y))
        # self.dF = RK4(lambda t, y: t*getI(y))

        print('NeuronalPopulation object: ', self.name, ' created')

    #-----------------------------------ODE resolver------------------------------------#

    def RK4(self, f): #Runge-Kutta of the fourth order (NOT WORKING)
        return lambda y, dt: (
                lambda dy1: (
                lambda dy2: (
                lambda dy3: (
                lambda dy4: (dy1 + 2*dy2 + 2*dy3 + dy4)/6
            )( dt * f( y + dy3   ) )
    	    )( dt * f( y + dy2/2 ) )
    	    )( dt * f( y + dy1/2 ) )
    	    )( dt * f( y         ) )

    #-----------------------------------??------------------------------------#

    def setNextStep(self, dt, method): #Set the Popualtion variable
    #args: dt:Time step  / method:Method of ODE resolution used
        if method == "Euler":
            self.F = self.F+dt*self.getFR()
            self.C = self.C+dt*self.getC()
        if method == "RK4": #(NOT WORKING)
            self.dF = self.RK4(lambda y: self.getFR())
            self.dC = self.RK4(lambda y: self.getC())

            self.F = self.F+self.dF( self.F, dt )
            self.C = self.C+self.dC( self.C, dt )

    #---------------------------------Equations------------------------------------#

    def getFR(self): #Equation of the firing rate
        return ((self.F_max *(0.5*(1 + np.tanh((self.getI() - self.getBeta())/self.alpha)))) - self.F  )/self.tau_pop

    def getI(self): #Get I from the connection in self.connections
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

    #---------------------------------Recorder------------------------------------#

    def recorder(self): # Return the variables of the population
        return [self.F,self.C]


########################HOMEOSTATICSLEEPDRIVE############################
#   ....                  #
#######################################################################

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

    #---------------------------------Equations------------------------------------#

    def getH(self):
        print(self.theta_X-self.getSourceFR())
        return float((self.H_max-self.h)/self.tau_hw*self.heaviside(self.getSourceFR()-self.theta_X) - self.h/self.tau_hs*self.heaviside(self.theta_X-self.getSourceFR()))

    def getSourceFR(self):
        if len(self.connections) > 0:
            return self.connections[0].getConnectVal()

    def heaviside(self,X):
        if(X >= 0):
            return 1
        else:
            return 0

    #---------------------------------Recorder------------------------------------#

    def recorder(self):
        return [self.h]


#############################CONNECTION################################
#   ....                                                              #
#######################################################################

class Connection:
    # creation of the connections class, which manages the connections between the different populations (manages the concentrations and associated weights)

    def __init__(self, type, source, target, weight) :
        self.type = type # String describing the type of connection. Depends on the type of compartments connected
        self.source = source # Compartement object
        self.target = target # Compartement object
        self.weight = float(weight) #Weight of the connection

        print('Connection object',self.source.name ,'-',self.target.name ,'created')

    def getConnectVal(self):
        if self.type == "NP-NP":
            return self.source.C * self.weight
        if self.type == "HSD-NP":
            return self.source.h * self.weight
        if self.type == "NP-HSD":
            return self.source.F
