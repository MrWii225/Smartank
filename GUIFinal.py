import tkinter as tk  
from tkinter import ttk
from dictionaries import *
from time import strftime
import time
from PIL import Image, ImageTk
import json
import os
import time
import schedule
from datetime import datetime
import threading
from Sensors import voltage_to_ph, get_phvoltage, get_temp
import RPi.GPIO as GPIO
from time import sleep

# GPIO Pins
FRONT = 18
BACK= 19

# GPIO Setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(BACK, GPIO.OUT)
GPIO.setup(FRONT, GPIO.OUT)
GPIO.output(FRONT, GPIO.HIGH)
GPIO.output(BACK, GPIO.HIGH)

def feed():
	GPIO.output(FRONT, GPIO.LOW)
	sleep(3)
	GPIO.output(FRONT, GPIO.HIGH)
	sleep(0.25)
	GPIO.output(BACK, GPIO.LOW)
	sleep(3)
	GPIO.output(BACK, GPIO.HIGH)
	


AVAILABLE_FONTS = ["Arial", "Georgia", "Times", "Helvetica", "Courier"]
SMALL_FONT_SIZE = 14
MED_FONT_SIZE = 24
LARGE_FONT_SIZE = 40
CONFIG_FILE = "settings.json"
NUMBER = ""
PROVIDER = ""
MESSAGE = ""
FISHTYPE = "Goldfish"
HIGHTEMP = high_temp[FISHTYPE]
LOWTEMP = low_temp[FISHTYPE]
WARNING = ""
PHWARNING = ""
HIGHPH = high_ph[FISHTYPE]
LOWPH = low_ph[FISHTYPE]
temp_alert_sent = None
ph_alert_sent = None
last_alert_time = 0 

ALERT_INTERVAL = 3600


pageph = voltage_to_ph(get_phvoltage())
pagetemp_f = get_temp()


def load_settings():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as file:
            return json.load(file)
    return {
        "theme": "light",
        "font": "Arial",
        "font_size": SMALL_FONT_SIZE,
        "feeding_frequency": 2,
        "phone_num": "",
        "provider": "",
        "message": "",
        "Fish_type": ""
    }

def save_settings(settings):
    with open(CONFIG_FILE, 'w') as file:
        json.dump(settings, file)
import smtplib
from email.message import EmailMessage


def send_sms(message, number, provider):
    msg = EmailMessage()
    msg.set_content(message)
    msg["Subject"] = "SMARTANK"
    msg["From"] = "smartank100@gmail.com"
    msg["To"] = f"{number}@{provider}"

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
            smtp.starttls()
            smtp.login("smartank100@gmail.com", "cnae ccjt hyat qfti")  # use environment variables in production
            smtp.send_message(msg)
            print("SMS sent successfully.")
    except Exception as e:
        print(f"Failed to send SMS: {e}")

def autofeeder():
    print("Task executed at:", datetime.now())
    feed()
    message = "Your fish is being fed :)"
    settings = load_settings()
    number = settings.get("phone_number", "")
    provider = settings.get("provider", "")
    if number and provider:
        send_sms(message, number, provider)

def display_remaining_time():
    next_run = schedule.next_run()
    if next_run:
        time_remaining = next_run - datetime.now()
        return str(time_remaining).split(".")[0]
    else:
        return "Autofeeder disabled"


def Warning():
    global WARNING, temp_alert_sent, last_alert_time
    temp = get_temp()
    current_time = time.time()

    def try_send_alert(message):
        global temp_alert_sent, last_alert_time
        settings = load_settings()
        number = settings.get("phone_number", "")
        provider = settings.get("provider", "")
        if number and provider:
            if temp_alert_sent != message or (current_time - last_alert_time) >= ALERT_INTERVAL:
                send_sms(message, number, provider)
                temp_alert_sent = message
                last_alert_time = current_time

    if int(temp) > int(HIGHTEMP):
        message = "TEMP IS TOO HIGH"
        try_send_alert(message)
        WARNING = message
    elif int(temp) < int(LOWTEMP):
        message = "TEMP IS TOO LOW"
        try_send_alert(message)
        WARNING = message
    else:
        WARNING = ""

