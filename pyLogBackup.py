import sys
import os
from tkinter import *
import shutil
import datetime
from tkinter import filedialog
import notify2

notify2.init('Deus Ex Logging')

def Notif(Summary, Text):
	n = notify2.Notification(Summary,
							 Text,
							 "C731_DXMeshTool.0"
							)
	n.show()
	
#Launching
# execute the file from command-line, e.i. "python3 pyLogBackup.y -a" with -a being either -a, -m or -c depending on the mode
# -a : Auto - Uses the config vars below to automatically clone the files without any input, and renames the cloned file to the current time
# -m : Manual - Brings up file browser dialogs to manually choose the file paths (Does not yet support renaming after cloning)
# -c : Command mode - Uses the command line to choose paths, e.i. python3 pyLogBackup.py -c /a/path/file.log /b/path/new.log - this takes the file.log, clones it to /b/path and calls it new.log

#Auto mode configs, what is read by the -a command
logpath = "/home/kaiz0r/.wine/drive_c/Deus Ex GOTY/System/" #Path to directory where the log file is
outputpath = "/home/kaiz0r/.wine/drive_c/Deus Ex GOTY/System/Backup Logs/" #Path where you want it to be cloned to
filename = "server.log" #The file name

now = datetime.datetime.now()
#f.writelines(now.strftime("%Y-%m-%d %H:%M:%S")+": "+logmsg+"\n")

def alert(title, txt):
	global master
	master = Tk()
	msg = Label(master, text = txt)
	msg.grid(row=0)
	msg.config(font=('times', 12)) #, 'italic' bg='white', 
	master.title(title)
	q = Button(master, text='Close', command=on_closing)
	q.grid(row=5)
	master.mainloop()
	
def on_closing():
    master.destroy()
    
marg = ""
try:
	marg = sys.argv[1]
except IndexError:
	pass
	
try:
	mval1 = sys.argv[2]
except IndexError:
	pass
	
try:
	mval2 = sys.argv[3]
except IndexError:
	pass

try:
	mval3 = sys.argv[4]
except IndexError:
	pass
	
def main():
	if marg == "":
		alert("Error", "No file argument, could not execute.")

	if marg == "-a": #Standard, reads the config name , outputs, automatic so just names it as log
		shutil.copy2(logpath+filename, outputpath)
		print(logpath+filename+" cloned to "+outputpath)
		Notif("Cloned", filename+' cloned to '+outputpath)
		newlogfile = outputpath+filename
		os.rename(outputpath+filename, outputpath+now.strftime("%Y-%m-%d %H.%M.%S")+".log")
		print(newlogfile+" renamed to "+outputpath+now.strftime("%Y-%m-%d %H.%M.%S")+".log")
		Notif("Renamed", newlogfile+' renamed to '+now.strftime("%Y-%m-%d %H.%M.%S")+'.log')
		
	if marg == "-m": #manual mode, doesn't use config, opens file dialog
		templogpath = filedialog.askopenfilename()
		tempoutputpath = filedialog.askdirectory()
		shutil.copy2(templogpath, tempoutputpath)
		print(templogpath+" cloned to "+tempoutputpath)
	
	if marg == "-c": #command mode, like -m but takes the input from the command line
		shutil.copy2(mval1, mval2)
		print(mval1+" cloned to "+mval2)
		
if __name__ == "__main__":
  #Run as main program
  main()
