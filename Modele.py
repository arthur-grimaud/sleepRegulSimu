import Sleep_Regulation as SR
import numpy as np
import utile
import ODE
import time



T = 30
res = 1E4
dt = 1E3/res
h = np.sqrt(dt)

SR_obj=SR.Sleep_Regulation()

start=time.time()
for i in range (0,int(T*res)):
    ODE.ODE(SR_obj,dt)
end=time.time()
temps=end-start
print("execution in ",temps," seconds")
