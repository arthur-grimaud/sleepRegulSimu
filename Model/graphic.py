#!bin/python
#-*-coding:utf-8-*-

import tkinter as tk
import matplotlib.pyplot as plt
from pylab import xticks
from pylab import yticks
import csv
import statistics

### If user is on Mac ###
from sys import platform as sys_pf
if sys_pf == 'darwin':
    import matplotlib
    matplotlib.use("TkAgg")

### Choose what to display ###

def whatToDisplay() :
    window = tk.Tk()
    window.title("Select what to display")

    choice_F = tk.IntVar(window)
    button_F = tk.Checkbutton(window, text="Firing rates", variable=choice_F)
    button_F.grid(row=0,column=0)
    button_F.select()
    
    choice_C = tk.IntVar(window)
    button_C = tk.Checkbutton(window, text="Concentrations", variable=choice_C)
    button_C.grid(row=1,column=0)
    button_C.select()

    choice_homeo = tk.IntVar(window)
    button_homeo = tk.Checkbutton(window, text="Homeostatic sleep drive", variable=choice_homeo)
    button_homeo.grid(row=2,column=0)
    button_homeo.select()

    choice_hypno = tk.IntVar(window)
    button_hypno = tk.Checkbutton(window, text="Hypnogram", variable=choice_hypno)
    button_hypno.grid(row=3,column=0)
    button_hypno.select()

    tk.Button(window,text="Done",command=window.quit).grid(column=0,row=4)

    window.mainloop()

    to_display = []
    if choice_F.get() == 1 :
        to_display.append("F")
    if choice_C.get() == 1 :
        to_display.append("C")
    if choice_homeo.get() == 1 :
        to_display.append("homeo")
    if choice_hypno.get() == 1 :
        to_display.append("hypno")

    return to_display


### Transform the data in order to use a more flexible createGraph() function ###

def transformData(data,option) : 
    new_data = {}
    new_data["firing rates"] = {}
    new_data["concentrations"] = {}
    if option == 'stdev' :
        for a in ['stdev min','stdev max'] :
            new_data[a] = {}
            for b in ['firing rates','concentrations'] :
                new_data[a][b] = {}

    for (variable,values) in data.items() :
        if variable[-2:] == "_F" :
            new_data["firing rates"][variable[:-2]] = values
        elif variable[-2:] == "_C" :
            new_data["concentrations"][variable[:-2]] = values

        elif variable[-10:] == '_stdev_min' :
            if variable[-12:-10] == "_F" :
                new_data['stdev min']["firing rates"][variable[:-12]] = values
            elif variable[-12:-10] == "_C" :
                new_data['stdev min']["concentrations"][variable[:-12]] = values
        elif variable[-10:] == '_stdev_max' :
            if variable[-12:-10] == "_F" :
                new_data['stdev max']["firing rates"][variable[:-12]] = values
            elif variable[-12:-10] == "_C" :
                new_data['stdev max']["concentrations"][variable[:-12]] = values

        elif variable == "time" or variable == "homeostatic" or variable == "hypnogram":
            new_data[variable] = values
    
    return new_data

### Create the graph ###

def createGraph(data,option=0):

    to_display = whatToDisplay()
    print("to display : ",to_display)
    
    ### defines the corresponding colors for the 3 populations model
    colors = {
        'wake' : 'g', 
        'NREM' : 'r',
        'REM' : 'b',
        'homeostatic' : 'y',
        'hypnogram' : 'black'
    }
    data = transformData(data,option)

    step_hour = 5
    time_ms = []
    time_h = []
    for t in range(int(data['time'][-1])) :
        if t % (60*60*step_hour) == 0 :
            time_ms.append(t)
            time_h.append(int(t/(60*60)))

    plt.figure(1)

    ### subplot 1 - firing rates 
    if 'F' in to_display :
        sub1=plt.subplot(3,1,1)
        for (fr,values) in data["firing rates"].items() :
            sub1=plt.plot(data['time'], values, colors[fr], label=fr)

        # show the standard deviation on the mean graphs
        if option == 'stdev' :
            for stdev in ['stdev min','stdev max'] :
                for (fr, values) in data[stdev]["firing rates"].items() :
                    sub1=plt.plot(data['time'], values, colors[fr], linewidth=0.5)

        xticks(time_ms,time_h)
        plt.ylabel('Activity (Hz)')
        plt.legend(loc='best')


    ### subplot 2 - concentrations
    if 'C' in to_display or 'homeo' in to_display:
        sub2=plt.subplot(3,1,2)
        if 'C' in to_display :
            for (c,values) in data["concentrations"].items() :
                sub2=plt.plot(data['time'], values, colors[c], label=c)
        if 'homeo' in to_display :
            sub2=plt.plot(data['time'],data['homeostatic'],colors['homeostatic'],label="homeostatic")
        xticks(time_ms,time_h)
            
        # show the standard deviation on the mean graphs
        if option == 'stdev' :
            for stdev in ['stdev min','stdev max'] :
                for (c,values) in data[stdev]["concentrations"].items() :
                    sub2=plt.plot(data['time'], values, colors[c], linewidth=0.5)

        plt.ylabel("Concentrations")
        plt.legend(loc='best')


    ### subplot 3 - hypnogram 
    if 'hypno' in to_display :
        sub3=plt.subplot(3,1,3)
        plt.plot(data['time'],data['hypnogram'], colors['hypnogram'])
        plt.ylim(-0.5,1.5)
        xticks(time_ms,time_h)
        yticks([0,0.5,1],['NREM','REM','Wake'])
        plt.xlabel('Time (h)')
        plt.ylabel('Hypnogram')
   
    plt.show()


