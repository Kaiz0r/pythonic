from tkinter import *
from dice_notation.parser import DiceParser
import tkinter.messagebox

def About():
   tkinter.messagebox.showinfo("Help", "Pythena System created by Kaiz0r\n\nDice Roll v1.0")
    
	#filemenu.add_separator()
	
def initz(win):
	root = win
	menu = Menu(root)
	root.config(menu=menu)
	
	filemenu = Menu(menu)
	menu.add_cascade(label="File", menu=filemenu)
	filemenu.add_command(label="Roll Dice", command=show_entry_fields)
	filemenu.add_command(label="Exit", command=root.destroy)
	
	helpmenu = Menu(menu)
	menu.add_cascade(label="Help", menu=helpmenu)
	helpmenu.add_command(label="About...", command=About)

fresult="No roll yet..."

def show_entry_fields():
	rollin(e1.get(), e2.get())
   # print("Die: %s\nSides: %s\nRolled: %s" % (e1.get(), e2.get(), rollin(e1.get(), e2.get())))
    #sTxt("You rolled " + str(fresult))
   # sTxt("You rolled " + die + "d" + sides + " and got " + result)#
   
def rollin(die, sides):
    global fresult
    parser = DiceParser()
    dice = parser.parse(die + "d" + sides)
    result = dice.roll()
    #T.insert(END,"Rolled "+ str(die) + "d" + str(sides) + "... Got "+str(result)+"\n")
    resultlabel.config(text="Rolled "+ str(die) + "d" + str(sides) + "... Got "+str(result))
    return result

master = Tk()
dielabel = Label(master, text="Die", width=5, anchor='e')
dielabel.grid(row=0)

sidelabel = Label(master, text="Sides", width=5, anchor='e')
sidelabel.grid(row=1)

resultlabel = Label(master, text=str(fresult), width=20, anchor='w')
resultlabel.grid(row=2, column=1)

#T = Text(master, height=2, width=50)
#T.grid(row=3, column=1)

e1 = Entry(master)
e2 = Entry(master)
e1.insert(10,"1")
e2.insert(10,"6")

e1.grid(row=0, column=1)
e2.grid(row=1, column=1)

def on_closing():
    master.destroy()
	
master.title("Dice Roll")
Button(master, text='Quit', command=on_closing).grid(row=5, column=0, sticky=W, pady=4)
Button(master, text='Roll', command=show_entry_fields).grid(row=5, column=1, sticky=W, pady=4)
#PythenaMenu.
initz(master)
#PythenaMenu.adddice(master)
master.mainloop()
