#!bin/python
#-*-coding:utf-8-*-

import math

def read_parameters() :
    ### reads the file parameters.txt and extract parameters from it
    # returns a list of dictionnaries of dictionnaries : [populations,concentrations,cycles,time]

    fic = open("default_parameters.txt","r")
    content = fic.read().split("\n")

    populations = {}
    concentrations = {}
    cycles = {}
    simulation_parameters = {}

    # when the check is equal to 1, you're currently in the corresponding block (a popultion block, a concentration block, etc) 
    check_pop = 0   # check wether you're currently in a population block
    check_conc = 0   # check wether you're currently in a concentration block
    check_cycle = 0   # check wether you're currently in a cycle block
    check_sim = 0   # check wether you're currently in a simulation definion block

    for lines in content :
        line = lines.split(" ")
        if len(line) != 0 and line[0] != "//" :
            if line[0] == "*" and check_pop == 0 :
                check_pop = 1
                currentPopulation = line[3]
                populations[currentPopulation] = {}
            elif line[0] == "*" and check_pop == 1 :
                check_pop = 0
            elif line[0] == "@" and check_conc == 0 :
                check_conc = 1
                currentConcentration = line[3]
                concentrations[currentConcentration] = {}
            elif line[0] == "@" and check_conc == 1 : 
                check_conc = 0
            elif line[0] == "+" and check_cycle == 0 :
                check_cycle = 1
                currentCycle = line[3]
                cycles[currentCycle] = {}
            elif line[0] == "+" and check_cycle == 1 :
                check_cycle = 0
            elif line[0] == "#" and check_sim == 0 : 
                check_sim = 1
            elif line[0] == "#" and check_sim == 1 : 
                check_sim = 0
            
            elif check_pop == 1 and line[0] != "*" :
                if line[0] == "g" or line[0] == "pop_ext" or line[0] == "beta" :
                    myParameter = []
                    for i in range(2,len(line)) :
                        myParameter.append(line[i])
                    populations[currentPopulation][line[0]] = myParameter
                else :
                    populations[currentPopulation][line[0]] = line[2]
            elif check_conc == 1 and line[0] != "@" :
                concentrations[currentConcentration][line[0]] = line[2]
            elif check_cycle == 1 and line[0] != "+" :
                cycles[currentCycle][line[0]] = line[2]
            elif check_sim == 1 and line[0] != "#" :
                simulation_parameters[line[0]] = line[2]

    fic.close()
    return populations,concentrations,cycles,simulation_parameters


def write_parameters(name_file,populations,concentrations,cycles,simulation_parameters) :
    ### writes a file with the input parameters
    # creates a file following the same format as default_parameters.txt

    fic = open(name_file,"w")

    for myPop in populations :
        fic.write("* population = "+myPop+"\n")
        for parameter in populations[myPop] :
            if parameter == "g" or parameter == "pop_ext" or parameter == "beta" :
                fic.write(parameter+" =")
                for i in range(len(populations[myPop][parameter])) :
                    fic.write(" "+populations[myPop][parameter][i])
                fic.write("\n")
            else : 
                fic.write(parameter+" = "+populations[myPop][parameter]+"\n")
        fic.write("*\n\n")

    for myConcentration in concentrations : 
        fic.write("@ concentration = "+myConcentration+"\n")
        for parameter in concentrations[myConcentration] :
            fic.write(parameter+" = "+concentrations[myConcentration][parameter]+"\n")
        fic.write("@\n\n")

    for myCycle in cycles : 
        fic.write("+ cycle = "+myCycle+"\n")
        for parameter in cycles[myCycle] :
            fic.write(parameter+" = "+cycles[myCycle][parameter]+"\n")
        fic.write("+\n\n")
    
    fic.write("#\n")
    for parameter in simulation_parameters :
        fic.write(parameter+" = "+simulation_parameters[parameter]+"\n")
    fic.write("#\n")

    fic.close()



class NeuronalPopulation :
    # creation of the class NeuronalPopulation using the dictionnaries populations and concentrations 
    
    def __init__(self,myPopulation,myConcentration) :
        #initial conditions
        self.F = myPopulation["f"]
        self.C  = myConcentration["C"]
        #Firing rate parameters
        self.F_max = myPopulation["F_max"]
        self.beta = myPopulation["beta"]
        self.alpha = myPopulation["alpha"]
        self.tau_pop = myPopulation["tau"]
        #parameters for getI method # both should be lists
        self.g_NT_pop_list = myPopulation["g"]
        self.pop_list = myPopulation["pop_ext"]

        #Neurotransmitter Concentration parameters
        self.gamma = myConcentration["gamma"]
        self.tau_NT = myConcentration["tau"]

        print('Object created')

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

class HomeostaticSleepDrive:
    # creation of the class HomeostaticSleepDrive using the dictionnary cycles  => création objet cycle ?? 
    
    def __init__(self, myCycle):

        self.h = myCycle["h"]
        self.H_max = myCycle["H_max"]
        self.tau_hw = myCycle["tau_w"]
        self.tau_hs = myCycle["tau_s"]
        self.f_X = myCycle["X"]
        self.theta_X = myCycle["theta"]

        print('Object created')

    def getH(self):
        print(self.heaviside(eval(self.f_X).F-self.theta_X))
        return (self.H_max-self.h)/self.tau_hw*self.heaviside(eval(self.f_X).F-self.theta_X) - self.h/self.tau_hs*self.heaviside(self.theta_X-eval(self.f_X).F)

    def heaviside(self,X):
        if(X >= 0):
            return 1
        else:
            return 0

def setClasses() :
    wake = NeuronalPopulation(populations["wake"],concentrations["E"])
    nrem = NeuronalPopulation(populations["NREM"],concentrations["G"])
    rem = NeuronalPopulation(populations["REM"],concentrations["A"])
    homeo = HomeostaticSleepDrive(cycles["homeostatic"])
    return [wake,nrem,rem,homeo]


##### MAIN #####
populations,concentrations,cycles,simulation_parameters = read_parameters()
write_parameters("test.txt",populations,concentrations,cycles,simulation_parameters)
modele = setClasses()


# print("populations :")
# for pop in populations :
#     print '\t',pop,":"
#     for param in populations[pop] :
#         print "\t\t",param,populations[pop][param]
