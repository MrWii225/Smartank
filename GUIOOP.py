import tkinter as tk 
import tkinter.font as font
from tkinter.ttk import *
from time import strftime

class SmartankGUI(tk.Tk):
    
    def __init__(self):
        super().__init__()
        self.title("Smartank")
        self.geometry("1000x600")
        
        container = tk.Frame(self)
        container.pack(fill="both", expand=True)

        default_font = font.nametofont("TkDefaultFont")
        default_font.configure(size=20)
        
        self.frames = {}
        # , GoldfishData, GuppyData, ZebrafishData, TetraData, MinnowData, PeaPufferData, BarbData, SwordtailData, DwarfGouramiData
        for PageClass in (InitialPage, Fishionary, Options):
            page_name = PageClass.__name__
            frame = PageClass(parent=container, controller=self)
            self.frames[page_name] = frame 
            frame.grid(row=0, column=0, sticky="nsew") 
        
        self.show_frame("InitialPage")
    
    def show_frame(self, page_name:str):
        frame = self.frames[page_name]
        frame.tkraise() 

class InitialPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        tk.Label(self, text="Smartank", font = ("Arial",40)).pack(pady=10,anchor="center",expand=True)
        tk.Button(self, text="Options", command=lambda: controller.show_frame("Options")).pack()
        tk.Button(self, text="Fishionary", command=lambda: controller.show_frame("Fishionary")).pack(anchor="center")
        def time(): 
            string = strftime('%I:%M:%S %p') 
            lbl.config(text = string) 
            lbl.after(1000, time) 

        lbl = tk.Label(self, font = ('Times New Roman', 40)) 

        lbl.pack() 
        time() 

class Fishionary(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        tk.Label(self, text="Fishionary").grid(pady=10)
        tk.Button(self, text="Goldfish", command=lambda: controller.show_frame("GoldfishData")).grid(row=0, column=0)
        tk.Button(self, text="Guppy", command=lambda: controller.show_frame("GuppyData")).grid(row=1, column=0)
        tk.Button(self, text="Zebrafish", command=lambda: controller.show_frame("ZebrafishData")).grid(row=2, column=0)
        tk.Button(self, text="Tetra", command=lambda: controller.show_frame("TetraData")).grid(row=0, column=1)
        tk.Button(self, text="Minnow", command=lambda: controller.show_frame("MinnowData")).grid(row=1, column=1)
        tk.Button(self, text="Pea Puffer", command=lambda: controller.show_frame("PeaPufferData")).grid(row=2, column=1)
        tk.Button(self, text="Barb", command=lambda: controller.show_frame("BarbData")).grid(row=0, column=2)
        tk.Button(self, text="Swordtail", command=lambda: controller.show_frame("SwordtailData")).grid(row=1, column=2)
        tk.Button(self, text="Dwarf Gourami", command=lambda: controller.show_frame("DwarfGouramiData")).grid(row=2, column=2)
        tk.Button(self, text="Go Back", command=lambda: controller.show_frame("InitialPage")).grid(row=3, column= 1)

class Options(tk.Frame):
    def __init__(self,parent,controller):
        tk.Label(self, text="Options").pack()


smartankgui = SmartankGUI()
smartankgui.mainloop()
