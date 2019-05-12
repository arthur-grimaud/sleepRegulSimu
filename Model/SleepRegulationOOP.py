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
#This class is used to manage the simulation              #
###########################################################

class Network(NetworkGUI):

    #-----------------------------------Constructor------------------------------------#
    def __init__(self,*args):

        self.compartments  = {} #Ditionnary containing all the compartments objects
        self.results = []  #Data storage
        self.headers = [] # Data storage
        self.injections = [] #injection storage

        #Simulation parameters
        self.step = None # Used to store the number of time steps done
        self.T = None # Simulation time in seconds
        self.res = None # Iterations per seconds
        self.dt = None # Time step in milliseconds
        self.saveRate = 100 # Save rate in number of steps
        self.t = 0 # Current time of the model
        self.onset = 10 # Time until data is stored in seconds
        self.resMethod = "Euler" #Differential equation resolution method

        #Hypnogram Setup :

        self.wakeThreshold = 0.4  # Greater limit of wake promoting NT concentration for wich the model is considered in WAKE state.
        self.REMThreshold = 0.4 # Lower limit of REM promoting NT concentration for wich the model is considered in REM state.

        #RK4 coefficient
        self.A = [0.5, 0.5, 1.0, 1.0]

        if len(args) == 1: #If the parameters dictionnary has been given to the constructor
            self.step = float(args[0]["t"])
            self.T = float(args[0]["T"])
            self.res = float(args[0]["res"])
            self.dt = 1E3 / self.res
            self.t = 0
            self.mean = float(args[0]["mean"])
            self.std = float(args[0]["std"])

    #-----------------------------------Noise-----------------------------------#

    def additiveWhiteGaussianNoise(self): #Returns white noise from a Gaussian distribution
        meanNoise = 0.0 # Mean white noise value in [Hz]
        stdNoise = 0.001 # STD white noise value in [Hz]
        noiseSample = np.random.normal(meanNoise, stdNoise)
        return noiseSample

    #-----------------------------------Setter------------------------------------#

    def setSimParam(self, simParam):  #Set the simulation parameters from a dictionnary
        self.step = float(simParam["t"])
        self.T = float(simParam["T"])
        self.res = float(simParam["res"])
        self.dt = 1E3 / self.res
        self.t = 0

    #------------------------------Run simulation----------------------------------#

    def runSim(self):
        self.initResults()


        while (self.step < self.T*self.res): # Main loop

            if self.step%self.saveRate == 0 and self.step >= self.onset*self.res : #Each x steps
                print(math.floor((100*self.step)/(self.T*self.res)),"%")# Print simulation progress
                self.getAndSaveRecorders() # variable storage

            #Equation resolution
            if self.resMethod == "Euler":
                self.nextStepEuler()
            elif self.resMethod == "RK4":
                self.nextStepRK4()
            else:
                print("Error: ODE resolution method not defined")

            self.step += 1
            self.t = math.floor(self.step/self.res) # current time since simulation time in sc


    def nextStepEuler(self): #call Euler next step method in each compartments
        for c in self.compartments .values():
            if isinstance(c,NeuronalPopulation):
                noise = self.additiveWhiteGaussianNoise()
                c.setNextStepEuler(self.dt, 0, noise)
            else:
                c.setNextStepEuler(self.dt, 0)

    def nextStepRK4(self): #call RK4 next step method in each compartments
        for N in range(4):
            for c in self.compartments.values():
                c.setNextSubStepRK4(self.dt,N,self.A[N])
            for i in self.injections:
                i.setNextSubStepRK4(self.dt,N,self.A[N])

        for c in self.compartments.values():
            if isinstance(c,NeuronalPopulation):
                noise = self.additiveWhiteGaussianNoise()
                c.setNextStepRK4(noise)
            else:
                c.setNextStepRK4()

        for i in self.injections:
            i.setNextStepRK4()



    #-----------------------------Hypnogram--------------------------------------#

    def getHypno(self): #Return the current state of the model
        WAKEpromoting = 0
        RpNb = 0
        REMpromoting = 0

        for c in self.compartments.values():
            if isinstance(c,NeuronalPopulation):
                if c.promoting == "WAKE":
                    WAKEpromoting += c.C[0]
                if c.promoting == "REM":
                    REMpromoting += c.C[0]


        if WAKEpromoting < self.wakeThreshold :
            if REMpromoting > self.REMThreshold :
                return 0.5
            else :
                return 0
        else :
            return 1

    #-------------------------------Write results in file----------------------------------------#

    def fileHeader(self) :
        header = "### "
        for (compartment,values) in self.compartments.items() :
            if "neurotransmitter" in dir(values) :
                header += str(compartment)+"--->"+str(values.neurotransmitter)+" "
        header+="\n"
        return header

    def writeInFile(self,filename,data):
        filename.write(self.fileHeader())
        writer = csv.writer(filename, delimiter='\t')
        writer.writerows(zip(*data))
        filename.close()

    #-----------------------------Recorders--------------------------------------#

    def initResults(self): #Set the correct number of Sublist in self.results in function of the number of variable to be saved
        for header in self.recorder():
            self.results.append([header])
            self.headers.append(header)
        for c in self.compartments.values():
            for header in c.recorder():
                self.results.append([header])
                self.headers.append(header)

    def getAndSaveRecorders(self): #Call the recorders in each compartements
        i=0
        for var in self.headers:
            if var in self.recorder().keys() :
                self.results[i].append(self.recorder()[var])
                i+=1
            for c in self.compartments.values():
                if var in c.recorder().keys() :
                    self.results[i].append(c.recorder()[var])
                    i+=1

    def recorder(self):
        return {'time': self.t, 'hypnogram': self.getHypno()}



    #-------------------------Network modification methods------------------------------#

    def addNP(self, populationParam): #Add an instance of NeuronalPopulation to the compartments dictionnary
        self.compartments [populationParam["name"]] = NeuronalPopulation(populationParam)

    def addHSD(self, cycleParam): #Add an instance of HomeostaticSleepDrive to the compartments dictionnary
        self.compartments ['HSD'] = HomeostaticSleepDrive(cycleParam)

    def addNPConnection(self, type, sourceName, targetName, weight): #Add a connection object to the concerned compartment
        self.compartments [targetName].connections.append(Connection(type, self.compartments [sourceName],self.compartments [targetName],weight))

    def addInjection(self, connection, P0, TauInj, iMin, iMax, type ):
        if type == "Agonist":
            connection.addInjE(Injection(P0, TauInj, iMin, iMax))
            self.injections.append(connection.inj)
        if type == "Antagonist":
            connection.addInjE(Injection(P0, TauInj, iMin, iMax))
            self.injections.append(connection.inj)

    #-------------------------------Debugging methods----------------------------------#

    def printAttrType(self,compID): #Print name,value,type of all attributs of a compartment.
        for attr, value in self.compartments [compID].__dict__.items():
            print(attr," ",value," ",type(value))

    def displayConnections(self): #Print all connections wich are in a compartment informations
        for attr, value in self.compartments .items():
            for conn in value.connections:
                print("Connection type: ",conn.type,"  ",conn.source.name,"--",conn.weight,"-->",conn.target.name)

    #-----------------------------Save parameters------------------------------------#

    def save_parameters(self) :
        string = "#\n"
        for parameter in vars(self) :
            if parameter == 't' or parameter == 'T' or parameter == 'res' or parameter == 'mean' or parameter == 'std':
                string += parameter+" = "+str(getattr(self,parameter))+"\n"
        string += "#\n\n"
        return string



