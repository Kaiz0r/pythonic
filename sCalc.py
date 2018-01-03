from tkinter import *
from math import *
import tkinter.messagebox


def About():
	tkinter.messagebox.showinfo("Help","Calculation v1.0")
    
def initz(win):
	root = win
	menu = Menu(root)
	root.config(menu=menu)
	#filemenu.add_separator()
	filemenu = Menu(menu)
	menu.add_cascade(label="File", menu=filemenu)
	filemenu.add_command(label="Calculate", command=calc)
	filemenu.add_command(label="Exit", command=root.destroy)
	
	helpmenu = Menu(menu)
	menu.add_cascade(label="Help", menu=helpmenu)
	helpmenu.add_command(label="About...", command=About)
	
def evaluate(event):
    res.config(text = str(eval(entry.get())))
    
def calc():
	res.config(text = str(eval(entry.get())))
	
def on_closing():
    master.destroy()
    
master = Tk()
#l = Label(master, text="Your Expression:")
#l.grid(row=0)
entry = Entry(master)
entry.bind("<Return>", evaluate)
entry.grid(row=1)
res = Label(master)
res.grid(row=0, column=0)


master.title("Calculator")
#q = Button(master, text='Quit', command=on_closing)
#q.grid(row=3, column=0, ipadx=0)
ev = Button(master, text='Calculate', command=calc)
ev.grid(row=1, column=2, ipadx=0)
initz(master)
master.mainloop()
