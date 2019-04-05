
import Sleep_Regulation as SR

def ODE(SR_obj,dt) :
    for i in range(0,4):
        SR_obj.set_RK(i,dt)

    SR_obj.add_RK()
