from tkinter import *
from math import *
import wHelpWin
#import PythenaMenu

class cMenu():
	def showalert(txt, title):
		global alertx
		alertx = Tk()
		msg = Label(alertx, text = txt)
		msg.grid(row=0)
		msg.config(font=('times', 10)) #, 'italic' bg='white', 
		alertx.title(title)
		q = Button(alertx, text='Close', command=closealert)
		q.grid(row=5)
		alertx.mainloop()
		
	def closealert():
		alertx.destroy()
		
	def About():
		showalert("Pythena System created by Kaiz0r\n\nCalculation v1.0", "Help")
	
	def on_closing():
		master.destroy()	
	
	def initz():
		master = Tk()
		l = Label(master, text="Your Expression:")
		l.grid(row=0)
		entry = Entry(master)
		entry.bind("<Return>", evaluate)
		entry.grid(row=1)
		res = Label(master)
		res.grid(row=2, padx=5)
			
		master.title("Calculator")
		q = Button(master, text='Quit', command=on_closing)
		q.grid(row=3, column=0, ipadx=1)
		ev = Button(master, text='Calculate', command=calc)
		ev.grid(row=3, column=1, ipadx=1)
		master.mainloop()
		
		root = master
		menu = Menu(root)
		root.config(menu=menu)
		
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


#PythenaMenu.
cMenu().initz
#cMenu().
