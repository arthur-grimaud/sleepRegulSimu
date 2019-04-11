#!bin/Python3
#-*-coding:utf-8-*-

import numpy as np

data = np.loadtxt("results.txt")
f_W=data[0]
C_E=data[3]
C_A=data[4]
C_G=data[5]
h=data[6]

### creation of the list hypnogram
hypnogram=[]
for i in range(len(f_W)):
    if C_E[i] < 0.4 :
        hypnogram.append(0.5)
    elif C_A[i] > 0.4 :
        hypnogram.append(0)
    else : 
        hypnogram.append(1)

# save the data
np.savetxt("hypnogram.txt",hypnogram)