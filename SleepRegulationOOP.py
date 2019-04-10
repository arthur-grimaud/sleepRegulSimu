import numpy as np

class NeuronalPopulation :
    def __init__(self, F, C, F_max, beta, alpha, gamma, tau_pop, tau_NT, g_NT_pop_list, pop_list):
        #initial conditions
        self.F = F
        self.C  = C
        #Firing rate parameters
        self.F_max = F_max
        self.beta = beta
        self.alpha = alpha
        self.tau_pop = tau_pop
        #parameters for getI method # both should be lists
        self.g_NT_pop_list = g_NT_pop_list
        self.pop_list = pop_list

        #Neurotransmitter Concentration parameters
        self.gamma = gamma
        self.tau_NT = tau_NT

        print('Object created')

    def getFR(self): #differential equation of the firing rate
        return ((self.F_max *(0.5*(1 + np.tanh((self.getI() - self.getBeta())/self.alpha)))) - self.F  )/self.tau_pop

    def getI(self):
        result = 0
        for i in range((len(self.pop_list))):
            result += self.g_NT_pop_list[i] * eval(self.pop_list[i]).C
        return result

    def getC(self): #differential equation of the neurotransmitter concentration released by the population
        return np.tanh((self.F/self.gamma) - self.C)/self.tau_NT

    def getBeta(self): #used to handle the homeostatic sleep drive
        if isinstance (self.beta , list):
            return self.beta[0]*eval(self.beta[1]).h
        else:
            return self.beta

class HomeostaticSleepDrive:
    def __init__(self, h, H_max, tau_hw, f_X, theta_X, tau_hs ):

        self.h = h
        self.H_max = H_max
        self.tau_hw = tau_hw
        self.f_X = f_X
        self.theta_X = theta_X
        self.tau_hs = tau_hs

    def getH(self):
        print(self.heaviside(eval(self.f_X).F-self.theta_X))
        return (self.H_max-self.h)/self.tau_hw*self.heaviside(eval(self.f_X).F-self.theta_X) - self.h/self.tau_hs*self.heaviside(self.theta_X-eval(self.f_X).F)

    def heaviside(self,X):
        if(X >= 0):
            return 1
        else:
            return 0



#instanciation of the neuronal population and homeostatic sleep drive
wake = NeuronalPopulation(6.0, 0.9, 6.5, -0.23, 0.5, 5.0, 25, 25E3, [-2.0, 1.2], ["nrem", "rem"] )
nrem = NeuronalPopulation(1E-3, 1E-3, 5.0, [2.5,"homeo"], 0.25, 4.0, 25, 10E3, [-2.0], ["wake"])
rem = NeuronalPopulation(1E-3, 1E-3, 5.0, -0.6, 0.25, 3.0, 1, 10E3, [-1.3, 1.5, -2.1], ["nrem", "rem", "wake"])
homeo = HomeostaticSleepDrive(0.5, 1.0, 600, "wake", 2.0, 380)



#Simulation parameters
t = 0
T = 30
res = 1E4
dt 	= 1E3/res


while (t < T*res):
    t+=1
    print(homeo.h)
    wake.F = wake.F+dt*wake.getFR()
    nrem.F = nrem.F+dt*nrem.getFR()
    rem.F = rem.F+dt*rem.getFR()

    wake.C = wake.C+dt*wake.getC()
    nrem.C = nrem.C+dt*nrem.getC()
    rem.C = rem.C+dt*rem.getC()

    homeo.h = homeo.h+dt*homeo.getH()
