#!bin/python
#-*-coding:utf-8-*-

from manage_parameters import *
from classes import *

def setNeuronalPopulations(populations,concentrations) :
    ### set the NeuronalPopulations objects
    wake = NeuronalPopulation(populations["wake"],concentrations["E"])
    nrem = NeuronalPopulation(populations["NREM"],concentrations["G"])
    rem = NeuronalPopulation(populations["REM"],concentrations["A"])
    return [wake,nrem,rem]

def setCycles(cycles) :
    ### set the HomeostaticSleepDrive object
    homeo = HomeostaticSleepDrive(cycles["homeostatic"])
    return [homeo]

def setConnections(connections) :
    ### set the Connections objects
    listConnections = []
    for pop_source in connections.keys() :
        for pop_ext in connections[pop_source] :
            listConnections.append(Connections(pop_source,pop_ext))
    return listConnections

def setModele(populations,concentrations,cycles,simulation_parameters,connections) :
    modele = {}
    modele['populations'] = setNeuronalPopulations(populations,concentrations)
    modele['cycles'] = setCycles(cycles) 
    modele['simulation_parameters'] = simulation_parameters
    modele['connections'] = setConnections(connections)
    return modele

def setNetwork(modele) :
    ### set the Network object

    # creation of the populations list
    listPopulations = []
    for myPop in modele["populations"] :
        listPopulations.append(myPop.name)
    
    # get the homeostatic object
    for cycle in modele["cycles"] :
        if cycle.name == "homeostatic" :
            homeostatic = cycle

    return Network(listPopulations,modele["connections"],homeostatic)


##### MAIN #####
pop,conc,cycle,sim,conn=read_parameters()
modele = setModele(pop,conc,cycle,sim,conn)
# write_parameters("test.txt",modele)

network = setNetwork(modele)
print(vars(network))

# print(modele["populations"])
# print(modele)

# print(connections)
