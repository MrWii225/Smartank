import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from time import strftime
import json
import os
import schedule
from datetime import datetime
import threading
import smtplib
from email.message import EmailMessage
import RPi.GPIO as GPIO
from dictionaries import *
from Sensors import voltage_to_ph, get_phvoltage, get_temp

FRONT = 18
BACK = 19
GPIO.setmode(GPIO.BCM)
GPIO.setup(BACK, GPIO.OUT)
GPIO.setup(FRONT, GPIO.OUT)
GPIO.output(FRONT, GPIO.HIGH)
GPIO.output(BACK, GPIO.HIGH)

AVAILABLE_FONTS = ["Arial", "Georgia", "Times", "Helvetica", "Courier"]
SMALL_FONT_SIZE = 14
MED_FONT_SIZE = 24
LARGE_FONT_SIZE = 40
CONFIG_FILE = "settings.json"
WARNING = ""
PHWARNING = ""
temp_alert_sent = None
ph_alert_sent = None

def load_settings():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as file:
            return json.load(file)
    return {
        "theme": "light",
        "font": "Arial",
        "font_size": SMALL_FONT_SIZE,
        "feeding_frequency": 2,
        "phone_number": "",
        "provider": "",
        "message": "",
        "Fish_type": "Goldfish"
    }

def save_settings(settings):
    with open(CONFIG_FILE, 'w') as file:
        json.dump(settings, file)

def feed():
    GPIO.output(FRONT, GPIO.LOW)
    threading.Event().wait(3)
    GPIO.output(FRONT, GPIO.HIGH)
    threading.Event().wait(0.25)
    GPIO.output(BACK, GPIO.LOW)
    threading.Event().wait(3)
    GPIO.output(BACK, GPIO.HIGH)

def send_sms(message, number, provider):
    msg = EmailMessage()
    msg.set_content(message)
    msg['Subject'] = 'SMARTANK'
    msg['From'] = 'smartank100@gmail.com'
    msg['To'] = f"{number}@{provider}"
    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
            smtp.starttls()
            smtp.login("smartank100@gmail.com", "cnae ccjt hyat qfti")
            smtp.send_message(msg)
            print("SMS sent successfully.")
    except Exception as e:
        print(f"Failed to send SMS: {e}")

def autofeeder():
    print("Feeding at:", datetime.now())
    feed()
    settings = load_settings()
    number = settings.get("phone_number", "")
    provider = settings.get("provider", "")
    if number and provider:
        send_sms("Your fish has been fed!", number, provider)

def display_remaining_time():
    next_run = schedule.next_run()
    if next_run:
        remaining = next_run - datetime.now()
        return str(remaining).split('.')[0]
    return "Autofeeder disabled"

def Warning():
    global WARNING, temp_alert_sent
    temp = get_temp()
    settings = load_settings()
    number = settings.get("phone_number", "")
    provider = settings.get("provider", "")

    if int(temp) > int(high_temp[settings["Fish_type"]]):
        message = "TEMP IS TOO HIGH"
        if number and provider and temp_alert_sent != message:
            send_sms(message, number, provider)
            temp_alert_sent = message
        WARNING = message
    elif int(temp) < int(low_temp[settings["Fish_type"]]):
        message = "TEMP IS TOO LOW"
        if number and provider and temp_alert_sent != message:
            send_sms(message, number, provider)
            temp_alert_sent = message
        WARNING = message
    else:
        WARNING = ""
        temp_alert_sent = None

def PHWarning():
    global PHWARNING, ph_alert_sent
    ph = voltage_to_ph(get_phvoltage())
    settings = load_settings()
    number = settings.get("phone_number", "")
    provider = settings.get("provider", "")

    if ph > float(high_ph[settings["Fish_type"]]):
        message = "PH IS TOO HIGH"
        if number and provider and ph_alert_sent != message:
            send_sms(message, number, provider)
            ph_alert_sent = message
        PHWARNING = message
    elif ph < float(low_ph[settings["Fish_type"]]):
        message = "PH IS TOO LOW"
        if number and provider and ph_alert_sent != message:
            send_sms(message, number, provider)
            ph_alert_sent = message
        PHWARNING = message
    else:
        PHWARNING = ""
        ph_alert_sent = None



class SmartankGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Smartank")
        self.attributes("-fullscreen", True)
        self.bind("<Escape>", lambda e: self.attributes("-fullscreen", False))

        self.settings = load_settings()
        self._current_theme = self.settings["theme"]
        self.current_font = self.settings["font"]
        self.current_font_size = self.settings["font_size"]

        self.style = ttk.Style(self)
        self.style.theme_use("clam")
        self.apply_theme(self._current_theme)

        container = ttk.Frame(self)
        container.grid(row=0, column=0, sticky="nsew")

        self.frames = {}
        for PageClass in (WelcomePage, InitialPage, Options, Display, AutofeederPage, Notifications, FishParams, Fishionary, Goldfish, Guppy, Zebrafish, Tetra, Minnow, PeaPuffer, Barb, Swordtail, DwarfGourami):
            page_name = PageClass.__name__
            frame = PageClass(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        if not self.settings.get("phone_number") or not self.settings.get("provider"):
            self.show_frame("WelcomePage")
        else:
            self.show_frame("InitialPage")

        threading.Thread(target=self.run_schedule_loop, daemon=True).start()

    def run_schedule_loop(self):
        schedule.every(10).seconds.do(Warning).tag("sensor")
        schedule.every(10).seconds.do(PHWarning).tag("sensor")
        while True:
            schedule.run_pending()
            threading.Event().wait(1)

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()

    def apply_theme(self, theme):
        if theme == "dark":
            bg, fg, btn_bg = "#2E2E2E", "#FFFFFF", "#505050"
        else:
            bg, fg, btn_bg = "#F9F9F9", "#000000", "#E0E0E0"

        self.style.configure("TFrame", background=bg)
        self.style.configure("TLabel", background=bg, foreground=fg)
        self.style.configure("TButton", background=btn_bg, foreground=fg)



class WelcomePage(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        ttk.Label(self, text="WELCOME TO SMARTANK", font=("Times", 40)).pack(pady=10)
        ttk.Label(self, text="Enter Your Phone Number").pack(pady=10)
        self.phone_entry = ttk.Entry(self)
        self.phone_entry.pack(pady=5)

        ttk.Label(self, text="Choose Your Provider").pack(pady=10)
        self.provider_var = tk.StringVar()
        provider_menu = ttk.Combobox(self, textvariable=self.provider_var, values=["AT&T", "Verizon", "T-Mobile", "Sprint"], state="readonly")
        provider_menu.pack(pady=5)

        ttk.Button(self, text="Save and Continue", command=self.save_info).pack(pady=20)

    def save_info(self):
        phone = self.phone_entry.get().strip()
        provider_map = {"AT&T": "txt.att.net", "Verizon": "vtext.com", "T-Mobile": "tmomail.net", "Sprint": "messaging.sprintpcs.com"}
        provider = provider_map.get(self.provider_var.get().strip(), "")

        if phone and provider:
            self.controller.settings["phone_number"] = phone
            self.controller.settings["provider"] = provider
            save_settings(self.controller.settings)
            self.controller.show_frame("InitialPage")
        else:
            messagebox.showerror("Error", "Please fill in all fields.")



class InitialPage(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        img = Image.open("images/SMARTANK.png")
        photo = ImageTk.PhotoImage(img)
        label = ttk.Label(self, image=photo)
        label.image = photo
        label.pack(padx=10, pady=15)

        self.ph_label = ttk.Label(self, text=" pH")
        self.ph_label.pack(padx=10, pady=10)
        self.temp_label = ttk.Label(self, text=" °F")
        self.temp_label.pack(padx=10, pady=10)

        self.timer_label = ttk.Label(self, text="Autofeeder timer: Calculating...")
        self.timer_label.pack(padx=10, pady=10)

        ttk.Button(self, text="Options", command=lambda: controller.show_frame("Options")).pack(pady=5)

        self.update_readings()

    def update_readings(self):
        pageph = voltage_to_ph(get_phvoltage())
        pagetemp_f = get_temp()
        self.ph_label.config(text=f"{pageph:.2f} pH {PHWARNING}")
        self.temp_label.config(text=f"{pagetemp_f:.2f} °F {WARNING}")
        self.timer_label.config(text=f"Autofeeder timer: {display_remaining_time()}")
        self.after(5000, self.update_readings)



class Options(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        ttk.Button(self, text="Display", command=lambda: controller.show_frame("Display")).pack(pady=6)
        ttk.Button(self, text="Autofeeder", command=lambda: controller.show_frame("AutofeederPage")).pack(pady=6)
        ttk.Button(self, text="Notifications", command=lambda: controller.show_frame("Notifications")).pack(pady=6)
        ttk.Button(self, text="Fish Parameters",command=lambda: controller.show_frame("FishParams")).pack(pady=6)
        ttk.Button(self, text="Go Back", command=lambda: controller.show_frame("InitialPage")).pack(pady=6)



class Display(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

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

        ttk.Button(self, text="Go Back", command=lambda: controller.show_frame("Options")).pack(pady=6)



class AutofeederPage(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        ttk.Label(self, text="Set Feedings per Day:").pack(pady=10)
        self.feed_var = tk.StringVar(value=str(controller.settings["feeding_frequency"]))
        feed_menu = ttk.Combobox(self, textvariable=self.feed_var, values=["1", "2", "3"], state="readonly")
        feed_menu.pack(pady=5)

        ttk.Button(self, text="Start Feeding Schedule", command=self.set_schedule).pack(pady=10)
        ttk.Button(self, text="Feed Now", command=feed).pack(pady=5)
        ttk.Button(self, text="Go Back", command=lambda: controller.show_frame("Options")).pack(pady=10)

    def set_schedule(self):
        freq = int(self.feed_var.get())
        self.controller.settings["feeding_frequency"] = freq
        save_settings(self.controller.settings)

        schedule.clear("autofeeder")
        interval = {1: 24, 2: 12, 3: 8}.get(freq, 12)
        schedule.every(interval).hours.do(autofeeder).tag("autofeeder")



class Notifications(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        ttk.Label(self, text="Enter Your Phone Number").pack(pady=10)
        self.phone_entry = ttk.Entry(self)
        self.phone_entry.pack(pady=5)

        ttk.Label(self, text="Choose Your Provider").pack(pady=10)
        self.provider_var = tk.StringVar()
        provider_menu = ttk.Combobox(self, textvariable=self.provider_var, values=["AT&T", "Verizon", "T-Mobile", "Sprint"], state="readonly")
        provider_menu.pack(pady=5)

        ttk.Button(self, text="Update", command=self.save_info).pack(pady=20)
        ttk.Button(self, text="Go Back", command=lambda: controller.show_frame("Options")).pack(pady=20)

    def save_info(self):
        phone = self.phone_entry.get().strip()
        provider_map = {"AT&T": "txt.att.net", "Verizon": "vtext.com", "T-Mobile": "tmomail.net", "Sprint": "messaging.sprintpcs.com"}
        provider = provider_map.get(self.provider_var.get().strip(), "")

        if phone and provider:
            self.controller.settings["phone_number"] = phone
            self.controller.settings["provider"] = provider
            save_settings(self.controller.settings)
            self.controller.show_frame("InitialPage")
        else:
            messagebox.showerror("Error", "Please fill in all fields.")



class FishParams(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.fish_type_var = tk.StringVar()
        ttk.Label(self, text="Fish Parameters Page").pack(pady=20)
        self.fish_combo = ttk.Combobox(self, textvariable=self.fish_type_var, values=[
            "Goldfish", "Guppy", "Zebrafish", "Tetra", "Minnow", "Pea Puffer", "Barb", "Swordtail", "Dwarf Gourami"],
            state="readonly")
        self.fish_combo.pack(pady=10)
        ttk.Button(self, text="Confirm", command=self.save_fish).pack(pady=10)
        ttk.Button(self, text="Go Back", command=lambda: controller.show_frame("Options")).pack(pady=20)

    def save_fish(self):
        fish_type = self.fish_type_var.get()
        if fish_type:
            self.controller.settings["Fish_type"] = fish_type
            save_settings(self.controller.settings)



class Fishionary(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        for i in range(5):
            self.grid_columnconfigure(i, weight=1)
            self.grid_rowconfigure(i, weight=1)

        ttk.Label(self, text="Fishionary").grid(row=0, column=0, columnspan=5, pady=20)

        data_buttons = [
            ("Goldfish", "Goldfish"), ("Guppy", "Guppy"), ("Zebrafish", "Zebrafish"),
            ("Tetra", "Tetra"), ("Minnow", "Minnow"), ("Pea Puffer", "PeaPuffer"),
            ("Barb", "Barb"), ("Swordtail", "Swordtail"), ("Dwarf Gourami", "DwarfGourami")
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
