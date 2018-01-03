from tkinter import *
import tkinter.messagebox
from math import *
import time
import threading
import configparser
from subprocess import call, run
import pygame
#from playsound import playsound
#config = configparser.ConfigParser()
#config['DEFAULT'] = {'defaultmins': '0',
 #                     'defaultsecs': '10',
 #                     'sound': 'True',
#                      'soundpath': 'None'}
#with open('example.ini', 'w') as configfile:
	#config.write(configfile)

running=False


def About():
    tkinter.messagebox.showinfo("Help","Timer by Kaiz0r v1.0\nTodo: Naming timers for having multiple running at once.\nConfig file stored as: /pythena.ini [TIMER]")
    
def countdown():
	global cursecs, t, curmins, running
	if running is False:
		w.title("Timer")
		t.cancel()
		return
	elif running is True:
		t=threading.Timer(1, countdown)
		t.start()
	nm = curmins #int(entryTextmins.get())
	ns = cursecs #int(entryTextsecs.get())
	#print("-"+str(nm)+"-"+str(ns))
	ns = ns - 1
	if ns < 10 and ns >= 0:
		fns = "0"+str(ns)
	else:
		fns = ns
	if ns <= 0 and nm > 0:
		ns = 60
		nm = nm - 1
		fns = ns

	entryTextsecs.set(fns)
	cursecs = ns
	entryTextmins.set(nm)
	curmins = nm
	l3.config(text=str(nm)+":"+str(fns))
	w.title(str(nm)+":"+str(fns))
	if ns <= 0 and nm <= 0:
		running=False
		t.cancel()
		ev2.config(state=DISABLED)
		ev.config(state=NORMAL)
		entrymins.config(state=NORMAL)
		entrysecs.config(state=NORMAL)
		callsound()
		w.title("ALERT!")
		#wHelpWin.inito("Timer has expired", "Alert")
		tkinter.messagebox.showinfo("Alert", "Timer expired!")
		w.title("Timer")
		#on_closing()
		#callcom()

def callsound():
	pygame.mixer.music.play()
	#playsound("alarm.wav")
	
def callcom():
	config = configparser.ConfigParser()
	config.readfp(open(r'pythena.ini'))
	#''runcommand = config.get('TIMER', 'runcommand')
	#''docommand = config.get('TIMER', 'command')
	print(runcommand+docommand)
	call([docommand])
	if runcommand is "True":
		run(docommand)
		print(docommand)
	
def initz(win):
	root = win
	menu = Menu(root)
	root.config(menu=menu)
	
	filemenu = Menu(menu)
	menu.add_cascade(label="File", menu=filemenu)
	#filemenu.add_command(label="Calculate", command=calc)
	filemenu.add_command(label="Exit", command=root.destroy)
	
	helpmenu = Menu(menu)
	menu.add_cascade(label="Help", menu=helpmenu)
	helpmenu.add_command(label="About...", command=About)

def inittimer():
	global running, t, cursecs, curmins
	if running is False:
		try:
			cursecs=int(entryTextsecs.get())
			curmins=int(entryTextmins.get())
		except TclError:
			tkinter.messagebox.showerror("Error", "Values invalid.")
			return
		if int(cursecs) <= 0 and int(curmins) <= 0:
			tkinter.messagebox.showerror("Error", "Values must be positive numbers.")
			return
		running=True
		fsec = int(cursecs)
		if fsec < 10 and fsec >= 0:
			fsec = "0"+str(fsec)
		entryTextsecs.set(fsec)
		ev2.config(state=NORMAL)
		ev.config(state=DISABLED)
		#l3.config(text=str(entryTextmins.get())+":"+str(entryTextsecs.get()))
		l3.config(text=str(entryTextmins.get())+":"+str(fsec))
		t=threading.Timer(1, countdown)
		t.start()
		entrymins.config(state=DISABLED)
		entrysecs.config(state=DISABLED)
	else:
		tkinter.messagebox.showerror("Error", "Function should not be called here, report as a bug.\n>>>inittimer()\nRAN WHILE BOOL WAS TRUE")

def endtimer():
	global running, t, cursecs, curmins
	if running is True:
		running=False
		ev2.config(state=DISABLED)
		ev.config(state=NORMAL)
		entrymins.config(state=NORMAL)
		entrysecs.config(state=NORMAL)
		t.cancel()
		w.title("Timer")
	else:
		tkinter.messagebox.showerror("Error", "Function should not be called here, report as a bug.\n>>>endtimer()\nRAN WHILE BOOL WAS FALSE")

#entrymins.insert(10,"0")
#entrysecs.insert(10,"5")
#res = Label(w)
#res.grid(row=2)

def on_closing():
    w.destroy()

w = Tk()
l = Label(w, text="Minutes:")
l.grid(row=1, column=0)
l2 = Label(w, text="Seconds:")
l2.grid(row=1, column=2)
l3 = Label(w, text="0:00")
l3.grid(row=2, column=3)
entrymins = Entry(w) #entry.bind("<Return>", evaluate)

config = configparser.ConfigParser()
config.readfp(open(r'tcpython.ini'))
defmin = config.get('TIMER', 'defaultmins')
defsec = config.get('TIMER', 'defaultsecs')


entryTextmins = IntVar()
entrymins = Entry( w, textvariable=str(entryTextmins) )
entryTextmins.set( defmin )

entryTextsecs = IntVar()
entrysecs = Entry( w, textvariable=str(entryTextsecs) )
entryTextsecs.set( defsec )

entrymins.grid(row=1, column=1)
entrymins.config(width=5)
entrysecs.grid(row=1, column=3)
entrysecs.config(width=5)

w.title("Timer")
#q = Button(w, text='Quit', command=on_closing)
#q.grid(row=2, column=0)
ev = Button(w, text='Start', command=inittimer)
ev.grid(row=2, column=0)
ev2 = Button(w, text='Stop', command=endtimer, state=DISABLED)
ev2.grid(row=2, column=1)

pygame.init()
config = configparser.ConfigParser()
config.readfp(open(r'tcpython.ini'))
#sound = config.get('TIMER', 'sound')
soundpath = config.get('TIMER', 'soundpath')
##if sound is True:
pygame.mixer.music.load(soundpath)
initz(w)
w.mainloop()
w.quit()
