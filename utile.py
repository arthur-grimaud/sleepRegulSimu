#!/usr/bin/python3


def init(value):
    return [value, 0.0 ,0.0 ,0.0 ,0.0]


def heaviside(X):
    if X>=0 :
        return 1.0
    return 0.0

def add_RK (RK_list) :
    RK_list[0] = (-3*RK_list[0] + 2*RK_list[1] + 4*RK_list[2] + 2*RK_list[3] + RK_list[4])/6
