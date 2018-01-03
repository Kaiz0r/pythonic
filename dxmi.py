import os
import patoolib

archives = 0
files = 0
dlpath = '/home/kaiz0r/Downloads/'
gamepath = '/home/kaiz0r/.wine/drive_c/Deus Ex GOTY/'

def open_archives():
	global archives
	for file in os.listdir(dlpath):
		filename = os.fsdecode(file)
		if filename.endswith(".zip"):
			archives += 1
			print("["+str(archives)+"] Running extraction tool on "+dlpath+filename)
			patoolib.extract_archive(dlpath+filename, outdir=dlpath)
			

def move_files():
	global files
	for file in os.listdir(dlpath):
		filename = os.fsdecode(file)
		if filename.endswith(".dx"):
			files += 1
			print("["+str(files)+"] Moving "+dlpath+filename+" -> "+gamepath+"Maps/"+filename)
			os.rename(dlpath+filename, gamepath+"Maps/"+filename)
		elif filename.endswith(".u") or filename.endswith(".ini") or filename.endswith(".int"): 
			files += 1
			print("["+str(files)+"] Moving "+dlpath+filename+" -> "+gamepath+"System/"+filename)
			os.rename(dlpath+filename, gamepath+"System/"+filename)
		elif filename.endswith(".utx"): 
			files += 1
			print("["+str(files)+"] Moving "+dlpath+filename+" -> "+gamepath+"Textures/"+filename)
			os.rename(dlpath+filename, gamepath+"Textures/"+filename)  
		elif filename.endswith(".uax"): 
			files += 1
			print("["+str(files)+"] Moving "+dlpath+filename+" -> "+gamepath+"Sounds/"+filename)
			os.rename(dlpath+filename, gamepath+"Sounds/"+filename) 
		elif filename.endswith(".umx"): 
			files += 1
			print("["+str(files)+"] Moving "+dlpath+filename+" -> "+gamepath+"Music/"+filename)
			os.rename(dlpath+filename, gamepath+"Music/"+filename) 

print("Running installation script...")
print("Variables -:")
print("Base path: "+dlpath)
print("Game path: "+gamepath)
print("-------------")
print("Checking archives...")
open_archives()
if archives > 0:
	print(str(archives)+" archives extracted.")
else:
	print("No archives found, moving on.")
print("Checking files...")
move_files()
if files > 0:
	print(str(files)+" files moved.")
else:
	print("No files found. Ending script.")
input("Press enter to close.")