########################NeuronalPopulation ############################
#Class representing a neuronal population                             #
#######################################################################


class NeuronalPopulation :

    #-----------------------------------Constructor------------------------------------#

    # creation of the class NeuronalPopulation using the dictionnary "population"
    def __init__(self,myPopulation) :
        self.name = myPopulation["name"]
        self.promoting = myPopulation["promoting"] #

        #List of 'Connection' objects


        #initial conditions (Variables)
        self.F = [float(myPopulation["F"]),0,0,0,0]
        self.C  = [float(myPopulation["C"]),0,0,0,0]

        #Firing rate parameters (Constants used in the FiringRate equation)
        self.F_max = float(myPopulation["F_max"])
        self.beta = myPopulation["beta"]
        self.alpha = float(myPopulation["alpha"])
        self.tau_pop = float(myPopulation["tau_pop"])

        #Neurotransmitter Concentration parameters (Constants used in the Neurotransmitter concentration equation)
        self.neurotransmitter = myPopulation["neurotransmitter"]
        self.gamma = float(myPopulation["gamma"])
        self.tau_NT = float(myPopulation["tau_NT"])
        self.connections = []
        #Equation for RK4

        # self.dF = RK4(lambda t, y: t*getFR(y))
        # self.dF = RK4(lambda t, y: t*getI(y))

        print('NeuronalPopulation object: ', self.name, ' created')

    #-----------------------------------Next step------------------------------------#

    def setNextSubStepRK4(self,dt,N,coef):
        self.F[N+1] = self.F[0] + coef * dt * self.getFR(N)
        self.C[N+1] = self.C[0] + coef * dt * self.getC(N)

    def setNextStepRK4(self, noise):
        self.F[0] = ((-3*self.F[0] + 2*self.F[1] + 4*self.F[2] + 2*self.F[3] + self.F[4])/6) + noise
        self.C[0] = (-3*self.C[0] + 2*self.C[1] + 4*self.C[2] + 2*self.C[3] + self.C[4])/6

        if self.F[0] < 0: #FR not negative
            self.F[0] = 0

    def setNextStepEuler(self,dt,N, noise):
        self.F[0]  = self.F[0] + dt * self.getFR(N) + noise
        self.C[0] = self.C[0] + dt * self.getCEuler()

    #---------------------------------Equations------------------------------------#

    def getFR(self,N): #Equation of the firing rate
        return ((self.F_max *(0.5*(1 + np.tanh((self.getI(N) - self.getBeta(N))/self.alpha)))) - self.F[N]  )/self.tau_pop

    def getI(self,N): #Get I from the connection in self.connections
        result = 0
        for c in self.connections:
            if c.type == "NP-NP":
                result += c.getConnectVal(N)

        return result

    def getC(self,N): #equation of the neurotransmitter concentration released by the population
        return (np.tanh(self.F[N+1]/self.gamma) - self.C[N])/self.tau_NT

    def getCEuler(self): #equation of the neurotransmitter concentration released by the population
        return (np.tanh(self.F[0]/self.gamma) - self.C[0])/self.tau_NT

    def getBeta(self,N): #used to handle the homeostatic sleep drive

        for c in self.connections:
            if c.type == "HSD-NP":
                return c.getConnectVal(N)

        return float(self.beta[0])

    #---------------------------------Recorder------------------------------------#

    def recorder(self): # Return the variables of the population
        header_F = self.name+"_F"
        header_C = self.name+"_C"
        return {header_F: self.F[0], header_C: self.C[0]}

    #-----------------------------Save parameters------------------------------------#

    def save_parameters(self) :
        string = "* population = "+self.name+"\n"
        for parameter in vars(self) :
            if parameter == 'F' or parameter == 'C' :
                string += parameter+" = "+str(getattr(self,parameter)[0])+"\n"
            elif parameter == 'connections' :
                tmp = {}
                tmp["g_NT_pop_list"] = []
                tmp["pop_list"] = []
                for connection in getattr(self,parameter) :
                    tmp["g_NT_pop_list"].append(connection.weight)
                    tmp["pop_list"].append(connection.source.name)
                for (key,value) in tmp.items() :
                    string += key+" ="
                    for element in value :
                        string += " "+str(element)
                    string += "\n"
            elif isinstance(getattr(self,parameter),list) :
                string += parameter+" ="
                for value in getattr(self,parameter) :
                    string += " "+str(value)
                string += "\n"
            elif parameter != 'name' and parameter != 'connections':
                string += parameter+" = "+str(getattr(self,parameter))+"\n"
        string += "*\n\n"
        return string


