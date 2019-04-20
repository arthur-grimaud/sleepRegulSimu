#!bin/python
#-*-coding:utf-8-*-

import matplotlib.pyplot as plt 
import numpy as np
from mpl_toolkits.mplot3d import Axes3D

### get data
data = np.loadtxt("results.txt")
f_W=data[0]
f_N=data[1]
f_R=data[2]
C_E=data[3]
C_A=data[4]
C_G=data[5]
h=data[6]

hypnogram=np.loadtxt("hypnogram.txt")

### creation of the time list
time = range(1,6)

# plot
plt.figure(1)

sub1=plt.subplot(211)
plt.plot(time,hypnogram,'black')
plt.ylim(-0.5,1.5)
plt.xlabel('Time (h)')
plt.ylabel('Hypnogramme')

sub2=plt.subplot(212)
sub2=plt.plot(time,f_W,'g',label="F_W")    
sub2=plt.plot(time,f_N,'r',label="F_N")
sub2=plt.plot(time,f_R,'b',label="F_R")
sub2=plt.plot(time,h,'y',label="h")
plt.ylim(0,7)
plt.xlabel('Time (h)')
plt.ylabel('Activity (Hz)')
plt.legend(loc='best')
# plt.setp([0,0.5,1],'yticklabel',{'REM','NREM','wake'})

sub3=plt.subplot(213)
sub3=plt.plot(time,C_E,'g',label="C_E")
sub3=plt.plot(time,C_G,'r',label="C_G")
sub3=plt.plot(time,C_A,'b',label="C_A")
plt.ylim(0,1)
plt.xlabel("Time (h)")
plt.ylabel("Concentrations")
plt.legend(loc='best')

plt.show()