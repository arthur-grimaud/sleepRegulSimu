#!bin/python
#-*-coding:utf-8-*-

import matplotlib.pyplot as plt
from pylab import *
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import csv

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

def createGraph(data):
    
    step_hour = 5
    time_ms = []
    time_h = []
    for t in range(int(data['time'][-1])) :
        if t % (60*60*step_hour) == 0 :
            time_ms.append(t)
            time_h.append(int(t/(60*60)))

    # plot
    plt.figure(1)

    sub1=plt.subplot(3,1,1)
    plt.plot(data['time'],data['hypnogram'],'black')
    plt.ylim(-0.5,1.5)
    xticks(time_ms,time_h)
    yticks([0,0.5,1],['NREM','REM','Wake'])
    plt.xlabel('Time (h)')
    plt.ylabel('Hypnogram')

    sub2=plt.subplot(3,1,2)
    sub2=plt.plot(data['time'],data['wake_F'],'g',label="F_W")
    sub2=plt.plot(data['time'],data['NREM_F'],'r',label="F_N")
    sub2=plt.plot(data['time'],data['REM_F'],'b',label="F_R")
    plt.ylim(0,7)
    xticks(time_ms,time_h)
    plt.xlabel('Time (h)')
    plt.ylabel('Activity (Hz)')
    plt.legend(loc='best')

    sub3=plt.subplot(3,1,3)
    sub3=plt.plot(data['time'],data['wake_C'],'g',label="C_E")
    sub3=plt.plot(data['time'],data['NREM_C'],'r',label="C_G")
    sub3=plt.plot(data['time'],data['REM_C'],'b',label="C_A")
    sub3=plt.plot(data['time'],data['homeostatic'],'y',label="homeostatic")
    plt.ylim(0,1)
    xticks(time_ms,time_h)

    plt.xlabel("Time (h)")
    plt.ylabel("Concentrations")
    plt.legend(loc='best')

    plt.show()


def GraphFromCSV(file) :
    data = readCSV(file)
    createGraph(data)

def GraphFromSim(sim):
    data = {}
    for var in sim : 
        data[var[0]] = var[1:]
    createGraph(data)
    