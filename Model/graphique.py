#!bin/python
#-*-coding:utf-8-*-

import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D



def createGraph(network):

    # plot
    plt.figure(1)

    sub1=plt.subplot(3,1,1)
    plt.plot(network.results[0],network.results[1],'black')
    plt.ylim(-0.5,1.5)
    plt.xlabel('Time (h)')
    plt.ylabel('Hypnogramme')

    sub2=plt.subplot(3,1,2)
    sub2=plt.plot(network.results[0],network.results[2],'g',label="F_W")
    sub2=plt.plot(network.results[0],network.results[4],'r',label="F_N")
    sub2=plt.plot(network.results[0],network.results[6],'b',label="F_R")
    sub2=plt.plot(network.results[0],network.results[8],'y',label="h")
    plt.ylim(0,7)
    plt.xlabel('Time (h)')
    plt.ylabel('Activity (Hz)')
    plt.legend(loc='best')
    # plt.setp([0,0.5,1],'yticklabel',{'REM','NREM','wake'})

    sub3=plt.subplot(3,1,3)
    sub3=plt.plot(network.results[0],network.results[3],'g',label="C_E")
    sub3=plt.plot(network.results[0],network.results[5],'r',label="C_G")
    sub3=plt.plot(network.results[0],network.results[7],'b',label="C_A")
    plt.ylim(0,1)
    plt.xlabel("Time (h)")
    plt.ylabel("Concentrations")
    plt.legend(loc='best')

    plt.show()
