import numpy as np

class NeuronalPopulation :
    #Constructor **Args**
    # F : Firing rate initial value
    # C : Initial concentration of the neuronal population associated neurotransmitter
    # ...
    # beta : could be either a constant or a list (decription à completer)
    # ...
    # g_NT_pop_list : list of weights of the synaptic response to a neurottransmitter Concentration
    # pop_list : Populations associated to the weight list declared in "g_NT_pop_list". Have to be a list of strings corresponding to the name of a NeuronalPopulation instance.
    # (note, g_NT_pop_list and pop_list have to be the same length)
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
        return (self.H_max-self.h)/self.tau_hw*self.heaviside(eval(self.f_X).F-self.theta_X) - self.h/self.tau_hs*self.heaviside(self.theta_X-eval(self.f_X).F)

    def heaviside(self,X):
        if(X >= 0):
            return 1
        else:
            return 0



#instanciation of the neuronal population and homeostatic sleep drive objects (Rodent SR parameters)
# wake = NeuronalPopulation(6.0, 0.9, 6.5, -0.23, 0.5, 5.0, 25, 25E3, [-2.0, 1.2], ["nrem", "rem"] )
# nrem = NeuronalPopulation(1E-3, 1E-3, 5.0, [2.5,"homeo"], 0.25, 4.0, 25, 10E3, [-2.0], ["wake"])
# rem = NeuronalPopulation(1E-3, 1E-3, 5.0, -0.6, 0.25, 3.0, 1, 10E3, [-1.3, 1.5, -2.1], ["nrem", "rem", "wake"])
# homeo = HomeostaticSleepDrive(0.5, 1.0, 600, "wake", 2.0, 380)

# (Human SR parameters)
wake = NeuronalPopulation(6.0, 0.9, 6.5, -0.4,           0.5, 5.0, 1500E3, 25E3, [-1.68, 1.0], ["nrem", "rem"] )
nrem = NeuronalPopulation(1E-3, 1E-3, 5.0, [1.5,"homeo"], 0.175, 4.0, 600E3, 10E3, [-2.0], ["wake"])
rem = NeuronalPopulation(1E-3, 1E-3, 5.0, -0.9,          0.13, 2.0, 60E3, 10E3, [-1.3, 1.6, -4], ["nrem", "rem", "wake"])
homeo = HomeostaticSleepDrive(0.5, 1.0, 3483E3, "wake", 2.0,30600E3)



#Simulation parameters
t = 0
T = 1
res = 10
dt 	= 1E3/res

#temporary: (storage)
wakeF = []
nremF = []
remF = []

wakeC = []
nremC = []
remC = []

hL = []


while (t < T*res):
    t+=1
    print(rem.C)
    wake.F = wake.F+dt*wake.getFR()
    nrem.F = nrem.F+dt*nrem.getFR()
    rem.F = rem.F+dt*rem.getFR()

    wake.C = wake.C+dt*wake.getC()
    nrem.C = nrem.C+dt*nrem.getC()
    rem.C = rem.C+dt*rem.getC()

    homeo.h = homeo.h+dt*homeo.getH()

    wakeF.append(wake.F)
    nremF.append(nrem.F)
    remF.append(rem.F)
    wakeC.append(wake.C)
    nremC.append(nrem.C)
    remC.append(rem.C)

    hL.append(homeo.h)






from tkinter import *
# import SleepRegulationOOP.py as SR
#
#
#
# wake = SR.NeuronalPopulation(6.0, 0.9, 6.5, -0.23, 0.5, 5.0, 25, 25E3, [-2.0, 1.2], ["nrem", "rem"] )

window = Tk()
window.title("Model Parameters")
window.geometry()



i = 0
objFrame = Frame (window)
for attr, value in wake.__dict__.items():
    i+=1
    lbl = Label(objFrame, text=attr)
    lbl.grid(column=0, row=i)
    txt = Entry(objFrame,width=10)
    txt.insert(END, value)
    txt.grid(column=1, row=i)
objFrame.grid(column=0, row=0)

i = 0
objFrame = Frame (window)
for attr, value in nrem.__dict__.items():
    i+=1
    lbl = Label(objFrame, text=attr)
    lbl.grid(column=0, row=i)
    txt = Entry(objFrame,width=10)
    txt.insert(END, value)
    txt.grid(column=1, row=i)
objFrame.grid(column=1, row=0)

i = 0
objFrame = Frame (window)
for attr, value in rem.__dict__.items():
    i+=1
    lbl = Label(objFrame, text=attr)
    lbl.grid(column=0, row=i)
    txt = Entry(objFrame,width=10)
    txt.insert(END, value)
    txt.grid(column=2, row=i)
objFrame.grid(column=2, row=0)





window.mainloop()
