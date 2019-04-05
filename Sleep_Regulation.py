#!/usr/bin/python3

import numpy as np
import utile

class Sleep_Regulation :

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

    A = [0.5, 0.5, 1.0, 1.0]
    B = [0.75, 0.75, 0.0, 0.0]

    f_W	= utile.init(6.0)
    f_N	= utile.init(1E-3)
    f_R	= utile.init(1E-3)
    C_E	= utile.init(0.9)
    C_G	= utile.init(1E-3)
    C_A	= utile.init(1E-3)
    h = utile.init(0.5)



    def __init__(self):
        self.C_E = utile.init(np.tanh(Sleep_Regulation.f_W[0]/Sleep_Regulation.gamma_E))
        self.C_G = utile.init(np.tanh(Sleep_Regulation.f_N[0]/Sleep_Regulation.gamma_G))
        self.C_A = utile.init(np.tanh(Sleep_Regulation.f_R[0]/Sleep_Regulation.gamma_A))

    # def __init__(self,Par) :
    #     f_W=utile.init(Par[0])
    #     f_N=utile.init(Par[1])
    #     f_R=utile.init(Par[2])
    #     h=utile.init(Par[3])
    #
    #     self.C_E = utile.init(np.tanh(f_W[0]/Sleep_Regulation.gamma_E))
    #     self.C_G = utile.init(np.tanh(f_N[0]/Sleep_Regulation.gamma_G))
    #     self.C_A = utile.init(np.tanh(f_R[0]/Sleep_Regulation.gamma_A))

#####on peut remplacer les S_r par self.

    def set_RK(self,N,dt) :
        self.f_W	[N+1] = Sleep_Regulation.f_W [0] + Sleep_Regulation.A[N] * dt*(Sleep_Regulation.F_W_max *0.5*(1 + np.tanh((self.I_W(N) - Sleep_Regulation.beta_W)/Sleep_Regulation.alpha_W))     - Sleep_Regulation.f_W [N])/Sleep_Regulation.tau_W;
        self.f_N	[N+1] = Sleep_Regulation.f_N [0] + Sleep_Regulation.A[N] * dt*(Sleep_Regulation.F_N_max *0.5*(1 + np.tanh((self.I_N(N) + Sleep_Regulation.kappa*Sleep_Regulation.h[N])/Sleep_Regulation.alpha_N)) - Sleep_Regulation.f_N [N])/Sleep_Regulation.tau_N;
        self.f_R	[N+1] = Sleep_Regulation.f_R [0] + Sleep_Regulation.A[N] * dt*(Sleep_Regulation.F_R_max *0.5*(1 + np.tanh((self.I_R(N) - Sleep_Regulation.beta_R)/Sleep_Regulation.alpha_R))     - Sleep_Regulation.f_R [N])/Sleep_Regulation.tau_R;
        self.C_E [N+1] = Sleep_Regulation.C_E [0] + Sleep_Regulation.A[N] * dt*(np.tanh(Sleep_Regulation.f_W[N+1]/Sleep_Regulation.gamma_E) - Sleep_Regulation.C_E[N])/Sleep_Regulation.tau_E;
        self.C_A [N+1] = Sleep_Regulation.C_A [0] + Sleep_Regulation.A[N] * dt*(np.tanh(Sleep_Regulation.f_R[N+1]/Sleep_Regulation.gamma_A) - Sleep_Regulation.C_A[N])/Sleep_Regulation.tau_A;
        self.C_G [N+1] = Sleep_Regulation.C_G [0] + Sleep_Regulation.A[N] * dt*(np.tanh(Sleep_Regulation.f_N[N+1]/Sleep_Regulation.gamma_G) - Sleep_Regulation.C_G[N])/Sleep_Regulation.tau_G;
        self.h	[N+1] = Sleep_Regulation.h	[0] + Sleep_Regulation.A[N] * dt*((Sleep_Regulation.H_max-Sleep_Regulation.h[N])/Sleep_Regulation.tau_hw*utile.heaviside(Sleep_Regulation.f_W[N]-Sleep_Regulation.theta_W) - Sleep_Regulation.h[N]/Sleep_Regulation.tau_hs*utile.heaviside(Sleep_Regulation.theta_W- Sleep_Regulation.f_W[N]));

    def I_W(self,N):
        return Sleep_Regulation.g_GW * Sleep_Regulation.C_G[N] + Sleep_Regulation.g_AW * Sleep_Regulation.C_A[N]

    def I_N(self,N):
        return Sleep_Regulation.g_EN * Sleep_Regulation.C_E[N]

    def I_R(self,N):
        return Sleep_Regulation.g_ER * Sleep_Regulation.C_E[N] + Sleep_Regulation.g_GR * Sleep_Regulation.C_G[N] + Sleep_Regulation.g_AR * Sleep_Regulation.C_A[N]

    def add_RK(self):
        utile.add_RK(Sleep_Regulation.f_W)
        utile.add_RK(Sleep_Regulation.f_N)
        utile.add_RK(Sleep_Regulation.f_R)
        utile.add_RK(Sleep_Regulation.C_E)
        utile.add_RK(Sleep_Regulation.C_G)
        utile.add_RK(Sleep_Regulation.C_A)
        utile.add_RK(Sleep_Regulation.h)
