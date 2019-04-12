#!bin/python
#-*-coding:utf-8-*-

def read_parameters() :
    ### reads the file parameters.txt and extract parameters from it
    # returns a list of dictionnaries of dictionnaries : [populations,concentrations,cycles,time]

    fic = open("default_parameters.txt","r")
    content = fic.read().split("\n")

    populations = {}
    concentrations = {}
    cycles = {}
    simulation_parameters = {}

    connections = {}

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
                populations[currentPopulation]["name"] = currentPopulation
            elif line[0] == "*" and check_pop == 1 :
                check_pop = 0
            elif line[0] == "@" and check_conc == 0 :
                check_conc = 1
                currentConcentration = line[3]
                concentrations[currentConcentration] = {}
                concentrations[currentConcentration]["name"] = currentConcentration
            elif line[0] == "@" and check_conc == 1 : 
                check_conc = 0
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
            
            elif check_pop == 1 and line[0] != "*" :
                if line[0] == "g" or line[0] == "pop_ext" or line[0] == "beta" :
                    myParameter = []
                    for i in range(2,len(line)) :
                        myParameter.append(line[i])
                    populations[currentPopulation][line[0]] = myParameter
                else :
                    populations[currentPopulation][line[0]] = line[2]
                if line[0] == "pop_ext" :
                    connections[currentPopulation] = myParameter
            elif check_conc == 1 and line[0] != "@" :
                concentrations[currentConcentration][line[0]] = line[2]
            elif check_cycle == 1 and line[0] != "+" :
                cycles[currentCycle][line[0]] = line[2]
            elif check_sim == 1 and line[0] != "#" :
                simulation_parameters[line[0]] = line[2]

    fic.close()
    return populations,concentrations,cycles,simulation_parameters,connections


def write_parameters(name_file,modele) :
    ### writes a file with the input parameters
    # creates a file following the same format as default_parameters.txt

    fic = open(name_file,"w")

    for myPop in modele['populations'] :
        fic.write("* population = "+myPop.name+"\n")
        myConcentration = {}
        myConcentration["population"] = myPop.name
        for parameter in vars(myPop) :
            print(getattr(myPop,parameter))
            if parameter in ["concentration","C","gamma","tau_NT"]:
                myConcentration[parameter]=getattr(myPop,parameter)
            else :
                if isinstance(getattr(myPop,parameter),list) :
                    fic.write(parameter+" =")
                    for value in getattr(myPop,parameter) :
                        fic.write(" "+value)
                    fic.write("\n")
                elif parameter != 'name' : 
                    fic.write(parameter+" = "+getattr(myPop,parameter)+"\n")
        fic.write("*\n\n")

        fic.write("@ concentration = "+myConcentration["concentration"]+"\n")
        for parameter in myConcentration : 
            if parameter != 'concentration':
                fic.write(parameter+" = "+myConcentration[parameter]+"\n")
        fic.write("@\n\n")

    for myCycle in modele['cycles'] : 
        fic.write("+ cycle = "+myCycle.name+"\n")
        for parameter in vars(myCycle) :
            fic.write(parameter+" = "+getattr(myCycle,parameter)+"\n")
        fic.write("+\n\n")
    
    fic.write("#\n")
    for parameter in modele['simulation_parameters'] :
        fic.write(parameter+" = "+modele['simulation_parameters'][parameter]+"\n")
    fic.write("#\n")

    fic.close()

# print("populations :")
# for pop in populations :
#     print '\t',pop,":"
#     for param in populations[pop] :
#         print "\t\t",param,populations[pop][param]
