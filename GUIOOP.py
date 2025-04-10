import tkinter as tk 
from tkinter import ttk
from dictionaries import *
from time import strftime

class SmartankGUI(tk.Tk):
    
    def __init__(self):
        super().__init__()
        self.title("Smartank")
        self.geometry("1000x600")
        
        container = tk.Frame(self)
        container.pack(fill="none", expand=True)
        
        self.frames = {}
        
        for PageClass in (InitialPage, Options, Display, Fishionary, Goldfish, Guppy, Zebrafish, Tetra, Minnow, PeaPuffer, Barb, Swordtail, DwarfGourami):
            page_name = PageClass.__name__
            frame = PageClass(parent=container, controller=self)
            self.frames[page_name] = frame 
            frame.grid(row=0, column=0, sticky="nsew") 
        
        self.show_frame("InitialPage")
    
    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise() 

class InitialPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        
        tk.Label(self, text="Smartank", font = ('Georgia', 50)).pack(padx=10, pady=15)
        tk.Label(self, text="- pH", font = ('Arial', 30)).pack(padx=10, pady=10)
        tk.Label(self, text="- F", font = ('Arial', 30)).pack(padx=10, pady=10)
        tk.Button(self, text="Fishionary",font=('Arial',16),width=30, height=3, command=lambda: controller.show_frame("Fishionary")).pack(pady=3)
        tk.Button(self,text="Options", font=('Arial',16),width=30, height=3, command=lambda:controller.show_frame("Options")).pack(pady=3)

        def time(): 
            string = strftime('%I:%M:%S %p') 
            lbl.config(text = string) 
            lbl.after(1000, time) 
        lbl= tk.Label(self, font = ('Arial', 40)) 


        lbl.pack(pady=5) 
        time() 