def PHWarning():
    global PHWARNING, ph_alert_sent, ph_last_alert_time
    ph = voltage_to_ph(get_phvoltage())
    current_time = time.time()

    def try_send_alert(message):
        global ph_alert_sent, ph_last_alert_time
        settings = load_settings()
        number = settings.get("phone_number", "")
        provider = settings.get("provider", "")
        if number and provider:
            if ph_alert_sent != message or (current_time - ph_last_alert_time) >= ALERT_INTERVAL:
                send_sms(message, number, provider)
                ph_alert_sent = message
                ph_last_alert_time = current_time

    if ph > float(HIGHPH):
        message = "PH IS TOO HIGH"
        try_send_alert(message)
        PHWARNING = message
    elif ph < float(LOWPH):
        message = "PH IS TOO LOW"
        try_send_alert(message)
        PHWARNING = message
    else:
        PHWARNING = ""

class SmartankGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Smartank")
        self.attributes("-fullscreen", True)
        self.bind("<Escape>", lambda e: self.attributes("-fullscreen", False))
        self.style = ttk.Style(self)
        self.style.theme_use("clam")

        self.settings = load_settings()
        self._current_theme = self.settings["theme"]
        self.current_font = self.settings["font"]
        self.current_font_size = self.settings["font_size"]
        self.apply_theme(self._current_theme)

        self.style.configure("TButton", font=(self.current_font, self.current_font_size), padding=6)
        self.style.configure("TLabel", font=(self.current_font, self.current_font_size))

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        container = ttk.Frame(self)
        container.grid(row=0, column=0, sticky="nsew")
        container.rowconfigure(0, weight=1)
        container.columnconfigure(0, weight=1)

        self.NUMBER = self.settings.get("phone_number", "")
        self.PROVIDER = self.settings.get("provider", "")

        self.frames = {}
        for PageClass in (WelcomePage, InitialPage, Options, Display, Autofeeder, Notifications, FishParams, Fishionary, Goldfish, Guppy, Zebrafish, Tetra, Minnow, PeaPuffer, Barb, Swordtail, DwarfGourami):
            page_name = PageClass.__name__
            frame = PageClass(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        if not self.NUMBER or not self.PROVIDER:
            self.show_frame("WelcomePage")
        else:
            self.show_frame("InitialPage")
        threading.Thread(target=self.run_schedule_loop, daemon=True).start()
    
    def run_schedule_loop(self):
        while True:
            schedule.run_pending()
            time.sleep(1)

    def apply_theme(self, theme):
        if theme == "dark":
            self.apply_dark_theme()
        else:
            self.apply_light_theme()

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise() 

    def apply_dark_theme(self):
        self.style.configure("TFrame", background="#2E2E2E")
        self.style.configure("TLabel", background="#2E2E2E", foreground="#FFFFFF")
        self.style.configure("TButton", background="#505050", foreground="#F2F2F2")
        self.style.map("TButton", background=[('active', '#505050')])
        self.style.configure("TCombobox", fieldbackground="#3E3E3E", background="#2E2E2E", foreground="#000000")

    def apply_light_theme(self):
        self.style.configure("TFrame", background="#F9F9F9")
        self.style.configure("TLabel", background="#F9F9F9", foreground="#000000")
        self.style.configure("TButton", background="#E0E0E0", foreground="#000000")
        self.style.map("TButton", background=[('active', '#D0D0D0')])
        self.style.configure("TCombobox", fieldbackground="#FFFFFF", background="#FFFFFF", foreground="#000000")

    def toggle_theme(self):
        self._current_theme = "dark" if self._current_theme == "light" else "light"
        self.settings["theme"] = self._current_theme
        save_settings(self.settings)
        self.apply_theme(self._current_theme)

    def set_font(self, font_name):
        self.current_font = font_name
        self.settings["font"] = font_name

        self.style.configure("TLabel", font=(self.current_font, self.current_font_size))
        self.style.configure("TButton", font=(self.current_font, self.current_font_size))
        self.style.configure("TEntry", font=(self.current_font, self.current_font_size))
        self.style.configure("TCombobox", font=(self.current_font, self.current_font_size))

        save_settings(self.settings)

    def set_font_size(self, font_size):
        if font_size == "Small":
            self.current_font_size = SMALL_FONT_SIZE
        elif font_size == "Large":
            self.current_font_size = LARGE_FONT_SIZE
        else:
            self.current_font_size = MED_FONT_SIZE
        self.settings["font_size"] = self.current_font_size

        self.style.configure("TButton", font=(self.current_font, self.current_font_size))
        self.style.configure("TLabel", font=(self.current_font, self.current_font_size))
        self.style.configure("TEntry", font=(self.current_font, self.current_font_size))
        self.style.configure("TCombobox", font=(self.current_font, self.current_font_size))

        self.frames["InitialPage"].update_clock_font(self.current_font, self.current_font_size)

        save_settings(self.settings)


class WelcomePage(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        ttk.Label(self, text= "WELCOME TO SMARTANK", font=("Times", 40)).pack(pady=10)
        ttk.Label(self, text="Enter Your Phone Number").pack(pady=10)
        self.phone_entry = ttk.Entry(self)
        self.phone_entry.pack(pady=5)

        ttk.Label(self, text="Choose Your Provider").pack(pady=10)
        self.provider_var = tk.StringVar()
        provider_options = ["AT&T", "Verizon", "T-Mobile", "Sprint"]
        provider_menu = ttk.Combobox(self, textvariable=self.provider_var, values=provider_options, state="readonly")
        provider_menu.pack(pady=5)

        ttk.Button(self, text="Save and Continue", command=self.save_info).pack(pady=20)

    def save_info(self):
        phone = self.phone_entry.get().strip()
        if self.provider_var.get().strip() == "AT&T":
            provider = "txt.att.net"
        elif self.provider_var.get().strip() == "Verizon":
            provider = "vtext.com"
        elif self.provider_var.get().strip() == "T-Mobile":
            provider = "tmomail.net"
        elif self.provider_var.get().strip() == "Sprint":
            provider = "messaging.sprintpcs.com"

        if phone and provider:
            self.controller.settings["phone_number"] = phone
            self.controller.settings["provider"] = provider
            save_settings(self.controller.settings)
            self.controller.NUMBER = phone
            self.controller.PROVIDER = provider
            self.controller.show_frame("InitialPage")
        else:
            tk.messagebox.showerror("Error", "Please fill in all fields.")


class InitialPage(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        image_path = "images/SMARTANK.png"
        self.controller = controller

        image = Image.open(image_path)
        photo = ImageTk.PhotoImage(image)
        label = ttk.Label(self, image=photo)
        label.image = photo
        label.pack(padx=10, pady=15)


        self.ph_label = ttk.Label(self, text=" pH")
        self.ph_label.pack(padx=10, pady=10)
        self.temp_label = ttk.Label(self, text=" °F")
        self.temp_label.pack(padx=10, pady=10)
        self.update_sensor_readings()


        self.timer_label = ttk.Label(self, text="Autofeeder timer: Calculating...")
        self.timer_label.pack(padx=10, pady=10)
        self.update_timer()

        ttk.Button(self, text="Fishionary", width=30, command=lambda: controller.show_frame("Fishionary")).pack(pady=5)
        ttk.Button(self, text="Options", width=30, command=lambda: controller.show_frame("Options")).pack(pady=5)

        def time():
            string = strftime('%I:%M:%S %p')
            self.lbl.config(text=string)
            self.lbl.after(1000, time)

        self.lbl = ttk.Label(self)
        self.lbl.pack(pady=5)
        time()

    def update_clock_font(self, font_name, font_size):
        self.lbl.config(font=(font_name, font_size))
    
    def update_sensor_readings(self):
        pageph = voltage_to_ph(get_phvoltage())
        pagetemp_f = get_temp()
        schedule.every(10).seconds.do(Warning).tag("sensor")
        schedule.every(10).seconds.do(PHWarning).tag("sensor")
        self.ph_label.config(text=f"{pageph:.2f} pH {PHWARNING}")
        self.temp_label.config(text=f"{pagetemp_f:.2f} °F {WARNING}")

        self.after(5000, self.update_sensor_readings) #updates sensor readings after 5 seconds

    def update_timer(self):
        remaining = display_remaining_time()
        self.timer_label.config(text=f"Autofeeder timer: {remaining}")
        self.timer_label.after(1000, self.update_timer)




class Options(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        ttk.Button(self, text="Go Back", width=10, command=lambda: controller.show_frame("InitialPage")).pack(pady=8)
        ttk.Button(self, text="Display", width=30, command=lambda: controller.show_frame("Display")).pack(pady=8)
        ttk.Button(self, text="Autofeeder", width=30, command=lambda: controller.show_frame("Autofeeder")).pack(pady=8)
        ttk.Button(self, text="Fish Parameters", width=30, command=lambda: controller.show_frame("FishParams")).pack(pady=8)
        ttk.Button(self, text="Notifications", width=30, command=lambda: controller.show_frame("Notifications")).pack(pady=8)


class Autofeeder(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        ttk.Label(self, text="Set Feedings per Day:").pack(pady=10)

        self.feed_var = tk.StringVar(value=self.controller.settings["feeding_frequency"])
        feed_options = ["1", "2", "3"]
        feed_menu = ttk.Combobox(self, textvariable=self.feed_var, values=feed_options, state="readonly")
        feed_menu.pack(pady=5)

        ttk.Button(self, text="Start Feeding", command=self.feed_now).pack(pady=10)
        ttk.Button(self, text="Go Back", command=lambda: controller.show_frame("Options")).pack(pady=10)

    # Both functions unfinished
    def feed_now(self):
        print("Autofeeder runs.")
        feed()
        freq = int(self.feed_var.get())
        self.controller.settings["feeding_frequency"] = freq
        save_settings(self.controller.settings)
        schedule.clear("autofeeder")

        if freq == 1:
            schedule.every(24).hours.do(autofeeder).tag("autofeeder")
        elif freq == 2:
            schedule.every(12).hours.do(autofeeder).tag("autofeeder")
        elif freq == 3:
            schedule.every(8).hours.do(autofeeder).tag("autofeeder")

    # while True:
    #     schedule.run_pending()
    #     display_remaining_time()  # Show time remaining each iteration
    #     time.sleep(1)  # Check every second



class Display(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        ttk.Button(self, text="Go Back", command=lambda: controller.show_frame("Options")).pack(pady=6)

        ttk.Button(self, text="Switch Theme", command=controller.apply_theme).pack(pady=6)

        ttk.Label(self, text="Change Font:").pack(pady=6)
        font_choice = ttk.Combobox(self, values=AVAILABLE_FONTS, state="readonly")
        font_choice.set(controller.current_font)
        font_choice.pack(pady=6)
        font_choice.bind("<<ComboboxSelected>>", lambda e: controller.set_font(font_choice.get()))

        ttk.Label(self, text="Change Font Size:").pack(pady=6)
        font_size_choice = ttk.Combobox(self, values=["Small", "Medium", "Large"], state="readonly")
        font_size_choice.set("Small" if controller.current_font_size == SMALL_FONT_SIZE else "Large" if controller.current_font_size == LARGE_FONT_SIZE else "Medium")
        font_size_choice.pack(pady=6)
        font_size_choice.bind("<<ComboboxSelected>>", lambda e: controller.set_font_size(font_size_choice.get()))



class FishParams(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.fish_type_var = tk.StringVar()

        ttk.Label(self, text="Fish Parameters Page (under construction)").pack(pady=20)
        self.fish_combo = ttk.Combobox(self, textvariable=self.fish_type_var, values= ["Goldfish","Guppy","Zebrafish","Tetra","Minnow","Pea Puffer","Barb","Swordtail"]).pack(pady=10)
        ttk.Entry(self)
        ttk.Button(self, text="Confirm", command= self.save_fish).pack(pady=10)
        ttk.Button(self, text="Go Back", command=lambda: controller.show_frame("Options")).pack(pady=20)

    def save_fish(self):
        fish_type = self.fish_type_var.get()
        if fish_type:
            self.controller.settings["Fish_type"] = fish_type
            save_settings(self.controller.settings)

class Notifications(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        ttk.Label(self, text="Enter Your Phone Number").pack(pady=10)
        self.phone_entry = ttk.Entry(self)
        self.phone_entry.pack(pady=5)

        ttk.Label(self, text="Choose Your Provider").pack(pady=10)
        self.provider_var = tk.StringVar()
        provider_options = ["AT&T", "Verizon", "T-Mobile", "Sprint"]
        provider_menu = ttk.Combobox(self, textvariable=self.provider_var, values=provider_options, state="readonly")
        provider_menu.pack(pady=5)

        ttk.Button(self, text="Update", command=self.save_info).pack(pady=20)
        ttk.Button(self, text="Go Back", command=lambda: controller.show_frame("Options")).pack(pady=20)


    def save_info(self):
        phone = self.phone_entry.get().strip()
        if self.provider_var.get().strip() == "AT&T":
            provider = "txt.att.net"
        elif self.provider_var.get().strip() == "Verizon":
            provider = "vtext.com"
        elif self.provider_var.get().strip() == "T-Mobile":
            provider = "tmomail.net"
        elif self.provider_var.get().strip() == "Sprint":
            provider = "messaging.sprintpcs.com"

        if phone and provider:
            self.controller.settings["phone_number"] = phone
            self.controller.settings["provider"] = provider
            save_settings(self.controller.settings)
            self.controller.NUMBER = phone
            self.controller.PROVIDER = provider
            self.controller.show_frame("InitialPage")
        else:
            tk.messagebox.showerror("Error", "Please fill in all fields.")



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
