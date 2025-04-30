import tkinter as tk  
from tkinter import ttk
from dictionaries import *
from time import strftime
from PIL import Image, ImageTk

AVAILABLE_FONTS = ["Arial", "Georgia", "Times", "Courier", "Comic Sans MS"]
SMALL_FONT_SIZE = 14
MED_FONT_SIZE = 24
LARGE_FONT_SIZE = 40

class SmartankGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Smartank")
        self.geometry("1000x600")
        self.style = ttk.Style(self)
        self._current_theme = "light"
        self.current_font = "Arial"
        self.current_font_size = SMALL_FONT_SIZE
        self.apply_light_theme()

        self.style.configure("TButton", font=(self.current_font, self.current_font_size), padding=6)
        self.style.configure("TLabel", font=(self.current_font, self.current_font_size))

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        container = ttk.Frame(self)
        container.grid(row=0, column=0, sticky="nsew")
        container.rowconfigure(0, weight=1)
        container.columnconfigure(0, weight=1)

        self.frames = {}
        for PageClass in (InitialPage, Options, Display, Autofeeder, FishParams, Fishionary, Goldfish, Guppy, Zebrafish, Tetra, Minnow, PeaPuffer, Barb, Swordtail, DwarfGourami):
            page_name = PageClass.__name__
            frame = PageClass(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("InitialPage")

    @property
    def current_theme(self):
        return self._current_theme

    @current_theme.setter
    def current_theme(self, value):
        self._current_theme = value

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()

    def apply_dark_theme(self):
        self.style.configure("TFrame", background="#2E2E2E")
        self.style.configure("TLabel", background="#2E2E2E", foreground="#FFFFFF")
        self.style.configure("TButton", background="#3E3E3E", foreground="#000000")
        self.style.map("TButton", background=[('active', '#505050')])
        self.style.configure("TCombobox", fieldbackground="#3E3E3E", background="#2E2E2E", foreground="#000000")
        self.current_theme = "dark"

    def apply_light_theme(self):
        self.style.configure("TFrame", background="#F9F9F9")
        self.style.configure("TLabel", background="#F9F9F9", foreground="#000000")
        self.style.configure("TButton", background="#E0E0E0", foreground="#000000")
        self.style.map("TButton", background=[('active', '#D0D0D0')])
        self.style.configure("TCombobox", fieldbackground="#FFFFFF", background="#FFFFFF", foreground="#000000")
        self.current_theme = "light"

    def toggle_theme(self):
        if self.current_theme == "light":
            self.apply_dark_theme()
        else:
            self.apply_light_theme()

    def set_font(self, font_name):
        self.current_font = font_name
        self.style.configure("TButton", font=(self.current_font, self.current_font_size))
        self.style.configure("TLabel", font=(self.current_font, self.current_font_size))

        for frame in self.frames.values():
            for widget in frame.winfo_children():
                if isinstance(widget, (ttk.Label, ttk.Button, ttk.Entry, ttk.Combobox)):
                    widget.configure(font=(self.current_font, self.current_font_size))
        self.frames["InitialPage"].update_clock_font(self.current_font, self.current_font_size)

    def set_font_size(self, font_size):
        if font_size == "Small":
            self.current_font_size = SMALL_FONT_SIZE
        elif font_size == "Large":
            self.current_font_size = LARGE_FONT_SIZE
        else:
            self.current_font_size = MED_FONT_SIZE

        self.style.configure("TButton", font=(self.current_font, self.current_font_size))
        self.style.configure("TLabel", font=(self.current_font, self.current_font_size))

        for frame in self.frames.values():
            for widget in frame.winfo_children():
                if isinstance(widget, (ttk.Label, ttk.Button, ttk.Entry, ttk.Combobox)):
                    widget.configure(font=(self.current_font, self.current_font_size))
        self.frames["InitialPage"].update_clock_font(self.current_font, self.current_font_size)

class InitialPage(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        image_path = "C:/Users/Shawn/OneDrive/Desktop/Smartank/Screenshot 2025-04-23 172321.png"
        image = Image.open(image_path)
        photo = ImageTk.PhotoImage(image)
        label = ttk.Label(self, image=photo)
        label.image = photo
        label.pack(padx=10, pady=15)

        ttk.Label(self, text="- pH", font=('Arial', 30)).pack(padx=10, pady=10)
        ttk.Label(self, text="- F", font=('Arial', 30)).pack(padx=10, pady=10)

        ttk.Label(self, text="Autofeeder timer: ", font=('Arial', 30)).pack(padx=10, pady=10)

        ttk.Button(self, text="Fishionary", width=30, command=lambda: controller.show_frame("Fishionary")).pack(pady=5)
        ttk.Button(self, text="Options", width=30, command=lambda: controller.show_frame("Options")).pack(pady=5)

        def time():
            string = strftime('%I:%M:%S %p')
            self.lbl.config(text=string)
            self.lbl.after(1000, time)

        self.lbl = ttk.Label(self,font=("Times",40))
        self.lbl.pack(pady=5)
        time()

class Options(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        ttk.Button(self, text="Go Back", width=10, command=lambda: controller.show_frame("InitialPage")).pack(pady=8)
        ttk.Button(self, text="Display", width=30, command=lambda: controller.show_frame("Display")).pack(pady=8)
        ttk.Button(self, text="Autofeeder", width=30, command=lambda: controller.show_frame("Autofeeder")).pack(pady=8)
        ttk.Button(self, text="Fish Parameters", width=30, command=lambda:controller.show_frame("FishParams")).pack(pady=8)

class Autofeeder(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        ttk.Label(self, text="Set Feedings per Day:").pack(pady=10)

        self.feed_var = tk.IntVar(value=2)
        feed_options = [1, 2, 3]
        feed_menu = ttk.Combobox(self, textvariable=self.feed_var, values=feed_options, state="readonly")
        feed_menu.pack(pady=5)

        ttk.Button(self, text="Feed Now", command=self.feed_now).pack(pady=10)
        ttk.Button(self, text="Go Back", command=lambda: controller.show_frame("Options")).pack(pady=10)
    def autofeeder(self):
        pass
    def feed_now(self):
        ##### Placeholder #####
        print("Autofeeder runs.")

class Display(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        ttk.Button(self, text="Go Back", command=lambda: controller.show_frame("Options")).pack(pady=6)

        ttk.Button(self, text="Switch Theme", command=controller.toggle_theme).pack(pady=6)

        ttk.Label(self, text="Change Font:").pack(pady=6)
        font_choice = ttk.Combobox(self, values=AVAILABLE_FONTS, state="readonly")
        font_choice.set(controller.current_font)
        font_choice.pack(pady=6)
        font_choice.bind("<<ComboboxSelected>>", lambda e: controller.set_font(font_choice.get()))

        ttk.Label(self, text="Change Font Size:").pack(pady=6)
        font_size_choice = ttk.Combobox(self, values=["Small", "Medium", "Large"], state="readonly")
        font_size_choice.set("Small")
        font_size_choice.pack(pady=6)
        font_size_choice.bind("<<ComboboxSelected>>", lambda e: controller.set_font_size(font_size_choice.get()))

class FishParams(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        ttk.Label(self, text="Parameters").pack()
        ttk.Button(self, text="")

class Fishionary(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        for i in range(5):
            self.grid_columnconfigure(i, weight=1)
            self.grid_rowconfigure(i, weight=1)

        ttk.Label(self, text="Fishionary").grid(row=0, column=0, columnspan=5, pady=20)

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
            ttk.Button(self, text=label, command=lambda page=page: controller.show_frame(page), width=20).grid(row=r, column=c, padx=10, pady=10)

        ttk.Button(self, text="Go Back", command=lambda: controller.show_frame("InitialPage")).grid(row=5, column=2, pady=20)

class InfoPage(ttk.Frame):
    def __init__(self, parent, controller, fish_name):
        super().__init__(parent)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        ttk.Label(self, text=fish_name).grid(row=1, column=0, columnspan=2, pady=10)

        data = (
            f"Ideal Water Temperature: {ideal_temp_f[fish_name]}/{ideal_temp_c[fish_name]}\n"
            f"Ideal Water pH: {ideal_ph[fish_name]}\n"
            f"How Many Times to Feed per day: {food_amount[fish_name]}"
        )

        ttk.Label(self, text=data, wraplength=800, justify="center").grid(row=2, column=0, columnspan=2, padx=20, pady=20)
        ttk.Button(self, text="Go Back", command=lambda: controller.show_frame("Fishionary")).grid(row=3, column=0, columnspan=2, pady=10)

class Goldfish(InfoPage):     
    def __init__(self, parent, controller): 
        super().__init__(parent, controller, "Goldfish")
class Guppy(InfoPage):        
    def __init__(self, parent, controller): 
        super().__init__(parent, controller, "Guppy")
class Zebrafish(InfoPage):    
    def __init__(self, parent, controller): 
        super().__init__(parent, controller, "Zebrafish")
class Tetra(InfoPage):        
    def __init__(self, parent, controller): 
        super().__init__(parent, controller, "Tetra")
class Minnow(InfoPage):       
   def __init__(self, parent, controller): 
        super().__init__(parent, controller, "Minnow")
class PeaPuffer(InfoPage):    
    def __init__(self, parent, controller): 
        super().__init__(parent, controller, "Pea Puffer")
class Barb(InfoPage):         
    def __init__(self, parent, controller): 
        super().__init__(parent, controller, "Barb")
class Swordtail(InfoPage):    
    def __init__(self, parent, controller): 
        super().__init__(parent, controller, "Swordtail")
class DwarfGourami(InfoPage): 
    def __init__(self, parent, controller): 
        super().__init__(parent, controller, "Dwarf Gourami")


if __name__ == "__main__":
    app = SmartankGUI()
    app.mainloop() 