class Options(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        tk.Button(self,text="Go Back", font=(20),width=10, height=1,command=lambda: controller.show_frame("InitialPage")).pack(pady=3)
        tk.Button(self,text="Display", font=('Arial',16),width=30, height=3,command=lambda: controller.show_frame("Display")).pack(pady=3)
        tk.Button(self,text="Autofeeder", font=('Arial',16),width=30, height=3,command=lambda: controller.show_frame("InitialPage")).pack(pady=3)

class Display(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        tk.Button(self,text="Go Back", font=(20),width=10, height=1,command=lambda: controller.show_frame("Options")).pack(pady=6)

class Fishionary(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        
        # Configuring grid
        for i in range(5):
            self.grid_columnconfigure(i, weight=1)
        for i in range(5):
            self.grid_rowconfigure(i, weight=1)
            
        # label
        tk.Label(self,text="Fishionary", font=("Arial", 24, "bold")).grid(row=0, column=0, columnspan=5, pady=20)   
        
        # Data Buttons
        data_buttons = [
            ("Goldfish", "Goldfish"),
            ("Guppy", "Guppy"),
            ("Zebrafish", "Zebrafish"),
            ("Tetra", "Tetra"),
            ("Minnow", "Minnow"),
            ("Pea Puffer", "PeaPuffer"),
            ("Barb", "Barb"),
            ("Swordtail", "Swordtail"),
            ("Dwarf Gourami", "DwarfGourami")
        ]
        for i, (label, page) in enumerate(data_buttons):
            
            r = i // 3 + 1
            c = i % 3 + 1
            tk.Button(
                self,
                text=label, 
                command= lambda page=page: controller.show_frame(page),
                font=("Arial", 16),
                width=16,
                height=2,
                bg="#DFF0FF"
            ).grid(row=r, column=c, padx=10, pady=10)
        
        # Go Back Button
        tk.Button(
            self,
            text="Go Back",
            command= lambda: controller.show_frame("InitialPage"),
            font=("Arial", 14),
            width=12,
            bg="#FFE0E0"
        ).grid(row=5, column=2, pady=20)

class Goldfish(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        
        # Configuring grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(4, weight=1)
        # Label
        tk.Label(self, text="Goldfish", font=("Arial", 24, "bold")).grid(
            row=1, column=0, columnspan=2, pady=10
        )
        # Data
        data = (
            f"Ideal Water Temperature: {ideal_temp_f['Goldfish']}/{ideal_temp_c['Goldfish']}\n"
            f"Ideal Water pH: {ideal_ph['Goldfish']}\n"
            f"How Many Times to Feed per day: {food_amount['Goldfish']}"
        )

        tk.Label(
            self,
            text=data,
            wraplength=800,
            justify="center",
            font=("Arial", 14),
        ).grid(row=2, column=0, columnspan=2, padx=20, pady=20)

        tk.Button(
            self,
            text="Go Back",
            command=lambda: controller.show_frame("Fishionary"),
            font=("Arial", 12),
            bg="#FFE0E0",
            width=12,
        ).grid(row=3, column=0, columnspan=2, pady=10)

class Guppy(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        
        # Configuring grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(4, weight=1)
        # Label
        tk.Label(self, text="Guppy", font=("Arial", 24, "bold")).grid(
            row=1, column=0, columnspan=2, pady=10
        )
        # Data
        data = (
            f"Ideal Water Temperature: {ideal_temp_f['Guppy']}/{ideal_temp_c['Guppy']}\n"
            f"Ideal Water pH: {ideal_ph['Guppy']}\n"
            f"How Many Times to Feed per day: {food_amount['Guppy']}"
        )

        tk.Label(
            self,
            text=data,
            wraplength=800,
            justify="center",
            font=("Arial", 14),
        ).grid(row=2, column=0, columnspan=2, padx=20, pady=20)

        tk.Button(
            self,
            text="Go Back",
            command=lambda: controller.show_frame("Fishionary"),
            font=("Arial", 12),
            bg="#FFE0E0",
            width=12,
        ).grid(row=3, column=0, columnspan=2, pady=10)

class Zebrafish(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        
        # Configuring grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(4, weight=1)
        # Label
        tk.Label(self, text="Zebrafish", font=("Arial", 24, "bold")).grid(
            row=1, column=0, columnspan=2, pady=10
        )
        # Data
        data = (
            f"Ideal Water Temperature: {ideal_temp_f['Zebrafish']}/{ideal_temp_c['Zebrafish']}\n"
            f"Ideal Water pH: {ideal_ph['Zebrafish']}\n"
            f"How Many Times to Feed per day: {food_amount['Zebrafish']}"
        )

        tk.Label(
            self,
            text=data,
            wraplength=800,
            justify="center",
            font=("Arial", 14),
        ).grid(row=2, column=0, columnspan=2, padx=20, pady=20)

        tk.Button(
            self,
            text="Go Back",
            command=lambda: controller.show_frame("Fishionary"),
            font=("Arial", 12),
            bg="#FFE0E0",
            width=12,
        ).grid(row=3, column=0, columnspan=2, pady=10)

class Tetra(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        
        # Configuring grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(4, weight=1)
        # Label
        tk.Label(self, text="Tetra", font=("Arial", 24, "bold")).grid(
            row=1, column=0, columnspan=2, pady=10
        )
        # Data
        data = (
            f"Ideal Water Temperature: {ideal_temp_f['Tetra']}/{ideal_temp_c['Tetra']}\n"
            f"Ideal Water pH: {ideal_ph['Tetra']}\n"
            f"How Many Times to Feed per day: {food_amount['Tetra']}"
        )

        tk.Label(
            self,
            text=data,
            wraplength=800,
            justify="center",
            font=("Arial", 14),
        ).grid(row=2, column=0, columnspan=2, padx=20, pady=20)

        tk.Button(
            self,
            text="Go Back",
            command=lambda: controller.show_frame("Fishionary"),
            font=("Arial", 12),
            bg="#FFE0E0",
            width=12,
        ).grid(row=3, column=0, columnspan=2, pady=10)

class Minnow(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        
        # Configuring grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(4, weight=1)
        # Label
        tk.Label(self, text="Minnow", font=("Arial", 24, "bold")).grid(
            row=1, column=0, columnspan=2, pady=10
        )
        # Data
        data = (
            f"Ideal Water Temperature: {ideal_temp_f['Minnow']}/{ideal_temp_c['Minnow']}\n"
            f"Ideal Water pH: {ideal_ph['Minnow']}\n"
            f"How Many Times to Feed per day: {food_amount['Minnow']}"
        )

        tk.Label(
            self,
            text=data,
            wraplength=800,
            justify="center",
            font=("Arial", 14),
        ).grid(row=2, column=0, columnspan=2, padx=20, pady=20)

        tk.Button(
            self,
            text="Go Back",
            command=lambda: controller.show_frame("Fishionary"),
            font=("Arial", 12),
            bg="#FFE0E0",
            width=12,
        ).grid(row=3, column=0, columnspan=2, pady=10)

class PeaPuffer(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        
        # Configuring grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(4, weight=1)
        # Label
        tk.Label(self, text="Pea Puffer", font=("Arial", 24, "bold")).grid(
            row=1, column=0, columnspan=2, pady=10
        )
        # Data
        data = (
            f"Ideal Water Temperature: {ideal_temp_f['Pea Puffer']}/{ideal_temp_c['Pea Puffer']}\n"
            f"Ideal Water pH: {ideal_ph['Pea Puffer']}\n"
            f"How Many Times to Feed per day: {food_amount['Pea Puffer']}"
        )

        tk.Label(
            self,
            text=data,
            wraplength=800,
            justify="center",
            font=("Arial", 14),
        ).grid(row=2, column=0, columnspan=2, padx=20, pady=20)

        tk.Button(
            self,
            text="Go Back",
            command=lambda: controller.show_frame("Fishionary"),
            font=("Arial", 12),
            bg="#FFE0E0",
            width=12,
        ).grid(row=3, column=0, columnspan=2, pady=10)

class Barb(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        
        # Configuring grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(4, weight=1)
        # Label
        tk.Label(self, text="Barb", font=("Arial", 24, "bold")).grid(
            row=1, column=0, columnspan=2, pady=10
        )
        # Data
        data = (
            f"Ideal Water Temperature: {ideal_temp_f['Barb']}/{ideal_temp_c['Barb']}\n"
            f"Ideal Water pH: {ideal_ph['Barb']}\n"
            f"How Many Times to Feed per day: {food_amount['Barb']}"
        )

        tk.Label(
            self,
            text=data,
            wraplength=800,
            justify="center",
            font=("Arial", 14),
        ).grid(row=2, column=0, columnspan=2, padx=20, pady=20)

        tk.Button(
            self,
            text="Go Back",
            command=lambda: controller.show_frame("Fishionary"),
            font=("Arial", 12),
            bg="#FFE0E0",
            width=12,
        ).grid(row=3, column=0, columnspan=2, pady=10)

class Swordtail(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        
        # Configuring grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(4, weight=1)
        # Label
        tk.Label(self, text="Swordtail", font=("Arial", 24, "bold")).grid(
            row=1, column=0, columnspan=2, pady=10
        )
        # Data
        data = (
            f"Ideal Water Temperature: {ideal_temp_f['Swordtail']}/{ideal_temp_c['Swordtail']}\n"
            f"Ideal Water pH: {ideal_ph['Swordtail']}\n"
            f"How Many Times to Feed per day: {food_amount['Swordtail']}"
        )

        tk.Label(
            self,
            text=data,
            wraplength=800,
            justify="center",
            font=("Arial", 14),
        ).grid(row=2, column=0, columnspan=2, padx=20, pady=20)

        tk.Button(
            self,
            text="Go Back",
            command=lambda: controller.show_frame("Fishionary"),
            font=("Arial", 12),
            bg="#FFE0E0",
            width=12,
        ).grid(row=3, column=0, columnspan=2, pady=10)

class DwarfGourami(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        
        # Configuring grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(4, weight=1)
        # Label
        tk.Label(self, text="Dwarf Gourami", font=("Arial", 24, "bold")).grid(
            row=1, column=0, columnspan=2, pady=10
        )
        # Data
        data = (
            f"Ideal Water Temperature: {ideal_temp_f['Dwarf Gourami']}/{ideal_temp_c['Dwarf Gourami']}\n"
            f"Ideal Water pH: {ideal_ph['Dwarf Gourami']}\n"
            f"How Many Times to Feed per day: {food_amount['Dwarf Gourami']}"
        )

        tk.Label(
            self,
            text=data,
            wraplength=800,
            justify="center",
            font=("Arial", 14),
        ).grid(row=2, column=0, columnspan=2, padx=20, pady=20)

        tk.Button(
            self,
            text="Go Back",
            command=lambda: controller.show_frame("Fishionary"),
            font=("Arial", 12),
            bg="#FFE0E0",
            width=12,
        ).grid(row=3, column=0, columnspan=2, pady=10)

smartankgui = SmartankGUI()
smartankgui.mainloop()
