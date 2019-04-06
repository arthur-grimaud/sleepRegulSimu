import numpy as np



#-------------Constants---------------

tau_W = 1500E3
tau_N = 600E3
tau_R = 60E3

tau_E = 25E3
tau_G = 10E3
tau_A = 10E3

F_W_max	= 6.5
F_N_max	= 5.
F_R_max	= 5.

alpha_W	= 0.5
alpha_N	= 0.175
alpha_R	= 0.13

beta_W	= -0.4
# beta_N	= kappa * h(t)
beta_R	= -0.9

gamma_E	= 5.0
gamma_G	= 4.0
gamma_A	= 2.0


g_GW = -1.68
g_AW = 1.0
g_GR = -1.3
g_AR = 1.6
g_ER = -4.0
g_EN = -2.0

H_max		= 1.0
theta_W		= 2.0
tau_hw		= 34830E3
tau_hs		= 30600E3
kappa		= 1.5

time = [6.0]

f_W	= [6.0]
f_N	= [1E-3]
f_R	= [1E-3]
C_E	= [0.9]
C_G	= [1E-3]
C_A	= [1E-3]
h = [0.5]





t = 0

T = 30
res = 1E4
dt 	= 1E3/res
# h	= np.sqrt(dt)

# def FiringRate(F_x_max,I_x,beta_x,alpha_x):
#     return F_x_max*0.5(1 + np.tanh((I_x - beta_x)/alpha_x))
#
# def NTConcentration():
#     return np.tanh(f_x/gamma_x) - C_x)/tau_x


def Heaviside(X):
  if(X >= 0):
      return 1
  else:
      return 0



def I_W():
    return g_GW * C_G[-1] + g_AW * C_A[-1]
def I_N():
    return g_EN * C_E[-1]
def I_R():
    return g_ER * C_E[-1] + g_GR * C_G[-1] + g_AR * C_A[-1]


while (t < T*res):
    t+=1
    time.append(t)
    f_W.append(f_W[-1]+dt*(F_W_max *(0.5*(1 + np.tanh(((g_GW * C_G[-1] + g_AW * C_A[-1]) - beta_W)/alpha_W))) - f_W[-1])/tau_W)
    f_N.append(f_N[-1]+dt*(F_N_max *(0.5*(1 + np.tanh(((g_EN * C_E[-1]) + kappa*h[-1])/alpha_N))) - f_N[-1])/tau_N)
    f_R.append(f_R[-1]+dt*(F_R_max *(0.5*(1 + np.tanh(((g_ER * C_E[-1] + g_GR * C_G[-1] + g_AR * C_A[-1]) - beta_R)/alpha_R))) - f_R[-1])/tau_R)

    C_E.append(C_E[-1]+dt*(np.tanh((f_W[-1]/gamma_E) - C_E[-1])/tau_E))
    C_G.append(C_G[-1]+dt*(np.tanh((f_N[-1]/gamma_G) - C_G[-1])/tau_G))
    C_A.append(C_A[-1]+dt*(np.tanh((f_R[-1]/gamma_A) - C_A[-1])/tau_A))

    h.append(h[-1]+dt*((H_max-h[-1])/tau_hw*Heaviside(f_W[-1]-theta_W) - h[-1]/tau_hs*Heaviside(theta_W-f_W[-1])))



def saveInTxt():
    file=open("resultEulerSR.txt","w")
    file.write("time f_W f_N f_R C_E C_G C_A\n")
    for i in range(len(time)):
        file.write(str(time[i]) + " " + str(f_W[i]) + " " + str(f_N[i]) + " " + str(f_R[i]) +  " " + str(C_E[i]) +  " " + str(C_G[i]) +  " " + str(C_A[i]) + "\n")



saveInTxt()
