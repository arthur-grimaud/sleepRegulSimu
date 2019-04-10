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
                populations[currentPopulation][line[0]] = line[2]
            elif check_conc == 1 and line[0] != "@" :
                concentrations[currentConcentration][line[0]] = line[2]
            elif check_cycle == 1 and line[0] != "+" :
                cycles[currentCycle][line[0]] = line[2]
            elif check_sim == 1 and line[0] != "#" :
                simulation_parameters[line[0]] = line[2]

    fic.close()
    return populations,concentrations,cycles,simulation_parameters

# print("populations :")
# for pop in populations :
#     print ('\t',pop,":")
#     for param in populations[pop] :
#         print("\t\t",param,populations[pop][param]) 


def write_parameters(name_file,populations,concentrations,cycles,simulation_parameters) :
    ### writes a file with the input parameters
    # creates a file following the same format as default_parameters.txt

    fic = open(name_file,"w")

    for myPop in populations :
        fic.write("* population = "+myPop+"\n")
        for parameter in populations[myPop] :
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


# def setClasses() 


# création de classes pour chaque objet 


##### MAIN #####
populations,concentrations,cycles,simulation_parameters = read_parameters()
write_parameters("test.txt",populations,concentrations,cycles,simulation_parameters)