########################HOMEOSTATIC SLEEP DRIVE##########################
#                                                                       #
#########################################################################

class HomeostaticSleepDrive:
    # creation of the class HomeostaticSleepDrive using the dictionnary cycles  => création objet cycle 

    def __init__(self, myCycle):
        self.name = "HSD"

        #variable
        self.h = [float(myCycle["h"]),0,0,0,0,]

        self.H_max = float(myCycle["H_max"])
        self.tau_hw = float(myCycle["tau_hw"])
        self.tau_hs = float(myCycle["tau_hs"])
        self.theta = float(myCycle["theta"])

        self.connections = []

        print('HomeostaticSleepDrive object: ', self.name, ' created')


    def setNextSubStepRK4(self,dt,N,coef):
        self.h[N+1] = self.h[0] + coef * dt * self.getH(N)

    def setNextStepRK4(self):
        #print(self.name, " H ", self.h[0])
        self.h[0] = (-3*self.h[0] + 2*self.h[1] + 4*self.h[2] + 2*self.h[3] + self.h[4])/6

    def setNextStepEuler(self,dt,N):
        self.h[0]  = self.h[0] + dt * self.getH(N)



    #---------------------------------Equations------------------------------------#

    def getH(self,N): # Homeostatic Sleep Drive value equation
        return float((self.H_max-self.h[N])/self.tau_hw * self.heaviside(self.getSourceFR(N)-self.theta) - self.h[N]/self.tau_hs*self.heaviside(self.theta-self.getSourceFR(N)))

    def getSourceFR(self,N):
        res = 0
        for c in self.connections:
            if c.type == "NP-HSD":
                res += self.connections[0].getConnectVal(N)

        return res

    def heaviside(self,X):
        if(X >= 0):
            return 1
        else:
            return 0

    #---------------------------------Recorder------------------------------------#

    def recorder(self):
        return {'homeostatic': self.h[0]}

    #-----------------------------Save parameters------------------------------------#

    def save_parameters(self) :
        string = "+ cycle = "+self.name+"\n"
        for parameter in vars(self) :
            if parameter == 'h' :
                string += parameter+" = "+str(getattr(self,parameter)[0])+"\n"
            elif parameter == 'connections' :
                tmp = {}
                tmp["g_NT_pop_list"] = []
                tmp["pop_list"] = []
                for connection in getattr(self,parameter) :
                    tmp["g_NT_pop_list"].append(connection.weight)
                    tmp["pop_list"].append(connection.source.name)
                for (key,value) in tmp.items() :
                    string += key+" ="
                    for element in value :
                        string += " "+str(element)
                    string += "\n"
            elif isinstance(getattr(self,parameter),list) :
                string += parameter+" ="
                for value in getattr(self,parameter) :
                    string += " "+str(value)
                string += "\n"
            elif parameter != 'name' and parameter != 'connections':
                string += parameter+" = "+str(getattr(self,parameter))+"\n"
        string += "+\n\n"
        return string


