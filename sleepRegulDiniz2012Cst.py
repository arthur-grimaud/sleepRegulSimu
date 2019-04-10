import numpy as np
import matplotlib.pyplot as plt


#-------------Constants---------------

tau_W = 25
tau_N = 10
tau_R = 1

tau_E = 25E3
tau_G = 10E3
tau_A = 10E3

F_W_max	= 6.5
F_N_max	= 5.
F_R_max	= 5.

alpha_W	= 0.5
alpha_N	= 0.25
alpha_R	= 0.25

beta_W	= -0.23
# beta_N	= kappa * h(t)
beta_R	= -0.6

gamma_E	= 5.0
gamma_G	= 4.0
gamma_A	= 3.0


g_GW = -2
g_AW = 1.2
g_GR = -1.3
g_AR = 1.5
g_ER = -2.1
g_EN = -2.0

H_max		= 1.0
theta_W		= 2.0
tau_hw		= 600
tau_hs		= 380
kappa		= 2.5

time = []

f_W_val	= []
f_N_val	= []
f_R_val	= []
C_E_val	= []
C_G_val	= []
C_A_val	= []
h_val = []


f_W	= 6.0
f_N	= 1E-3
f_R	= 1E-3
C_E	= 0.9
C_G	= 1E-3
C_A	= 1E-3
h = 0.5




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
    return g_GW * C_G   + g_AW * C_A
def I_N():
    return g_EN * C_E
def I_R():
    return g_ER * C_E   + g_GR * C_G   + g_AR * C_A


while (t < T*res):
    t+=1

    f_W=f_W +dt*(((F_W_max *(0.5*(1 + np.tanh((I_W() - beta_W)/alpha_W)))) - f_W  )/tau_W)
    f_N=f_N +dt*(((F_N_max *(0.5*(1 + np.tanh((I_N() + kappa*h  )/alpha_N)))) - f_N  )/tau_N)
    f_R=f_R +dt*(((F_R_max *(0.5*(1 + np.tanh((I_R() - beta_R)/alpha_R)))) - f_R  )/tau_R)

    C_E=C_E+dt*(np.tanh((f_W/gamma_E) - C_E)/tau_E)
    C_G=C_G+dt*(np.tanh((f_N/gamma_G) - C_G)/tau_G)
    C_A=C_A+dt*(np.tanh((f_R/gamma_A) - C_A)/tau_A)

    h = h+dt*((H_max-h)/tau_hw*Heaviside(f_W-theta_W) - h/tau_hs*Heaviside(theta_W-f_W))

    f_W_val.append(f_W)
    f_N_val.append(f_N)
    f_R_val.append(f_R)

    C_E_val.append(C_E)
    C_G_val.append(C_G)
    C_A_val.append(C_A)

    h_val.append(h)
    time.append(t)
    print(Heaviside(f_W-theta_W))
    print(f_N)


plt.plot(time,f_W_val)
plt.plot(time,f_N_val)
plt.plot(time,f_R_val)
plt.show()

plt.plot(time,_val)
plt.plot(time,f_N_val)
plt.plot(time,f_R_val)
plt.show()


def saveInTxt():
    file=open("resultEulerSR2.txt","w")
    file.write("time f_W f_N f_R C_E C_G C_A\n")
    for i in range(len(f_R_val)-10):
        file.write(str(time[i]) + " " + str(f_W_val[i]) + " " + str(f_N_val[i]) + " " + str(f_R_val[i]) +  " " + str(C_E_val[i]) +  " " + str(C_G_val[i]) +  " " + str(C_A_val[i]) + "\n")



saveInTxt()
