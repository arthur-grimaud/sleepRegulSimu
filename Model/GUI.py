#!bin/python
#-*-coding:utf-8-*-

# 05/12/19
# Authors: Darnige Eden / Grimaud Arthur / Amelie Gruel / Alexia Kuntz


#######################IMPORTATIONS########################

#Calculation
import numpy as np ### not necessary
#Gaphical interface
from tkinter import *
from tkinter import filedialog
#Graph generation
from graphviz import Digraph

from functools import partial
import os

class NetworkGUI:

    #---------------Display Compartement Parameters-----------------------
    def displayCompParam(self,window):

        i = 0
        objFrame = Frame (window)
        for comp in self.compartments.values():
            i += 1
            self.getCompartmentFrame(comp,objFrame).grid(column=i, row=0)








        return objFrame

    def getCompartmentFrame(self, comp, frame):

        i = 0
        compFrame = Frame (frame)

        lbl = Label(compFrame, text=comp.name)
        lbl.config(font=("Courier", 15))
        lbl.grid(column=0, row=0)

        def callback(attr, attrB):
            try:
                if attr == "F" or  attr =="C" or attr =="h":
                    comp.__dict__[attr] = [float(attrB.get()),0,0,0,0]
                elif attr == "beta":
                    print("beta")
                else:
                    comp.__dict__[attr] = float(attrB.get())
                print (attrB.get())
            except ValueError:
                print("Var set as str")
                comp.__dict__[attr] = str(attrB.get())
                print (attrB.get())


        def callbackW(weight, c):
            try:
                c.__dict__["weight"] = float(weight.get())
                print (weight.get())
                print("type(c.weight):",type(c.weight),c.weight)
            except ValueError:
                print("Var set as str")
                comp.__dict__[attr] = str(weight.get())
                print (weight.get())


        for attr, value in comp.__dict__.items():

            attrB = attr #making a copy of attr for trace


            attrB = StringVar()
            attrB.set(value)
            attrB.trace("w", lambda name, index, mode,attr=attr, attrB=attrB: callback(attr, attrB))


            if isinstance(value, list) and len(value) > 0 and attr == "connections": #If connection liste
                for c in value:


                    i += 1

                    weight = StringVar()
                    weight.set(c.weight)
                    weight.trace("w", lambda name, index, mode, weight=weight, c=c: callbackW(weight, c))

                    lbl = Label(compFrame, text="connection: ").grid(column=0, row=i)

                    lbl = Label(compFrame, text=c.source.name).grid(column=1, row=i)

                    lbl = Label(compFrame, text=c.target.name).grid(column=2, row=i)

                    e = Entry(compFrame, width=10)
                    # e.delete(0,END)
                    # e.insert(END, value)
                    e.config(textvariable=weight)
                    e.grid(column=3, row=i)


            elif attr == "name":
                i += 1
                lbl = Label(compFrame, text=attr)
                lbl.grid(column=0, row=i)
                txt = Entry(compFrame, width=10)
                txt.insert(END, value)
                txt.grid(column=1, row=i)
            elif attr == "promoting":
                i += 1
                lbl = Label(compFrame, text=attr)
                lbl.grid(column=0, row=i)
                txt = Entry(compFrame, width=10)
                txt.insert(END, value)
                txt.grid(column=1, row=i)
            elif attr == "F" or attr == "C" or attr == "h":
                i += 1
                lbl = Label(compFrame, text=attr)
                lbl.grid(column=0, row=i)
                txt = Entry(compFrame, width=10)
                txt.config(textvariable=attrB)
                txt.delete(0,END)
                txt.insert(END, value[0])
                txt.grid(column=1, row=i)
            else:
                i += 1
                lbl = Label(compFrame, text=attr)
                lbl.grid(column=0, row=i)
                txt = Entry(compFrame, width=10)
                txt.config(textvariable=attrB)
                txt.delete(0,END)
                txt.insert(END, value)
                txt.grid(column=1, row=i)

        #b = Button(compFrame, text="Apply changes", command=lambda: self.saveAndClose(var,window),width=25).grid(column=2, row=0)


        return compFrame

    #---------------Display simulation parameters---------------------------


    def getSimParamFrame(self, window):


        def callbackT(T):
            self.T = float(T.get())
            print (T.get())

        def callbackres(res):
            self.res = float(res.get())
            self.dt = 1E3/self.res
            print (res.get())

        def callbackSaveRate(saveRate):
            self.saveRate = float(saveRate.get())
            print (saveRate.get())

        def callbackMean(mean):
            self.mean = float(mean.get())
            print (mean.get())

        def callbackStd(std):
            self.std = float(std.get())
            print (std.get())

        T = StringVar()
        T.trace("w", lambda name, index, mode, T=T: callbackT(T))

        res = StringVar()
        res.trace("w", lambda name, index, mode, res=res: callbackres(res))

        saveRate = StringVar()
        saveRate.trace("w", lambda name, index, mode, saveRate=saveRate: callbackSaveRate(saveRate))

        mean = StringVar()
        mean.trace("w", lambda name, index, mode, mean=mean: callbackMean(mean))

        std = StringVar()
        std.trace("w", lambda name, index, mode, std=std: callbackStd(std))

        frame = Frame(window)

        resMethod = StringVar()
        optMethod = ["Euler", "RK4"]

        def changeMethod(new):
            resMethod = new
            print(resMethod)
            self.resMethod = new



        lbl = Label(frame, text="Select Resolution Method").grid(column=0, row=0)
        optMenu = OptionMenu(frame, resMethod, *optMethod, command=changeMethod).grid(column=1, row=0)


        lbl = Label(frame, text="T").grid(column=0, row=1)
        lbl = Label(frame, text="T (s)").grid(column=0, row=1)
        e = Entry(frame, textvariable=T)
        e.insert(END, self.T)
        e.grid(column=1, row=1)

        lbl = Label(frame, text="res (iterations/s)").grid(column=0, row=2)
        e = Entry(frame, textvariable=res)
        e.insert(END, self.res)
        e.grid(column=1, row=2)

        lbl = Label(frame, text="Save Rate (in Steps)").grid(column=0, row=3)
        e = Entry(frame, textvariable=saveRate)
        e.insert(END, self.saveRate)
        e.grid(column=1, row=3)

        lbl = Label(frame, text="Mean noise (Hz)").grid(column=0, row=4)
        e = Entry(frame, textvariable=mean)
        e.insert(END, self.mean)
        e.grid(column=1, row=4)

        lbl = Label(frame, text="Std noise (Hz)").grid(column=0, row=5)
        e = Entry(frame, textvariable=std)
        e.insert(END, self.std)
        e.grid(column=1, row=5)


        def callbackThresholdWake(std):
            self.wakeThreshold = float(std.get())
            print (std.get())

        thresholdWake = StringVar()
        thresholdWake.trace("w", lambda name, index, mode, thresholdWake=thresholdWake: callbackThresholdWake(thresholdWake))

        lbl = Label(frame, text="threshold Wake").grid(column=0, row=6)

        e = Entry(frame, textvariable=thresholdWake)
        e.insert(END, self.wakeThreshold)
        e.grid(column=1, row=6)


        def callbackThresholdREM(std):
            self.REMThreshold = float(std.get())
            print (std.get())

        thresholdREM = StringVar()
        thresholdREM.trace("w", lambda name, index, mode, thresholdREM=thresholdREM: callbackThresholdREM(thresholdREM))

        lbl = Label(frame, text="threshold REM").grid(column=0, row=7)

        e = Entry(frame, textvariable=thresholdREM)
        e.insert(END, self.REMThreshold)
        e.grid(column=1, row=7)

        return frame





    #---------------Display Compartement Variables for Recorders  /!\ -----------------------

    def displayCompVar(self):
        window = Tk()
        var = 0
        cb = Checkbutton(window, text = "FiringRate", width = 20, variable=var, onvalue=["wake","F"], offvalue=0).grid(column=1, row=0)
        b = Button(window, text="Create Compartment", command=lambda: self.saveAndClose(var,window),width=25)
        b.grid(column=2, row=0)
        window.mainloop()


    def saveAndClose(self,param,window):
        self.results = param
        window.destroy()
        print(self.results)

    #-----------Display window for the creation of new compartment/connection------------

    def addObjToModel(self, network):

        window = Tk()
        options = ["Neuronal Population", "Homeostatic Sleep Drive", "Connection"]
        var = StringVar()
        optMenu = OptionMenu(window, var, *options, command=lambda naz: self.getCreateObjFrame(naz, window, optMenu, network).grid(column=3, row=4))
        optMenu.place(x=10, y=10)

    def getCreateObjFrame(self, selection, window, optMenu, network):
        frame = Frame (window)
        if selection == "Neuronal Population":

            lbl = Label(frame, text="name").grid(column=0, row=0)
            ety = Entry(frame, width=10).grid(column=1, row=0)

            lbl = Label(frame, text="F").grid(column=0, row=1)
            ety = Entry(frame, width=10).grid(column=1, row=1)

            lbl = Label(frame, text="C").grid(column=0, row=2)
            ety = Entry(frame, width=10).grid(column=1, row=2)

            lbl = Label(frame, text="F_max").grid(column=0, row=3)
            ety = Entry(frame, width=10).grid(column=1, row=3)

            lbl = Label(frame, text="beta").grid(column=0, row=4)
            ety = Entry(frame, width=10).grid(column=1, row=4)

            lbl = Label(frame, text="alpha").grid(column=0, row=5)
            ety = Entry(frame, width=10).grid(column=1, row=5)

            lbl = Label(frame, text="tau_pop").grid(column=0, row=6)
            ety = Entry(frame, width=10).grid(column=1, row=6)

            lbl = Label(frame, text="neurotransmitter").grid(column=0, row=7)
            ety = Entry(frame, width=10).grid(column=1, row=7)

            lbl = Label(frame, text="gamma").grid(column=0, row=8)
            ety = Entry(frame, width=10).grid(column=1, row=8)

            lbl = Label(frame, text="tau_NT").grid(column=0, row=9)
            ety = Entry(frame, width=10).grid(column=1, row=9)

            lbl = Label(frame, text="promoting").grid(column=0, row=10)
            ety = Entry(frame, width=10).grid(column=1, row=10)

            b = Button(frame, text="Create", command=lambda: self.readAndCreateComp(frame, window, "NP"),width=25).grid(column=0, row=11)

        if selection == "Homeostatic Sleep Drive":

            lbl = Label(frame, text="h").grid(column=0, row=0)
            ety = Entry(frame, width=10).grid(column=1, row=0)

            lbl = Label(frame, text="H_max").grid(column=0, row=1)
            ety = Entry(frame, width=10).grid(column=1, row=1)

            lbl = Label(frame, text="tau_hw").grid(column=0, row=2)
            ety = Entry(frame, width=10).grid(column=1, row=2)

            lbl = Label(frame, text="tau_hs").grid(column=0, row=3)
            ety = Entry(frame, width=10).grid(column=1, row=3)

            lbl = Label(frame, text="theta_X").grid(column=0, row=4)
            ety = Entry(frame, width=10).grid(column=1, row=4)

            b = Button(frame, text="Create", command=lambda: self.readAndCreateComp(frame, window, "HSD"),width=25).grid(column=0, row=10)

        if selection == "Connection":

            compsNames = []
            target = StringVar()
            source = StringVar()
            type = StringVar()
            weightVal = 0

            def changeTarget(new):
                target = new
                print(target)

            def changeSource(new):
                source = new
                print(source)

            def changeType(new):
                type = new
                print(type)

            for c in self.compartments.keys():
                compsNames.append(c)

            types = ["NP-NP","HSD-NP","NP-HSD"]

            lbl = Label(frame, text="Select Connection Type").grid(column=0, row=0)
            optMenu = OptionMenu(frame, target, *types, command=changeType).grid(column=1, row=0)

            lbl = Label(frame, text="Select Source Compartment").grid(column=0, row=1)
            optMenu = OptionMenu(frame, source, *compsNames, command=changeSource).grid(column=1, row=1)

            lbl = Label(frame, text="Select Target Compartment").grid(column=0, row=2)
            optMenu = OptionMenu(frame, target, *compsNames, command=changeTarget).grid(column=1, row=2)

            lbl = Label(frame, text="theta_X").grid(column=0, row=3)
            e = Entry(frame)
            e.grid(column=1, row=3)

            b = Button(frame, text="Create", command=lambda: self.addNPConnection(type.get(), source.get(), target.get(), e.get() ),width=25).grid(column=0, row=4)
            #b = Button(frame, text="Create", command=lambda: self.getEntry(frame) ,width=25).grid(column=0, row=4)

        return frame

    def readAndCreateComp(self,frame,window,compType):

        allWidgets = frame.winfo_children() #get all widgets from the Object creation window
        compParam = {}
        for w in range(0, len(allWidgets)-1, 2):
            compParam[(allWidgets[w]['text'])] = allWidgets[w+1].get()
            print(allWidgets[w], allWidgets[w+1])

        if compType == "NP":
            self.addNP(compParam)
        elif compType == "HSD":
            self.addHSD(compParam)

        window.destroy()

    # def getEntry(self, frame):
    #     allWidgets = frame.winfo_children()
    #     for w in  range(len(allWidgets)):
    #         print(allWidgets[w])
    #         if isinstance(allWidgets[w], Entry):
    #             a = str(allWidgets[w].get())
    #             return a.get()  ####PROBLEM:return as stringvar type but is a string##### :o(

    #------------------------------Injection settings---------------------------------------

    def getInjectionCreationWindow(self):

        window = Tk()


        connAvailable = []
        connAvailableStr = []
        connStr = StringVar()
        injType = StringVar()

        optType = ["Agonist", "Antagonist"]

        def changeConn(new):

            connStr = new
            print(connStr, "type", type(connStr))

        def changeInjType(new):
            injType = new
            print(injType)

        def getConnObject(name):
            print("return:::", connAvailable[connAvailableStr.index(name)], "type", type(connAvailable[connAvailableStr.index(name)]))
            return connAvailable[connAvailableStr.index(name)]


        for c in self.compartments.values():
            for i in c.connections:
                if i.type == "NP-NP":
                    connAvailableStr.append("Injection of: "+str(i.source.neurotransmitter)+" in "+str(i.target.name))
                    connAvailable.append(i)


        lbl = Label(window, text="Select Injection").grid(column=0, row=0)
        optMenu = OptionMenu(window, connStr, *connAvailableStr, command=changeConn).grid(column=1, row=0)

        lbl = Label(window, text="P0").grid(column=0, row=1)
        e1 = Entry(window)
        e1.grid(column=1, row=1)

        lbl = Label(window, text="TauInj").grid(column=0, row=2)
        e2 = Entry(window)
        e2.grid(column=1, row=2)

        lbl = Label(window, text="iMin").grid(column=0, row=3)
        e3 = Entry(window)
        e3.grid(column=1, row=3)

        lbl = Label(window, text="iMax").grid(column=0, row=4)
        e4 = Entry(window)
        e4.grid(column=1, row=4)

        lbl = Label(window, text="Select Injection").grid(column=0, row=5)
        optMenu = OptionMenu(window, injType, *optType, command=changeInjType).grid(column=1, row=5)

        print(e1.get())
        print(e2.get())
        print(e3.get())
        print(e4.get())

        b = Button(window, text="Create", command=lambda: self.addInjection(getConnObject(connStr.get()), e1.get(), e2.get(), e3.get(), e4.get(), injType.get() ),width=25).grid(column=0, row=6)

        window.mainloop()


    #------------------------------Graph generation-----------------------------------------

    def displayGraph(self):
        dot = Digraph()

        for cName in self.compartments .keys():
            dot.node(str(cName),str(cName))

        for cObj in self.compartments .values():
            for conn in cObj.connections:
                    if conn.weight < 0:
                        dot.edge(str(conn.source.name),str(conn.target.name), constraint='true',directed='false',arrowhead='tee')
                    if conn.weight >= 0:
                        dot.edge(str(conn.source.name),str(conn.target.name), constraint='true',directed='false')

        dot.render('Network-Graph.gv', view=True)


    #------------------------------Save the results-----------------------------------------

    def getResults(self) :
        self.runSim()
        self.writeInFile(filedialog.asksaveasfile(title="Save as", initialdir=os.getcwd(), mode="w", defaultextension=".csv"),self.results)
