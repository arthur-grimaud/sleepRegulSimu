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

        #RK4 coefficient
        self.A = [0.5, 0.5, 1.0, 1.0]

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
            if self.t%1000 == 0: #Each x steps
                print(math.floor((100*self.t)/(self.T*self.res)),"%")
                self.getAndSaveRecorders() # variable storage

                print("wake",self.compartments["wake"].F[0])
                print("wakeC",self.compartments["wake"].C[0])
                print("nremC",self.compartments["NREM"].C[0])
                print("remC",self.compartments["REM"].C[0])
                #print("rem",self.compartments["REM"].F[0])

            self.nextStepRK4() # call next step
            self.t += 1 #

        self.writeInFile(self.results) # Write results in a file

    def nextStep(self): #call next step method in each compartments
        for c in self.compartments .values():
            c.setNextStep(self.dt, "Euler")

    def nextStepRK4(self):
        for N in range(4):
            for c in self.compartments .values():
                c.setNextSubStepRK4(self.dt,N,self.A[N])

        for c in self.compartments .values():
            c.setNextStepRK4()

    #-----------------------------Hypnogram--------------------------------------#

    def getHypno(self): #Return the current state of the model
        if self.compartments["wake"].C[0] < 0.4 :
            return 0.5
        elif self.compartments["REM"].C[0] > 0.4 :
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
        self.F = [float(myPopulation["F"]),0,0,0,0]
        self.C  = [float(myPopulation["C"]),0,0,0,0]

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

    def setNextSubStepRK4(self,dt,N,coef):
        self.F[N+1] = self.F[0] + coef * dt * self.getFR(N)
        self.C[N+1] = self.C[0] + coef * dt * self.getC(N)

    def setNextStepRK4(self):
        self.F[0] = (-3*self.F[0] + 2*self.F[1] + 4*self.F[2] + 2*self.F[3] + self.F[4])/6
        self.C[0] = (-3*self.C[0] + 2*self.C[1] + 4*self.C[2] + 2*self.C[3] + self.C[4])/6

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

    def getFR(self,N): #Equation of the firing rate

        return ((self.F_max *(0.5*(1 + np.tanh((self.getI(N) - self.getBeta(N))/self.alpha)))) - self.F[N]  )/self.tau_pop

    def getI(self,N): #Get I from the connection in self.connections
        result = 0
        for c in self.connections:
            if c.type == "NP-NP":
                result += c.getConnectVal(N)
        return result

    def getC(self,N): #differential equation of the neurotransmitter concentration released by the population
        return (np.tanh(self.F[N+1]/self.gamma) - self.C[N])/self.tau_NT

    def getBeta(self,N): #used to handle the homeostatic sleep drive
        if len(self.beta) == 2 :
            for c in self.connections:
                if c.type == "HSD-NP":
                    return c.getConnectVal(N)

        return float(self.beta[0])

    #---------------------------------Recorder------------------------------------#

    def recorder(self): # Return the variables of the population
        return [self.F[0],self.C[0]]


########################HOMEOSTATICSLEEPDRIVE############################
#   ....                  #
#######################################################################

class HomeostaticSleepDrive:
    # creation of the class HomeostaticSleepDrive using the dictionnary cycles  => création objet cycle ??

    def __init__(self, myCycle):
        self.name = "HSD"

        #variable
        self.h = [float(myCycle["h"]),0,0,0,0,]

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

    def setNextSubStepRK4(self,dt,N,coef):
        self.h[N+1] = self.h[0] + coef * dt * self.getH(N)

    def setNextStepRK4(self):
        self.h[0] = (-3*self.h[0] + 2*self.h[1] + 4*self.h[2] + 2*self.h[3] + self.h[4])/6

    def setNextStep(self, dt, method):
        if method == "Euler":
            self.h = self.h+dt*self.getH()
        if method == "RK4":
            self.dh = self.RK4(lambda y: self.getH())
            self.h = self.dh( self.h, dt )

    #---------------------------------Equations------------------------------------#

    def getH(self,N):
        #print(self.theta_X-self.getSourceFR())
        return float((self.H_max-self.h[N])/self.tau_hw*self.heaviside(self.getSourceFR(N)-self.theta_X) - self.h[N]/self.tau_hs*self.heaviside(self.theta_X-self.getSourceFR(N)))

    def getSourceFR(self,N):
        if len(self.connections) > 0:
            return self.connections[0].getConnectVal(N)

    def heaviside(self,X):
        if(X >= 0):
            return 1
        else:
            return 0

    #---------------------------------Recorder------------------------------------#

    def recorder(self):
        return [self.h[0]]


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

    def getConnectVal(self,N):
        if self.type == "NP-NP":
            return self.source.C[N] * self.weight
        if self.type == "HSD-NP":
            return self.source.h[N] * self.weight
        if self.type == "NP-HSD":
            return self.source.F[N]
