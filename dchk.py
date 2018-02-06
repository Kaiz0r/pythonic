import os
import sys

dlpath = '/home/kaiz0r/.wine/drive_c/Deus Ex GOTY/OpenDX/Classes/'
fileext = ".uc"
dchkstr = "setWPActive"

foundnum = 0
foundstr = ""

try:
	dlpath = sys.argv[1]
except IndexError:
	pass

try:
	fileext = sys.argv[2]
except IndexError:
	pass
	
try:
	dchkstr = sys.argv[3]
except IndexError:
	pass
	
def dchk():
	global dlpath, dchkstr, fileext, foundnum, foundstr
	for file in os.listdir(dlpath):
		filename = os.fsdecode(file)
		if filename.endswith(fileext):
			print("Opening "+filename)
			with open(dlpath+filename, "rb") as fl:
				cont = str(fl.read(), "latin-1")
				if dchkstr in cont:
					print("Found in "+filename)
					foundnum += 1
					foundstr = foundstr+"\n"+filename
				else:
					print("Nope...")
			

print("Running script...")
print("Checking "+dlpath+" *"+fileext+" for "+dchkstr+"...")
dchk()
print(str(foundnum)+" files matched!\n"+foundstr)
input("Script complete. Press enter to close.")
