import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedTk
from dictionaries import *
from time import strftime

class SmartankGUI(tk.Tk):
    def __init__(self):
        super().__init__()  #'plastik', 'arc', 'breeze', 'equilux'
        self.title("Smartank")
        self.geometry("1000x600")

        style = ttk.Style()
        style.configure("TButton", font=('Arial', 14), padding=6)
        style.configure("TLabel", font=('Arial', 14))

        container = ttk.Frame(self)
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

class InitialPage(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        ttk.Label(self, text="Smartank", font=('Georgia', 50)).pack(padx=10, pady=15)
        ttk.Label(self, text="- pH", font=('Arial', 30)).pack(padx=10, pady=10)
        ttk.Label(self, text="- F", font=('Arial', 30)).pack(padx=10, pady=10)
        ttk.Label(self, text="Autofeeder timer: ", font=('Arial', 30)).pack(padx=10, pady=10)

        ttk.Button(self, text="Fishionary", width=30, command=lambda: controller.show_frame("Fishionary")).pack(pady=3)
        ttk.Button(self, text="Options", width=30, command=lambda: controller.show_frame("Options")).pack(pady=3)

        def time():
            string = strftime('%I:%M:%S %p')
            lbl.config(text=string)
            lbl.after(1000, time)

        lbl = ttk.Label(self, font=('Arial', 40))


        lbl.pack(pady=5)
        time()

class Options(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        ttk.Button(self, text="Go Back", width=10, command=lambda: controller.show_frame("InitialPage")).pack(pady=6)
        ttk.Button(self, text="Display", width=30, command=lambda: controller.show_frame("Display")).pack(pady=6)
        ttk.Button(self, text="Autofeeder", width=30, command=lambda: controller.show_frame("InitialPage")).pack(pady=6)

class Display(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        ttk.Button(self, text="Go Back", width=10, command=lambda: controller.show_frame("Options")).pack(pady=6)

class Fishionary(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        for i in range(5):
            self.grid_columnconfigure(i, weight=1)
            self.grid_rowconfigure(i, weight=1)

        ttk.Label(self, text="Fishionary", font=("Arial", 24, "bold")).grid(row=0, column=0, columnspan=5, pady=20)

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
            ttk.Button(
                self,
                text=label,
                command=lambda page=page: controller.show_frame(page),
                width=20
            ).grid(row=r, column=c, padx=10, pady=10)

        ttk.Button(self, text="Go Back", command=lambda: controller.show_frame("InitialPage")).grid(row=5, column=2, pady=20)


class InfoPage(ttk.Frame):
    def __init__(self, parent, controller, fish_name):
        super().__init__(parent)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        ttk.Label(self, text=fish_name, font=("Arial", 24, "bold")).grid(row=1, column=0, columnspan=2, pady=10)

        data = (
            f"Ideal Water Temperature: {ideal_temp_f[fish_name]}/{ideal_temp_c[fish_name]}\n"
            f"Ideal Water pH: {ideal_ph[fish_name]}\n"
            f"How Many Times to Feed per day: {food_amount[fish_name]}"
        )

        ttk.Label(self, text=data, wraplength=800, justify="center").grid(row=2, column=0, columnspan=2, padx=20, pady=20)

        ttk.Button(self, text="Go Back", command=lambda: controller.show_frame("Fishionary")).grid(row=3, column=0, columnspan=2, pady=10)

class Goldfish(InfoPage):     
    def __init__(self, parent, controller): super().__init__(parent, controller, "Goldfish")
class Guppy(InfoPage):        
    def __init__(self, parent, controller): super().__init__(parent, controller, "Guppy")
class Zebrafish(InfoPage):    
    def __init__(self, parent, controller): super().__init__(parent, controller, "Zebrafish")
class Tetra(InfoPage):        
    def __init__(self, parent, controller): super().__init__(parent, controller, "Tetra")
class Minnow(InfoPage):       
    def __init__(self, parent, controller): super().__init__(parent, controller, "Minnow")
class PeaPuffer(InfoPage):    
    def __init__(self, parent, controller): super().__init__(parent, controller, "Pea Puffer")
class Barb(InfoPage):         
    def __init__(self, parent, controller): super().__init__(parent, controller, "Barb")
class Swordtail(InfoPage):    
    def __init__(self, parent, controller): super().__init__(parent, controller, "Swordtail")
class DwarfGourami(InfoPage): 
    def __init__(self, parent, controller): super().__init__(parent, controller, "Dwarf Gourami")

# Run the app
if __name__ == "__main__":
    app = SmartankGUI()
    app.mainloop()
