from tkinter import *
import tkinter.font as font
from time import strftime




def raise_frame(frame):
    frame.tkraise()

root = Tk()

default_font = font.nametofont("TkDefaultFont")
default_font.configure(size=20)

f1 = Frame(root)
f2 = Frame(root)
f3 = Frame(root)
f4 = Frame(root)

for frame in (f1, f2, f3, f4):
    frame.grid(row=0, column=0, sticky='news')

# Main Page 

Label(f1, text='Temp: 77').pack()
Label(f1, text='pH: 7.0').pack()

Button(f1, text='Options', command=lambda:raise_frame(f2)).pack()
Button(f1, text='Fishionary', command=lambda:raise_frame(f3)).pack()

def time(): 
    string = strftime('%I:%M:%S %p') 
    lbl.config(text = string) 
    lbl.after(1000, time) 

lbl=Label(f1, font = ('Times New Roman', 40)) 

lbl.pack() 
time() 
################################

Label(f2, text='Options').pack()
Button(f2, text='Back', command=lambda:raise_frame(f1)).pack()
Button(f2, text='Display', command=lambda:raise_frame(f4)).pack()
Button(f2, text='Feeder', command=lambda:raise_frame(f4)).pack()

Label(f3, text='Fishionary').pack()
Button(f3, text='Back', command=lambda:raise_frame(f1)).pack()


Button(f4,text="Back", command=lambda:raise_frame(f2)).pack()

raise_frame(f1)
root.mainloop()