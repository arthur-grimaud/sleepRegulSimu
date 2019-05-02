#!bin/python
#-*-coding:utf-8-*-

import tkinter as tk
import matplotlib.pyplot as plt
from pylab import xticks
from pylab import yticks
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import csv

### Choose what to display ###

# def whatToDisplay() :
#     window = tk.Tk()
#     window.title("Select what to display")

#     choice_F = tk.IntVar()
#     button_F = tk.Checkbutton(window, text="Firing rates", variable=choice_F)
#     button_F.grid(row=0,column=0)
#     button_F.select()
    
#     choice_C = tk.IntVar()
#     button_C = tk.Checkbutton(window, text="Concentrations", variable=choice_C)
#     button_C.grid(row=1,column=0)
#     button_C.select()

#     choice_homeo = tk.IntVar()
#     button_homeo = tk.Checkbutton(window, text="Homeostatic sleep drive", variable=choice_homeo)
#     button_homeo.grid(row=2,column=0)
#     button_homeo.select()

#     choice_hypno = tk.IntVar()
#     button_hypno = tk.Checkbutton(window, text="Hypnogram", variable=choice_hypno)
#     button_hypno.grid(row=3,column=0)
#     button_hypno.select()

#     tk.Button(window,text="Done",command=window.quit).grid(column=0,row=4)

#     window.mainloop()

#     to_display = []
#     if choice_F.get() == 1 :
#         to_display.append("F")
#     if choice_C.get() == 1 :
#         to_display.append("C")
#     if choice_homeo.get() == 1 :
#         to_display.append("homeo")
#     if choice_hypno.get() == 1 :
#         to_display.append("hypno")

#     return to_display


### Transform the data in order to use a more flexible createGraph() function ###

def transformData(data) : 
    new_data = {}
    new_data["firing rates"] = {}
    new_data["concentrations"] = {}

    for (variable,values) in data.items() :
        if variable[-2:] == "_F" :
            new_data["firing rates"][variable[:-2]] = values
        elif variable[-2:] == "_C" :
            new_data["concentrations"][variable[:-2]] = values
        elif variable == "time" or variable == "homeostatic" or variable == "hypnogram":
            new_data[variable] = values
    
    return new_data

### Create the graph ###

def createGraph(data):

    # to_display = whatToDisplay()
    # print("to display : ",to_display)
    
    ### defines the corresponding colors for the 3 populations model
    colors = {
        'wake' : 'g', 
        'NREM' : 'r',
        'REM' : 'b',
        'homeostatic' : 'y',
        'hypnogram' : 'black'
    }
    data = transformData(data)

    step_hour = 5
    time_ms = []
    time_h = []
    for t in range(int(data['time'][-1])) :
        if t % (60*60*step_hour) == 0 :
            time_ms.append(t)
            time_h.append(int(t/(60*60)))

    plt.figure(1)

    sub1=plt.subplot(3,1,1)
    for (fr,values) in data["firing rates"].items() :
        sub1=plt.plot(data['time'], values, colors[fr], label=fr)
    xticks(time_ms,time_h)
    plt.xlabel('Time (h)')
    plt.ylabel('Activity (Hz)')
    plt.legend(loc='best')

    sub2=plt.subplot(3,1,2)
    for (c,values) in data["concentrations"].items() :
        sub2=plt.plot(data['time'], values, colors[c], label=c)
    sub2=plt.plot(data['time'],data['homeostatic'],colors['homeostatic'],label="homeostatic")
    xticks(time_ms,time_h)
    plt.xlabel("Time (h)")
    plt.ylabel("Concentrations")
    plt.legend(loc='best')

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
                results[name].append(element)
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