#############################CONNECTION################################
#                                                                     #
#######################################################################

class Connection: # creation of the connections class, which manages the connections between the different populations (manages the concentrations and associated weights)

    def __init__(self, type, source, target, weight) :
        self.type = type # String describing the type of connection. Depends on the type of compartments connected
        self.source = source # Compartement object
        self.target = target # Compartement object
        self.weight = float(weight) #Weight of the connection
        self.inj = None

        print('Connection object',self.source.name ,'-',self.target.name ,'created with weight ',self.weight)

    def addInjE(self,injObj):
        self.type = "NP-MIE-NP" # MIE : MicroInjection Excitatory (Agonist)
        self.inj = injObj
        print("NP-NP connection has been modified into NP-MIE-NP")

    def addInjI(self,injObj):
        self.type = "NP-MII-NP" # MIE : MicroInjection Inhibitory (Antagonist)
        self.inj = injObj
        print("NP-NP connection has been modified into NP-MII-NP")

    def getConnectVal(self,N):
        if self.type == "NP-NP":
            #print(self.source.name," " ,self.source.C[N] * self.weight, " " ,self.target.name, "( C: ",self.source.C[N]," * w:",self.weight,") N:", N )
            return self.source.C[N] * self.weight
        if self.type == "HSD-NP":
            #print(self.source.name," " ,self.source.h[N] * self.weight, " " ,self.target.name)
            return self.source.h[N] * self.weight
        if self.type == "NP-HSD":
            #print(self.source.name," " ,self.source.F[N], " " ,self.target.name)
            return self.source.F[N]
        if self.type == "NP-MIE-NP": #microinjections of agonist simulations
            return Mi*self.source.C[N]+Pi
        if self.type == "NP-MII-NP": #microinjections of antagonist simulations
            return (1-Pi)*self.source.C[N]



#############################Injection#################################
#                                                                     #
#######################################################################


class Injection:

    def __init__(self, P, tauPi, iMin, iMax) :
        self.P = [P,0,0,0,0]
        self.tauPi = tauPi #Au
        self.iMin = iMin #Au
        self.imax = iMax #Au


    def getP(self,N):
        return -(self.P[N]/self.tauPi)

    def getMi(self):
        if self.P <= self.iMin:
            return 1
        else:
            return 1 - (self.P[0] - self.iMin)/(self.iMax - self.iMin)

    def setNextSubStepRK4(self,dt,N,coef):
        self.P[N+1] = self.P[0] + coef * dt * self.getP(N)

    def setNextStepRK4(self):
        self.P[0] = (-3*self.P[0] + 2*self.P[1] + 4*self.P[2] + 2*self.P[3] + self.P[4])/6
