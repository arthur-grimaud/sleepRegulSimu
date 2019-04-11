#!bin/python
#-*-coding:utf-8-*-

from manage_parameters import *
from classes import *

def setObjects() :
    ### set the NeuronalPopulations objects
    wake = NeuronalPopulation(populations["wake"],concentrations["E"])
    nrem = NeuronalPopulation(populations["NREM"],concentrations["G"])
    rem = NeuronalPopulation(populations["REM"],concentrations["A"])

    ### set the HomeostaticSleepDrive object
    homeo = HomeostaticSleepDrive(cycles["homeostatic"])

    # ### set the Connections objects
    # listPopulations = vars()
    # for 

    return {'populations' : [wake,nrem,rem], 'cycles' : [homeo]}


##### MAIN #####
populations,concentrations,cycles,simulation_parameters = read_parameters()
modele = setObjects()
modele['simulation_parameters'] = simulation_parameters

print(modele["populations"])
print(modele)
# write_parameters("test.txt",modele["populations"],modeleconcentrations,cycles,simulation_parameters)

