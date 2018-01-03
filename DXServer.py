import sys
import os
import notify2

notify2.init('Deus Ex Server')

def Notif(Summary, Text):
	n = notify2.Notification(Summary,
							 Text,
							 "C731_DXMeshTool.0"
							)
	n.show()

backupscriptpath = "/home/kaiz0r/projects/Python/" 
bUnixMode = True
servermap = "Funline_UnlimitedParty-3"
executablepath = '"C:\Deus Ex GOTY\System\deusex.exe"'
game = "OpenDX.Playground"
mutators = "mPack1.ModifyZoneInfo,mPack1.ModifyPlayerSettings,id.MutPlayerID"
logfile = "server.log"
unix_winecommand = "wine"

marg = ""
try:
	marg = sys.argv[1]
except IndexError:
	pass
	
def main():
	os.system("python3 "+backupscriptpath+"pyLogBackup.py -a")
	Notif("Launching server", "Initiating "+servermap)
	if bUnixMode is True:
		os.system(unix_winecommand+' '+executablepath+' '+servermap+'?Game='+game+'?Mutator='+mutators+' -server -LOG='+logfile+' > NUL')
	else:
		os.system(executablepath+' '+servermap+'?Game='+game+'?Mutator='+mutators+' -server -LOG='+logfile+' > NUL')

	#os.system('wine-development "C:\Deus Ex GOTY\System\deusex.exe" '+servermap+'?Game=OpenDX.OpenDX?Mutator=mPack1.ModifyZoneInfo,mPack1.ModifyPlayerSettings -server -LOG=server.log > NUL')

if __name__ == "__main__":
  #Run as main program
  main()