### Read from a CVS file ###

def readCSV(file) :
    tmp = open(file,'r')
    names=tmp.readline().rsplit()
    tmp.close()
    
    results={}
    for n in names : 
        results[n]=[]

    with open(file) as f:
        reader = csv.DictReader(f, delimiter='\t')
        for row in reader :
            for (name,element) in row.items() :
                results[name].append(float(element))
    return results

def GraphFromCSV(file) :
    data = readCSV(file)
    createGraph(data)


### Read from the simulation ###

def GraphFromSim(sim):
    data = {}
    for var in sim : 
        data[var[0]] = var[1:]
    createGraph(data)


#########################################################################################################

### create mean graphs ###

def createMeanGraphs(files) :
    results = []
    for file in files :
        results.append(readCSV(file)) 

    ### user chooses whether to use show standard deviation or no
    window_stdev = tk.Tk()
    window_stdev.title("Display the standard deviation ?")
    standard_deviation = tk.StringVar(window_stdev)
    tk.Radiobutton(window_stdev,  text="Yes", value="yes", variable=standard_deviation,width=45).pack()
    tk.Radiobutton(window_stdev,  text="No", value="no", variable=standard_deviation,width=45).pack()
    tk.Button(window_stdev,text="Done",command=window_stdev.quit).pack()
    window_stdev.mainloop()

    mean_data = {}
    stat = {}
    for element in results[0] :
        if element != 'hypnogram' :
            mean_data[element] = []
            stat[element] = []

    for element in mean_data :
        for i in range(len(results[0][element])) : 
            stat_tmp = []
            for fic in results :
                stat_tmp.append(fic[element][i])    
            stat[element].append(stat_tmp)
        for l in stat[element] :
            tmp = 0
            for val in l :
                tmp += val
            tmp /= len(l)
            mean_data[element].append(tmp)
    
    if standard_deviation.get() == 'yes' :
        for (variable,values) in stat.items() : 
            if variable != 'homeostatic' :
                mean_data[variable+'_stdev_min'] = []
                mean_data[variable+'_stdev_max'] = []
                for k in range(len(values)) : 
                    stdev = statistics.stdev(values[k])
                    mean_data[variable+'_stdev_min'].append(mean_data[variable][k]-stdev)
                    mean_data[variable+'_stdev_max'].append(mean_data[variable][k]+stdev)
    
    mean_data['hypnogram'] = []
    for i in range(len(mean_data['time'])):
        if mean_data['wake_C'][i] < 0.4 :
            if mean_data['REM_C'][i] > 0.4 :
                mean_data['hypnogram'].append(0.5)
            else :
                mean_data['hypnogram'].append(0)
        else : 
            mean_data['hypnogram'].append(1)
    
    if standard_deviation.get() == 'yes' :
        createGraph(mean_data,'stdev')
    else : 
        createGraph(mean_data)


files = [
    {'time' : [1,2,8,5,9]},
    {'time' : [45,8,5,69,21]},
    {'time' : [7,58,45,62,14]},
    {'time' : [5,12,48,35,65]},
    {'time' : [64,56,21,47,85]}
]

# createMeanGraphs(files)