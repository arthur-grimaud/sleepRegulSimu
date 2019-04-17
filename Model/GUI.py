import numpy as np
from tkinter import *
from graphviz import Digraph

class NetworkGUI:

    #---------------Display Compartements Parametiers-----------------------

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
            else:
                i += 1
                lbl = Label(compFrame, text=attr)
                lbl.grid(column=0, row=i)
                txt = Entry(compFrame, width=10)
                txt.insert(END, value)
                txt.grid(column=1, row=i)


        return compFrame


    #---------------Display Compartements Variables for Recorders  /!\ -----------------------

    def displayCompVar(self):
        window = Tk()
        var = 0
        cb = Checkbutton(window, text = "FiringRate", width = 20, variable=var, onvalue=["wake","F"], offvalue=0).grid(column=1, row=0)
        b = Button(window, text="Create Compartment", command=lambda: self.saveAndClose(var,window),width=25)
        b.grid(column=2, row=0)
        window.mainloop()

        # varToSave = [[]]
        #
        #
        # window = Tk()
        # i = 0
        #
        # for compKey, comp in self.compartments.items():
        #     #varToSave.append([])
        #     i += 1
        #     lbl = Label(window, text=comp.name)
        #     lbl.grid(column=0, row=i)
        #     cb = Checkbutton(window, text = "FiringRate", width = 20, variable=varToSave[0], onvalue=[str(compKey),"F"], offvalue=0)
        #     cb.grid(column=1, row=i)
        #     cb = Checkbutton(window, text = "Concentration", width = 20, variable=varToSave[0], onvalue=[str(compKey),"C"], offvalue=0)
        #     cb.grid(column=2, row=i)
        #
        # b = Button(window, text="Create Compartment", command=lambda: self.saveAndClose(varToSave,window),width=25)
        # b.grid(column=2, row=0)
        #
        # window.mainloop()



    def saveAndClose(self,param,window):
        self.results = param
        window.destroy()
        print(self.results)




    def getCreationWindow(self):   #Temporary implementation

        creaWin = Tk()

        i = 0

        for attr, value in self.compartments["NREM"].__dict__.items():
            i+=1
            lbl = Label(creaWin, text=attr)
            lbl.grid(column=0, row=i)
            txt = Entry(creaWin, width=10)
            txt.insert(END, "0")
            txt.grid(column=1, row=i)


        b = Button(creaWin, text="Create Compartment", command=lambda: self.CreateObjFromCreationWindow(creaWin),width=25).grid(column=2, row=0)

        creaWin.mainloop()


    def getCreationWindowConnect(self):   #Temporary implementation

        creaWin = Tk()

        #source
        lbl = Label(creaWin, text="source")
        lbl.grid(column=0, row=0)
        txt = Entry(creaWin, width=10)
        txt.insert(END, "0")
        txt.grid(column=1, row=0)
        #target
        lbl = Label(creaWin, text="target")
        lbl.grid(column=0, row=1)
        txt = Entry(creaWin, width=10)
        txt.insert(END, "0")
        txt.grid(column=1, row=1)
        #weight
        lbl = Label(creaWin, text="weight")
        lbl.grid(column=0, row=2)
        txt = Entry(creaWin, width=10)
        txt.insert(END, "0")
        txt.grid(column=1, row=2)
        #type
        lbl = Label(creaWin, text="type")
        lbl.grid(column=0, row=3)
        txt = Entry(creaWin, width=10)
        txt.insert(END, "0")
        txt.grid(column=1, row=3)


        b = Button(creaWin, text="Create Connection", command=lambda: self.CreateObjFromCreationWindowConnect(creaWin),width=25)
        b.grid(column=0, row=5)

        creaWin.mainloop()


    def CreateObjFromCreationWindow(self, window):   #Temporary implementation

        allWidgets = window.winfo_children() #get all widgets from the Object creation window
        popParam = {}
        for w in range(0, len(allWidgets)-2, 2):
            popParam[(allWidgets[w]['text'])] = allWidgets[w+1].get()
            print(allWidgets[w], allWidgets[w+1])
        self.addNP(popParam)

        window.destroy()


    def CreateObjFromCreationWindowConnect(self, window):   #Temporary implementation

        allWidgets = window.winfo_children() #get all widgets from the Object creation window
        popParam = {}
        for w in range(0, len(allWidgets)-1, 2):
            popParam[(allWidgets[w]['text'])] = allWidgets[w+1].get()
            print(allWidgets[w], allWidgets[w+1])
        self.addNP(popParam)

        window.destroy()




    def displayGraph(self):
        dot = Digraph()

        for cName in self.compartments .keys():
            dot.node(str(cName),str(cName))

        for cObj in self.compartments .values():
            for conn in cObj.connections:
                    if conn.weight < 0:
                        dot.edge(str(conn.source.name),str(conn.target.name), constraint='true',directed='false',arrowhead='tee')
                    if conn.weight > 0:
                        dot.edge(str(conn.source.name),str(conn.target.name), constraint='true',directed='false')

        dot.render('test-output.gv', view=True)
