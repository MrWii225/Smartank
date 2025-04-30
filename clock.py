from tkinter import *
from tkinter.ttk import *
from time import strftime
# moved clock logic into GUI.py cause I'm stupid and couldn't figure out how to import

Window = Tk()
Window.title('Clock') 

# This function is used to 
# display time on the label 
def time(): 
    string = strftime('%I:%M:%S %p') 
    lbl.config(text = string) 
    lbl.after(1000, time) 

# Styling the label widget so that clock 
# will look more attractive 
lbl = Label(Window, font = ('Times New Roman', 40), 
            background = 'black', 
            foreground = 'white') 

# Placing clock at the centre 
# of the tkinter window 
lbl.pack(anchor = 'center') 
time() 

mainloop() 