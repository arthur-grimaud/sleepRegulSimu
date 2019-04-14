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
h=data[6]

hypnogram=np.loadtxt("hypnogram.txt")

### creation of the time list
time = range(1,6)

# plot
plt.figure(1)
sub=plt.subplot(211)
sub=plt.plot(time,f_W,'g',label="F_W")    
sub=plt.plot(time,f_N,'r',label="F_N")
sub=plt.plot(time,f_R,'b',label="F_R")
sub=plt.plot(time,h,'y',label="h")
plt.xlim(1,5)
plt.ylim(0,7)
plt.xlabel('Time (h)')
plt.ylabel('Activity (Hz)')
plt.legend(loc='best')
plt.subplot(212)
plt.plot(time,hypnogram,'black')
plt.ylim(-0.5,1.5)
plt.xlabel('Time (h)')
plt.ylabel('Hypnogramme')
# plt.setp([0,0.5,1],'yticklabel',{'REM','NREM','wake'})
plt.show()