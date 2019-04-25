#!bin/python
#-*-coding:utf-8-*-

#######################IMPORTATIONS########################

#Calculation
import numpy as np
#Gaphical interface
from tkinter import *
#Graph generation
from graphviz import Digraph

from functools import partial

class NetworkGUI:

    #---------------Display Compartements Parameters-----------------------
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

        for attr, value in comp.__dict__.items():

            if isinstance(value, list) and len(value) > 0 and attr == "connections": #Si liste de connection
                for c in value:
                    i += 1
                    lbl = Label(compFrame, text="connection: ")
                    lbl.grid(column=0, row=i)
                    txt = Entry(compFrame, width=10)
                    txt.insert(END, c.source.name)
                    txt.grid(column=1, row=i)
                    txt = Entry(compFrame, width=10)
                    txt.insert(END, c.target.name)
                    txt.grid(column=2, row=i)
                    txt = Entry(compFrame, width=10)
                    txt.insert(END, c.weight)
                    txt.grid(column=3, row=i)
            elif attr == "F" or attr == "C" or attr == "h":
                i += 1
                lbl = Label(compFrame, text=attr)
                lbl.grid(column=0, row=i)
                txt = Entry(compFrame, width=10)
                txt.insert(END, value[0])
                txt.grid(column=1, row=i)
            else:
                i += 1
                lbl = Label(compFrame, text=attr)
                lbl.grid(column=0, row=i)
                txt = Entry(compFrame, width=10)
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
            print (res.get())

        def callbackSaveRate(saveRate):
            self.saveRate = float(saveRate.get())
            print (saveRate.get())

        T = StringVar()
        T.trace("w", lambda name, index, mode, T=T: callbackT(T))

        res = StringVar()
        res.trace("w", lambda name, index, mode, res=res: callbackres(res))

        saveRate = StringVar()
        saveRate.trace("w", lambda name, index, mode, saveRate=saveRate: callbackSaveRate(saveRate))


        frame = Frame(window)

        lbl = Label(frame, text="T").grid(column=0, row=1)
        e = Entry(frame, textvariable=T)
        e.insert(END, self.T)
        e.grid(column=1, row=1)

        lbl = Label(frame, text="res").grid(column=0, row=2)
        e = Entry(frame, textvariable=res)
        e.insert(END, self.res)
        e.grid(column=1, row=2)

        lbl = Label(frame, text="Save Rate (in Steps)").grid(column=0, row=3)
        e = Entry(frame, textvariable=saveRate)
        e.insert(END, self.saveRate)
        e.grid(column=1, row=3)

        return frame




    #---------------Display Compartements Variables for Recorders  /!\ -----------------------

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

    #-----------Display window for the creation new compartment/connection------------

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

            lbl = Label(frame, text="concentration").grid(column=0, row=7)
            ety = Entry(frame, width=10).grid(column=1, row=7)

            lbl = Label(frame, text="gamma").grid(column=0, row=8)
            ety = Entry(frame, width=10).grid(column=1, row=8)

            lbl = Label(frame, text="tau_NT").grid(column=0, row=9)
            ety = Entry(frame, width=10).grid(column=1, row=9)

            b = Button(frame, text="Create", command=lambda: self.readAndCreateComp(frame, window, "NP"),width=25).grid(column=0, row=10)

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
        for w in range(0, len(allWidgets), 2):
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

        dot.render('test-output.gv', view=True)
