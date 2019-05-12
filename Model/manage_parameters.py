#!bin/python
#-*-coding:utf-8-*-

def read_parameters(file) :
    ### reads the file parameters.txt and extracts parameters from it
    # returns a list of dictionnaries of dictionnaries : [populations,concentrations,cycles,time]

    fic = open(file,"r")
    content = fic.read().split("\n")

    populations = {}
    cycles = {}
    simulation_parameters = {}

    connections = {}

    # when the check is equal to 1, you're currently in the corresponding block (a popultion block, a concentration block, etc)
    check_pop = 0   # check whether you're currently in a population block
    check_cycle = 0   # check whether you're currently in a cycle block
    check_sim = 0   # check whether you're currently in a simulation definition block

    for lines in content :
        line = lines.split(" ")
        if len(line) != 0 and line[0] != "//" and line[0] != '' :
            if line[0] == "*" and check_pop == 0 :
                check_pop = 1
                currentPopulation = line[3]
                populations[currentPopulation] = {}
                populations[currentPopulation]["name"] = currentPopulation
            elif line[0] == "*" and check_pop == 1 :
                check_pop = 0
            elif line[0] == "+" and check_cycle == 0 :
                check_cycle = 1
                currentCycle = line[3]
                cycles[currentCycle] = {}
                cycles[currentCycle]["name"] = currentCycle
            elif line[0] == "+" and check_cycle == 1 :
                check_cycle = 0
            elif line[0] == "#" and check_sim == 0 :
                check_sim = 1
            elif line[0] == "#" and check_sim == 1 :
                check_sim = 0

            elif (check_pop == 1 and line[0] != "*") :
                if line[0] == "g_NT_pop_list" or line[0] == "pop_list" or line[0] == "beta" :
                    myParameter = []
                    for i in range(2,len(line)) :
                        myParameter.append(line[i])
                    populations[currentPopulation][line[0]] = myParameter
                else :
                    populations[currentPopulation][line[0]] = line[2]
                if line[0] == "pop_list" :
                    connections[currentPopulation] = myParameter
            elif check_cycle == 1 and line[0] != "+" :
                if line[0] == "g_NT_pop_list" or line[0] == "pop_list" :
                    myParameter = []
                    for i in range(2,len(line)) :
                        myParameter.append(line[i])
                    cycles[currentCycle][line[0]] = myParameter
                else :
                    cycles[currentCycle][line[0]] = line[2]
                if line[0] == "pop_list" :
                    connections[currentCycle] = myParameter
            elif check_sim == 1 and line[0] != "#" :
                simulation_parameters[line[0]] = line[2]

    fic.close()
    return populations,cycles,simulation_parameters,connections


def write_parameters(name_file,network) :
    ### writes a file with the input parameters
    # creates a file following the same format as default_parameters.txt

    for compartment in network.compartments.values() :
        name_file.write(compartment.save_parameters())
    name_file.write(network.save_parameters())

    name_file.close()

    print("Parameters have been saved under",name_file.name)
