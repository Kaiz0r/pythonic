from tkinter import *
import atexit
import configparser
import tkinter.messagebox
config = configparser.ConfigParser()
config.readfp(open(r'tcpython.ini'))
filepath = config.get('NOTES', 'filepath')
#defsec = config.get('TIMER', 'defaultsecs')

#filepath = ""#"/home/kaiz0r/projects/Python/Pythena/"
#filepath = "noteruntime.txt"

def About():
    tkinter.messagebox.showinfo("Help","Notes v1.0\n\n1.0 - Fully working basic system.\n\n\nFile saves to noteruntime.txt in same directory as this script by default.\nEdit tcpython.ini to change this.")
    
	#filemenu.add_separator()
	
def initz(win):
	root = win
	menu = Menu(root)
	root.config(menu=menu)
	
	filemenu = Menu(menu)
	menu.add_cascade(label="File", menu=filemenu)
	filemenu.add_command(label="Open", command=openfile)
	filemenu.add_command(label="Save", command=savefile)
	filemenu.add_command(label="Config", command=configz)
	filemenu.add_separator()
	filemenu.add_command(label="Exit", command=root.destroy)
	
	helpmenu = Menu(menu)
	menu.add_cascade(label="Help", menu=helpmenu)
	helpmenu.add_command(label="About...", command=About)

def savefile():
	f = open(filepath, "w")
	print("Saving to "+filepath+"....")
	f.write(T.get('1.0', 'end-1c'))
	tkinter.messagebox.showinfo("Help","File has been saved.\n"+filepath)
	f.close()
	
def openfile(): #TODO - New window with text box input, or file viewer, not sure yet
	tkinter.messagebox.showerror("Error","Function not yet defined.\n>>>TODO - 1")
master = Tk()

S = Scrollbar(master)
S.pack(side=RIGHT, fill=Y)
T = Text(master, height=30, width=70)
T.pack(side=LEFT, fill=Y)
S.config(command=T.yview)
T.config(yscrollcommand=S.set)	

try:
	with open(filepath, "r") as f:
		cont = f.read()
		print("Opening "+filepath+"....")
		T.insert('1.0',cont)
		f.close()
except:
	tkinter.messagebox.showerror("Error","Error in file loading.\n>>>INIT_ERROR")
	

def on_closing():
	f = open(filepath, "w")
	print("Saving to "+filepath+"....")
	f.write(T.get('1.0', 'end'))
	f.close()
	master.destroy()

def finalsave(inp):
	with open(filepath, "w") as outfile:
		outfile.write(inp)
	print("Saving to "+filepath+"....")

def configz():
	global master2
	master2 = Tk()
	msg = Label(master2, text = ">>>TO-DO - 2\nTo add config here.\nReadonly, save on quit")
	msg.grid(row=0)
	msg.config(font=('times', 10)) #, 'italic' bg='white', 
	master2.title("Config")
	q = Button(master2, text='Close', command=clz)
	q.grid(row=5)
	master2.mainloop()
	
def clz():
	master2.destroy()
		
master.protocol("WM_DELETE_WINDOW", on_closing)
#atexit.register(finalsave, T.get('1.0', 'end-1c'))
master.title("Notes")
initz(master)
master.mainloop()
