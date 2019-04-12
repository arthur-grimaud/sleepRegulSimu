#!bin/python
#-*-coding:utf-8-*-

import math

class NeuronalPopulation :
    # creation of the class NeuronalPopulation using the dictionnaries populations and concentrations 
    
    def __init__(self,myPopulation,myConcentration) :
        self.name = myPopulation["name"]
        #initial conditions
        self.F = myPopulation["f"]   ## variable
        self.C  = myConcentration["C"]   ## variable
        #Firing rate parameters
        self.F_max = myPopulation["F_max"]
        self.beta = myPopulation["beta"]
        self.alpha = myPopulation["alpha"]
        self.tau_pop = myPopulation["tau"]
        #parameters for getI method # both should be lists
        self.g_NT_pop_list = myPopulation["g"]
        self.pop_list = myPopulation["pop_ext"]

        #Neurotransmitter Concentration parameters
        self.concentration = myConcentration["name"]
        self.gamma = myConcentration["gamma"]
        self.tau_NT = myConcentration["tau"]

        print('Neuronal population object', self.name, 'created')

    def getFR(self): #differential equation of the firing rate
        return ((self.F_max *(0.5*(1 + math.tanh((self.getI() - self.getBeta())/self.alpha)))) - self.F  )/self.tau_pop

    def getI(self):
        result = 0
        for i in range((len(self.pop_list))):
            result += self.g_NT_pop_list[i] * eval(self.pop_list[i]).C
        return result

    def getC(self): #differential equation of the neurotransmitter concentration released by the population
        return math.tanh((self.F/self.gamma) - self.C)/self.tau_NT

    def getBeta(self): #used to handle the homeostatic sleep drive
        if len(self.beta) == 2 :
            return self.beta[0]*eval(self.beta[1]).h
        else :
            return self.beta[0]

    ### ajouter la fonction step (modifie chaque variable par la nouvelle variable, sans sauvegarder celle précédente)

class HomeostaticSleepDrive:
    # creation of the class HomeostaticSleepDrive using the dictionnary cycles  => création objet cycle ?? 
    
    def __init__(self, myCycle):

        self.name = myCycle["name"]
        ### variables
        self.h = myCycle["h"]
        self.f_X = myCycle["X"]

        ### parameters
        self.H_max = myCycle["H_max"]
        self.tau_hw = myCycle["tau_w"]
        self.tau_hs = myCycle["tau_s"]
        self.theta_X = myCycle["theta"]

        print('Homeostatis sleep drive object created')

    def getH(self):
        print(self.heaviside(eval(self.f_X).F-self.theta_X))
        return (self.H_max-self.h)/self.tau_hw*self.heaviside(eval(self.f_X).F-self.theta_X) - self.h/self.tau_hs*self.heaviside(self.theta_X-eval(self.f_X).F)

    def heaviside(self,X):
        if(X >= 0):
            return 1
        else:
            return 0
    
    ### lit la population X, calcule h puis injecte h dans une autre population 


class Connections:
    # creation of the connections class, which manages the connections between the different populations (manages the concentrations and associated weights)

    def __init__(self,source,target) :
        self.source = source
        self.target = target

        print('Connection object',self.source,'-',self.target,'created')
    
    ### lit les concentrations et les poids, calcule la nouvelle concentration et envoie vers la population cible pendant la fonction step


class Network :
    # creation of the network class, which manages the whole network formed by the neuronal populations and the different connections between them

    def __init__(self,listPopulations,connections,HomeostaticSleepDrive) :
        self.listPopulations = listPopulations
        self.listConnections = connections
        self.homeostatic = HomeostaticSleepDrive

        print("Network object created")
