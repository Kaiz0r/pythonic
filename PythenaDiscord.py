import discord
import asyncio
import sys
import subprocess
import os
import time
import urllib.request
import random
import socket
import zipfile
import datetime
from dice_notation.parser import DiceParser
from math import *
from bs4 import BeautifulSoup
import notify2

#Class instants
client = discord.Client()
ChatRoom = discord.Channel

#Constants
version = "180103"
changes = '''
180103 - New version control system/first git push.
180103.1 - Testing "No players found" response for !ping query
180103.2 - Finished the !ping update.
180107 - Testing MS update.
'''

#Variables
token = ""
note = ""
liststr = ""
BlockAIReason = ""
apass = ""

aiConvID = 0
uptimemins = 0
uptimehours = 0
statusvar = 0

bAlerting = False
bFoundPlayers = False
bFoundPlayersQ = False

def aNotify(title, text):
	n = notify2.Notification(title,text,"notification-message-im")
	n.show()
	
#======================
#Events
#======================
@client.event
async def on_ready():
	AddLog('Logged in as '+client.user.name+' ('+client.user.id+')')
	AddLog('------')
	notify2.init('Athena')
	AddLog("Notification daemon started...")
	aNotify("Athena", "The Athena client is ready.")
	AddLog("Running task: status")
	await client.loop.create_task(status_task())
	
@client.event
async def on_message_delete(message):
	if message.author.bot is False:
		AddLog(message.author.name+' deleted message: '+message.content)

@client.event
async def on_message_edit(before, after):
	if before.author.bot is False and before.content != after.content:
		AddLog(before.author.name+' edited their message...')
		AddLog('Previous: '+before.content)
		AddLog('Changed: '+after.content)

@client.event
async def on_member_update(before, after):
	#global defaultchannel
	if before.name != after.name:
		AddLog(before.name+' now known as ['+after.name+']')
	
#@client.event
#async def on_error(event):
#	AddLog("Error found: "+str(sys.exc_info()))
	
@client.event
async def on_member_join(member):
	AddLog(member.name+' joined '+member.server.name)
	
@client.event
async def on_member_remove(member):
	AddLog(member.name+' left '+member.server.name)
	
@client.event
async def on_message(message):
	owner = 'Kaiz0r#3628'
	global note
	global ChatRoom
	global bAlerting
	global bTimerRunning
	global apass
	global uptimemins, uptimehours
	global BlockAIReason
	#Making sure the bot doesn't respond to itself.
	if message.author == client.user:
		return
	
	if message.content.startswith('t!') and str(discord.utils.get(message.server.members, name='Tatsumaki').status) == "offline":
		await client.send_message(message.channel, "Woops, looks like that bot is offline. Try again later.")
		
	if message.content.startswith('!cmd'):
		await client.send_message(message.channel, '''
```
!roles > shows your list of roles.
!join (players/mappers/coders) > joins one of the set roles.
!leave (players/mappers/coders) > leaves one of the roles.
!timer > starts a query for timer. Respond to the bots questions to fill in the details.
!calc (query) > calculates the mathematical value.
!roll (dice notation) > rolls the dice, e.i. "2d6" rolls 2 6-sided dice.
!changes > shows bot change-log.
!ping > quick-check masterserver for online players. If no response, no players.
!list > prints current deusexnetwork server list.
!pullfile > starts a query for pulling a file from the host machine. Format: !pullfile <directory> <filename> Certain files are restricted.
!pull (opendx/rcon/partystuff) > like above, but a shortcut for most used files.
!search (site) (query) > searches (site) for (query), site can be currently dxn, tca, more engines to come. 
```''')
		await client.add_reaction(message, "🔍")
	#My personal to-do list regarding coding the bot.
	elif message.content.startswith('!todo'):
		await client.send_typing(message.channel)
		await client.send_message(message.channel, '```css\nBot coding list\n\n[1] Create a GUI for the host.\n[2] <COMPLETE>\n[3] Expand commands.\n[4] Smite Jhonny.\n[5] <COMPLETE>\n[6] <COMPLETE> \n[7] <COMPLETE>\n[8] <COMPLETE>\n[9] <COMPLETE>\n[10] Add a blackjack game?```')
		await client.add_reaction(message, "🔍")
	
	#Shows the users current roles
	elif message.content.startswith('!roles'):
		await client.send_typing(message.channel)
		role_names = [role.name for role in message.author.roles]
		i = 0
		
		while i < (len(role_names) - 1):
			if "everyone" in role_names[i]:
				role_names[i] = "lurker"
			i += 1
				
		await client.send_message(message.channel, 'Your current roles: '+', '.join(role_names)+'\nTo join one of the joinable roles, use command `!join <role name>`.\nTo leave a role, use the command `!leave <role name>`\nOnce in that role, you will get notified if someone mentions that role name.\nCurrent joinable roles include `coders`, `mappers`, `players`, `artists`.')
		await client.add_reaction(message, "🔍")
	
	elif message.content.startswith('!except'):
		await exception(message)
		
	elif message.content.startswith('!status'):
		await client.send_message(message.channel, 'The bot is ('+str(discord.utils.get(message.server.members, name='Tatsumaki').status)+')')
			
	#Adds user to the role.	
	elif message.content.startswith('!join'):
		await client.send_typing(message.channel)
		rolename = message.content[6:]
		if rolename == "players" or rolename == "coders" or rolename == "mappers" or rolename == "artists" or rolename == "test":
			role_names = [role.name for role in message.author.roles]
			if rolename in role_names:
				await client.send_message(message.channel, "Already in that role.")
				await client.add_reaction(message, "⛔")
				return
					
			roleid = discord.utils.get(message.server.roles, name=rolename)
			await client.add_roles(message.author, roleid)
			await client.send_message(message.channel, "Added "+message.author.mention+" to role **"+roleid.name+"**")
			await client.add_reaction(message, "✅")
		else:
			await client.send_message(message.channel, "Sorry, not an accepted joinable role.")
			await client.add_reaction(message, "⛔")
	
	#Removes user from the role.		
	elif message.content.startswith('!leave'):
		await client.send_typing(message.channel)
		rolename = message.content[7:]
		if rolename == "players" or rolename == "coders" or rolename == "mappers" or rolename == "artists" or rolename == "test":

			role_names = [role.name for role in message.author.roles]
			if rolename not in role_names:
				await client.send_message(message.channel, "Not in that role.")
				await client.add_reaction(message, "⛔")
				return
				
			roleid = discord.utils.get(message.server.roles, name=rolename)
			await client.remove_roles(message.author, roleid)
			await client.send_message(message.channel, "Removed "+message.author.mention+" to role **"+roleid.name+"**")
			await client.add_reaction(message, "✅")
										
	#Initiates timer requests, the bot will edit the original request message to ask for the other variables, and then start the timer task.
	elif message.content.startswith('!timer'):
		await client.send_typing(message.channel)
		command = message.content.split(" ")[0]
		time = message.content.split(" ")[1]
		msgt = message.content.split(" ")[2:]
		bAlerting = False
		await client.send_message(message.channel, 'Setting task...')
		client.loop.create_task(timer_task(message.channel, message.author, time.split(":")[0], time.split(":")[1], ' '.join(msgt), False))
		await client.add_reaction(message, "⌚")
		
	elif message.content.startswith('!remindme'):
		command = message.content.split(" ")[0]
		time = message.content.split(" ")[1]
		sm = message.content.split(" ")[2:]
		print("Command: "+command)
		print("Time: "+str(time))
		print("Message: "+' '.join(sm))
		bTimerRunning=False
		client.loop.create_task(wait_task(message.channel, message.author, time, ' '.join(sm)))
		
	#Evaluates the string as a calculation.
	elif message.content.startswith('!calc '):
		await client.send_typing(message.channel)
		await client.send_message(message.channel, message.content[6:]+'? I believe that is '+str(eval(message.content[6:])))
		await client.add_reaction(message, "🔣")
	
	#Evaluates the dice notation format (2d6 meaning 2 6-sided dice) for example.
	elif message.content.startswith('!roll '):
		await client.send_typing(message.channel)
		parser = DiceParser()
		dice = parser.parse(message.content[6:])
		result = dice.roll()
		await client.send_message(message.channel, 'You rolled '+str(result))
		await client.add_reaction(message, "🎲")
	
	elif message.content.startswith('!search'):
		await client.send_typing(message.channel)
		if message.content[8:11] == "dxn":
			result = ""
			lin = 0
			lmsg = await client.send_message(message.channel, '**Searching DeusExNetwork for '+message.content[12:]+'...**')
			try:
				result =  urllib.request.urlopen('http://deusexnetwork.com/files?q='+message.content[12:])
			except:
				exception(message)
			outp = BeautifulSoup(result, 'html.parser')
			fp = '**'+outp.title.string+'**\nSearch result for: '+message.content[12:]
			for link in outp.find_all('a'):
				lstr = link.get('href')
				if '/files/' in lstr and '/upload' not in lstr:
					fp = fp+'\nhttp://deusexnetwork.com'+lstr+' ('+outp.find_all('em')[lin].string+')'
					await client.edit_message(lmsg, fp)
					lin += 1
			
			if lin == 0 and lmsg.content == '**Searching DeusExNetwork for '+message.content[12:]+'...**':
				await client.edit_message(lmsg, "No results found for "+message.content[12:]+".")
				await client.add_reaction(message, "⛔")
			else:
				await client.add_reaction(message, "✅")
		elif message.content[8:11] == "tca":
			result = ""
			lin = 0
			lmsg = await client.send_message(message.channel, '**Searching TC Archive for '+message.content[12:]+'...**\n*Note: Connection to this service can be slow.*')
			try: # http://deusex.ucoz.net/search/?q='+message.content[12:]+'&m=load&t=0
				result =  urllib.request.urlopen('http://deusex.ucoz.net/search/?q='+message.content[12:]+'&m=load&t=0')
			except:
				exception(message)
			outp = BeautifulSoup(result, 'html.parser')
			fp = '**'+outp.title.string+'**\nSearch result for: '+message.content[12:]
			for link in outp.find_all('a'):
				lstr = link.get('href')
				if 'deusex.ucoz.net/load/' in lstr:
					fp = fp+'\n'+lstr
					await client.edit_message(lmsg, fp)
					lin += 1
			
			if lin == 0 and lmsg.content == '**Searching TC Archive for '+message.content[12:]+'...**\n*Note: Connection to this service can be slow.*':
				await client.edit_message(lmsg, "No results found for "+message.content[12:]+".")
				await client.add_reaction(message, "⛔")
			else:
				await client.add_reaction(message, "✅")
		else:
			await client.send_message(message.channel, "No service found for "+message.content.split(" ")[1]+"...")	
				
	#Empties the log file.
	elif message.content.startswith('!purgelog'):
		if str(message.author) == owner:
			await client.send_typing(message.channel)
			lmsg = await client.send_message(message.channel, 'Purging...')
			try:
				with open("/home/kaiz0r/PythenaDiscord/sys.log", "w") as fl:
					fl.writelines("")
					fl.close()
					await client.edit_message(lmsg, "Log purged.")
					await client.add_reaction(message, "🔍")
			except:
				await client.edit_message(lmsg, "Purge failed...")
				await client.add_reaction(message, "⛔")
	
	#Prints the log file in to chat, useful for quick access.
	elif message.content.startswith('!logprint'):
		await client.send_typing(message.channel)
		lmsg = await client.send_message(message.channel, 'Reading...')
		try:
			with open("/home/kaiz0r/PythenaDiscord/sys.log", "r") as fl:
				await client.edit_message(lmsg, str(fl.read()))
				fl.close()
				await client.add_reaction(message, "🔍")
		except:
			await client.edit_message(lmsg, "Read failed...")
			await client.add_reaction(message, "⛔")
	
	#Says version message and changelog.
	elif message.content.startswith('!changes'):
		await client.send_typing(message.channel)
		await client.send_message(message.channel, '```\nAthena v'+version+'\n\n'+changes+'```')
		await client.add_reaction(message, "🔍")
	
	#Quick masterserver ping for Deus Ex and responds with any server names that have players online.
	elif message.content.startswith('!ping'):
		await client.send_typing(message.channel)
		await client.add_reaction(message, "🔍")
		await msq(message.channel, False)
	
	#Slower masterserver check which lists ALL servers found.
	elif message.content.startswith('!list'):
		await client.send_typing(message.channel)
		await client.add_reaction(message, "🔍")
		await msq(message.channel, True)
	
	#Says the bot information.			
	elif message.content.startswith('!athena'):
		await client.send_typing(message.channel)
		majorv = str(sys.version_info)[23:24]
		minorv = str(sys.version_info)[32:33]
		microv = str(sys.version_info)[41:42]
		realver = majorv+'.'+minorv+'.'+microv
		#releasev = str(sys.version_info)[41:42]
		#print(majorv+'.'+minorv+'.'+microv)
		await client.send_message(message.channel, 'I am '+client.user.mention+' '+version+', A WIP Python based Discord bot by '+discord.utils.get(message.server.members, name='Kaiz0r').mention+'\nI am an open-source bot, use command `!pull source` to view the code.\n```Python Version:'+realver+' \nAPI Version: '+discord.__version__+' \n\nLibraries: BeautifulSoup Text Parser, math, dice_notation, datetime, socket, random, urllib, time, os, subprocess, sys, asyncio, discord```')
		await client.add_reaction(message, "🔍")

	#Responds with the note variable..	
	elif message.content.startswith('!checknote'):
		await client.send_typing(message.channel)
		await client.send_message(message.channel, ''+note.content+'')
		
	#Saves the response to a note.
	elif message.content.startswith('!note'):
		await client.send_typing(message.channel)
		await client.send_message(message.channel, 'Say your note.')

		note = await client.wait_for_message(timeout=5.0, author=message.author)
		if note is None:
			await client.send_message(message.channel, 'Problem there, nothing recorded?')
	
	elif message.content.startswith('!block'):
		if str(message.author) == owner:
			await client.send_typing(message.channel)
			msgt = message.content.split(" ")[1:]
			BlockAIReason = ' '.join(msgt)
			await client.send_message(message.channel, 'Setting AI Block: '+BlockAIReason)
		else:
			await client.send_message(message.channel, 'Access denied.')
			
	#Sets various properties.	
	elif message.content.startswith('!set'):
		if str(message.author) == owner:
			svar = message.content.split(" ")[1]
			sprop = ' '.join(message.content.split(" ")[2:])
			await client.send_typing(message.channel)
			
			if svar == 'status ':
				await client.change_presence(game=discord.Game(name=sprop))
				await client.add_reaction(message, "✅")
				await client.send_message(message.channel, message.author.mention+' Status changed to '+sprop)
			
			if svar == 'block':
				BlockAIReason = sprop
				await client.add_reaction(message, "✅")
				if sprop == "":
					await client.send_message(message.channel, 'Ending AI Block.')
				else:
					await client.send_message(message.channel, 'Setting AI Block: '+BlockAIReason)
		else:
			await client.send_message(message.channel, message.author.mention+' Access denied.')
			await client.add_reaction(message, "⛔")
	
	elif message.content.startswith('!uptime'):
		if uptimehours == 0:
			await client.send_message(message.channel, "Current uptime is "+str(uptimemins)+" minutes.")
		else:
			await client.send_message(message.channel, "Current uptime is "+str(uptimehours)+" hours and "+str(uptimemins)+" minutes.")
			
	elif message.content.startswith('!pullfile'):
		command = message.content.split(" ")[0]
		directory = message.content.split(" ")[1]
		rawfilename = message.content.split(" ")[2:]
		filename = ' '.join(rawfilename)
		
		if(filename.endswith(".ini") and str(message.author) != owner):
			await client.send_message(message.channel, 'Access to this file is denied.\n**Reason**: Denied by pattern (*.ini) for security reasons.')
			AddLog("Access denied to "+message.author.name+": "+filename)
		else:
				AddLog("Scanning file...")
				try:
					statinfo = os.stat('/home/kaiz0r/.wine/drive_c/Deus Ex GOTY/'+directory+'/'+filename)
					if isover9mb(statinfo.st_size) is True:
						await client.send_message(message.channel, 'File was too large. ('+byteconv(statinfo.st_size)+') Discords file sending limits are 9 MB.\nPlease request that '+discord.utils.get(message.server.members, name='Kaiz0r').mention+' ('+str(discord.utils.get(message.server.members, name='Kaiz0r').status)+') zips up that file first.\n**Note**: At some point in the future this might become automated, but for now, no.')
						await client.add_reaction(message, "⛔")
						return
					else:
						await client.send_message(message.channel, 'File is currently being fetched from the host. Please wait, this could take time depending on the file size.\n/home/kaiz0r/.wine/drive_c/Deus Ex GOTY/'+directory+'/'+filename+' ('+byteconv(statinfo.st_size)+')')
						await client.add_reaction(message, "🔍")
				
					try:
						await client.send_file(message.channel, "/home/kaiz0r/.wine/drive_c/Deus Ex GOTY/"+directory+"/"+filename)
						AddLog("File sent to "+message.author.name+": /home/kaiz0r/.wine/drive_c/Deus Ex GOTY/"+directory+"/"+filename)
						await client.add_reaction(message, "✅")
					except FileNotFoundError:
						await client.send_message(message.channel, 'File not found... Try checking the name again. \n**Note**: Values are *case-sensative*!')
						await client.add_reaction(message, "⛔")
					except discord.errors.HTTPException:
						await client.send_message(message.channel, 'File was too large. Please request that '+discord.utils.get(message.server.members, name='Kaiz0r').mention+' ('+str(discord.utils.get(message.server.members, name='Kaiz0r').status)+') zips up that file first.\n**Note**: At some point in the future this might become automated, but for now, no.')
						await client.add_reaction(message, "⛔")
					except:
						await exception(message)
				except FileNotFoundError:
					await client.send_message(message.channel, 'File not found... Try checking the name again. \n**Note**: Values are *case-sensative*!')
					await client.add_reaction(message, "⛔")
				except:
					await exception(message)
					
	#Like pullfile except pre-set files.					
	elif message.content.startswith('!pull'): #/system/
		cutstr = message.content[6:]
		await client.send_typing(message.channel)
		if(message.content[6:] == 'opendx'):
			await client.send_file(message.channel, "/home/kaiz0r/.wine/drive_c/Deus Ex GOTY/System/OpenDX.u")
			AddLog("File pulled by "+message.author.name+": /home/kaiz0r/.wine/drive_c/Deus Ex GOTY/System/OpenDX.u")
			await client.add_reaction(message, "✅")
		if(message.content[6:] == 'rcon'):
			await client.send_file(message.channel, "/home/kaiz0r/.wine/drive_c/Deus Ex GOTY/System/RCON.u")
			AddLog("File pulled by "+message.author.name+": /home/kaiz0r/.wine/drive_c/Deus Ex GOTY/System/RCON.u")
			await client.add_reaction(message, "✅")
		if(message.content[6:] == 'partystuff'):
			await client.send_file(message.channel, "/home/kaiz0r/.wine/drive_c/Deus Ex GOTY/System/PartyStuff.u")
			AddLog("File pulled by "+message.author.name+": /home/kaiz0r/.wine/drive_c/Deus Ex GOTY/System/PartyStuff.u")
			await client.add_reaction(message, "✅")
		if(message.content[6:] == 'log'):
			await client.send_file(message.channel, "/home/kaiz0r/PythenaDiscord/sys.log")
			AddLog("File pulled by "+message.author.name+": /home/kaiz0r/PythenaDiscord/sys.log")
			await client.add_reaction(message, "✅")
		if(message.content[6:] == 'source'):
			await client.send_file(message.channel, "/home/kaiz0r/PythenaDiscord/PythenaDiscord.py")
			AddLog("File pulled by "+message.author.name+": /home/kaiz0r/PythenaDiscord/PythenaDiscord.py")
			await client.add_reaction(message, "✅")
	
	elif message.content.startswith('!finger'):
		await client.send_typing(message.channel)
		await client.send_file(message.channel, "/home/kaiz0r/Downloads/.f/stuff-2/Pics & FUN!/Planet Deus Ex/fifth ending.jpg")
		await client.add_reaction(message, "✅")

	elif message.content.startswith('!giggle'):
		await client.send_typing(message.channel)
		await client.send_file(message.channel, "/home/kaiz0r/Downloads/.f/giggle.png")
		await client.add_reaction(message, "✅")
				
	elif message.content.startswith('!files'):
		reqdirectory = message.content[7:]
		await client.add_reaction(message, "🔍")
		await list_files(message, reqdirectory)
			
	#Forces the bot to say what you enter.
	elif message.content.startswith('!say'): #owner
		if str(message.author) == owner:
			await client.send_typing(message.channel)
			await client.send_message(message.channel, message.content[5:])
			AddLog("Remoted "+message.content[5:])
	
	#Sets the current room as the "Chat Room" which enables the AI auto-responder
	elif message.content.startswith('!ai.setroom'): #owner
		if str(message.author) == owner:
			ChatRoom = message.channel
			await client.send_message(ChatRoom, "Set auto-reply to this room.")
	
	#Cancels the above command.
	elif message.content.startswith('!ai.clearroom'): #owner
		if str(message.author) == owner:
			ChatRoom = None
			await client.send_message(ChatRoom, "Cleared auto-reply...")	
	
	#Closes the current AI session, resetting the conversation ID.
	elif message.content.startswith('!ai.disconnect'): #owner
		global aiConvID
		if aiConvID != 0 and str(message.author) == owner:
			await client.send_typing(message.channel)
			msgc = await client.send_message(message.channel, message.author.mention+' Closing conversation instance...')
			AddLog("AI Parser - Sending disconnect signal...")
			urllib.request.urlopen('https://www.botlibre.com/rest/api/form-chat?instance=19852766&application=6164811714561807251&conversation='+str(aiConvID)+'&disconnect=true')
			await client.edit_message(msgc,message.author.mention+" Closed conversation instance.")
			aiConvID = 0
		
	elif message.content.startswith('!watchtime'):
		await client.loop.create_task(status_task())
	#Logs the bot out of discord completely and shuts down the script.	
	elif message.content.startswith('!shutdown'): #owner
		await client.send_typing(message.channel)
		sdt = 5
		if str(message.author) == owner:
			msg = await client.send_message(message.channel, message.author.mention+' Shutting down in 5 seconds.')
			
			while sdt != -1:
				await asyncio.sleep(1)
				sdt -= 1
				await client.edit_message(msg, message.author.mention+' Shutting down in '+str(sdt)+' seconds.')
				if sdt == 0:
					await client.close()
					break
		else:
			await client.send_message(message.channel, message.author.mention+' Access denied.')		
	
	#Trigger for the AI.
	elif message.content.startswith('athena, ') or message.content.startswith('Athena, '):
		await queryAI(message, 1)
			
	elif message.channel is ChatRoom:
		await queryAI(message, 0)		
			
	elif message.content.startswith(client.user.mention): #<@384007758527332363>
		await queryAI(message, 2)

#======================
#Async Functions
#======================
async def queryAI(message, amode):
	global aiConvID, BlockAIReason
	
	await client.send_typing(message.channel)
	
	if BlockAIReason != "":
		await client.send_message(message.channel, 'Chat is currently disabled.\nReason: '+BlockAIReason)
		await client.add_reaction(message, "⛔")
		return
		
	if amode == 0: #Send full raw message
		bmsg = message.content
	elif amode == 1: #Cutting the "athena, " part
		bmsg = message.content[8:]
	elif amode == 2: #Cutting the athena mention string
		bmsg = message.content[22:]
		
		#https://www.botlibre.com/rest/api/form-chat?instance=19852766&message=hello&application=6164811714561807251
	bmsg = bmsg.replace(" ", "%20")
	AddLog("AI Parser - Sending: "+bmsg)
	#global aiConvID
	if aiConvID == 0: #New conversation starting
		cmsg = await client.send_message(message.channel, 'New conversation instance, generating new conversation ID...')
		if "?" in message.content:
			try:
				result =  urllib.request.urlopen('https://www.botlibre.com/rest/api/form-chat?user=DiscordUser&password='+apass+'&instance=19852766&message='+bmsg+'&application=6164811714561807251&includeQuestion=true')
			except UnicodeEncodeError:
				await client.send_message(message.channel, message.author.mention+' That request returned an encoding error. Please use plaintext only while communicating.')
				await client.add_reaction(message, "⛔")
				return
			except: 
				await exception(message)
				return
		else:
			try:
				result =  urllib.request.urlopen('https://www.botlibre.com/rest/api/form-chat?user=DiscordUser&password='+apass+'&instance=19852766&message='+bmsg+'&application=6164811714561807251')
			except UnicodeEncodeError:
				await client.send_message(message.channel, message.author.mention+' That request returned an encoding error. Please use plaintext only while communicating.')
				await client.add_reaction(message, "⛔")
			except: 
				await exception(message)
				return
		soup = BeautifulSoup(result, 'html.parser')
		soupf = soup.message.string.replace("<br/>", "\n")
		AddLog(soup.response['conversation']+" ["+soup.response['emote']+"]- Conversation parsed: "+soupf)
		aiConvID = soup.response['conversation']
		await client.edit_message(cmsg, 'New conversation instance, new conversation ID is '+aiConvID)
		await client.send_message(message.channel, message.author.mention+' '+soupf)
		await client.add_reaction(message, "💬")
	else:
		if "?" in message.content:
			try:
				result =  urllib.request.urlopen('https://www.botlibre.com/rest/api/form-chat?user=DiscordUser&password='+apass+'&instance=19852766&message='+bmsg+'&application=6164811714561807251&conversation='+str(aiConvID)+'&includeQuestion=true')
			except UnicodeEncodeError:
				await client.send_message(message.channel, message.author.mention+' That request returned an encoding error. Please use plaintext only while communicating.')
				await client.add_reaction(message, "⛔")
			except: 
				await exception(message)
				return
		else:
			try:
				result =  urllib.request.urlopen('https://www.botlibre.com/rest/api/form-chat?user=DiscordUser&password='+apass+'&instance=19852766&message='+bmsg+'&application=6164811714561807251&conversation='+str(aiConvID))
			except UnicodeEncodeError:
				await client.send_message(message.channel, message.author.mention+' That request returned an encoding error. Please use plaintext only while communicating.')
				await client.add_reaction(message, "⛔")
			except: 
				await exception(message)
				return
		soup = BeautifulSoup(result, 'html.parser')
		soupf = soup.message.string.replace("<br/>", "\n")
		AddLog(soup.response['conversation']+" ["+soup.response['emote']+"]- Conversation parsed: "+soupf)
		await client.send_message(message.channel, message.author.mention+' '+soupf)
		await client.add_reaction(message, "💬")

async def queryNormalDeusExServer(ip, port, channel):
	global bFoundPlayersQ
	try:
		particularQuery = "\\info\\"
		sockUDP = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		sockUDP.settimeout(1.0)
		sockUDP.sendto(bytes(particularQuery,"utf-8"), (ip, port))
		#sockUDP.sendto(b'particularQuery', (ip, port))
		data = sockUDP.recvfrom(2048) # buffer size is 2048 bytes
		shostname = data[0].split(b'\\hostname\\')[1].split(b'\\hostport\\')[0]
		playernum = data[0].split(b'\\maxplayers\\')[0].split(b'\\numplayers\\')[1]
		AddLog("Received message ::: "+str(data[0],"latin-1"))
		AddLog("Host name :::"+str(shostname,"latin-1"))
		AddLog("Players::: "+str(playernum,"latin-1"))
		shostx = str(shostname,"latin-1")
		if(int(playernum) == 1):
			await client.send_message(channel, "There is "+str(playernum,"latin-1")+" player online on "+str(shostname,"latin-1") )
			bFoundPlayersQ=True
		elif(int(playernum) > 1):
			await client.send_message(channel, "There is "+str(playernum,"latin-1")+" players online on "+str(shostname,"latin-1") )
			bFoundPlayersQ=True
		sockUDP.close()

	except:
		AddLog("This server did not respond our query ::: "+ip+":"+str(port)+" Reason: "+str(sys.exc_info()[0])+" :: "+str(sys.exc_info()[1]))

	return
async def queryListDeusExServer(ip, port, qmessage):
	try:
		particularQuery = "\\info\\"
		sockUDP = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		sockUDP.settimeout(1.0)
		sockUDP.sendto(bytes(particularQuery,"utf-8"), (ip, port))
		#sockUDP.sendto(b'particularQuery', (ip, port))
		data = sockUDP.recvfrom(2048) # buffer size is 2048 bytes
		shostname = data[0].split(b'\\hostname\\')[1].split(b'\\hostport\\')[0]
		playernum = data[0].split(b'\\maxplayers\\')[0].split(b'\\numplayers\\')[1]
		maxplayers = data[0].split(b'\\gamemode\\')[0].split(b'\\maxplayers\\')[1]
		gametype = data[0].split(b'\\numplayers\\')[0].split(b'\\gametype\\')[1]
		mapname = data[0].split(b'\\gametype\\')[0].split(b'\\mapname\\')[1]

		print(str(data[0], "latin-1"))

		if "password\True" in str(data[0], "latin-1"):
			lstr = "🔒"
		else:
			lstr = ""
		global liststr
		liststr += "\n\n"+lstr+" Host: "+str(shostname,"latin-1")+" ("+str(playernum,"latin-1")+"/"+str(maxplayers,"latin-1")+")  Map: "+str(mapname,"latin-1")+"  Game: "+str(gametype,"latin-1")

		await client.edit_message(qmessage, "```css\n"+liststr+"```")

		sockUDP.close()
			
	except:
		AddLog("This server did not respond our query... "+ip+":"+str(port)+" Reason: "+str(sys.exc_info()[0])+" :: "+str(sys.exc_info()[1]))
		liststr += "\n\n @ "+str(sys.exc_info()[1])+" :: "+ip+":"+str(port)
		await client.edit_message(qmessage, "```css\n"+liststr+"```")
		
	return
	
async def msq(channel, bListAll):
	global bFoundPlayersQ
	bFoundPlayersQ=False
	sockTCP = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	masterServerAddress = ('master.deusexnetwork.com', 28900)
	masterServerAuth = '\\gamename\\deusex\\location\\0\\validate\\FZcjB4YA\\final\\'
	masterServerQuery = '\\list\\\\gamename\\deusex\\final\\'
	
	if bListAll is True:
		global liststr
		liststr = ""
		mmy = await client.send_message(channel, "===SCANNING===")
	else:
		await client.send_message(channel, "Pinging `"+str(masterServerAddress)+"` for players...")
	AddLog("Connecting to "+str(masterServerAddress)+"...")
	sockTCP.connect(masterServerAddress)
	try:
		AddLog("Sending authentication ::: "+masterServerAuth)
		sockTCP.sendall(bytes(masterServerAuth,"utf-8"))

		data = sockTCP.recv(1024)
		AddLog("Received ack ::: "+str(data,"latin-1"))

		AddLog("Sending query to master server ::: "+masterServerQuery)
		sockTCP.sendall(bytes(masterServerQuery,"utf-8"))

		data = sockTCP.recv(4096)
		AddLog("Received answer ::: "+str(data,"latin-1"))

		arr = str(data).split('\\\\')

		for i in arr:
			pos = str(i)
			svr = pos.split(':')
			if len(svr) == 2:
				if bListAll is True:
					await queryListDeusExServer(svr[0],int(svr[1]), mmy)
				else:
					await queryNormalDeusExServer(svr[0],int(svr[1]), channel)
		if bListAll is False and bFoundPlayersQ is False:
			await client.send_message(channel, "No players found.")
	finally:
		sockTCP.close()

async def list_files(message, subdir):
	
	listr = await client.send_message(message.channel, 'Checking...')
	dlpath = '/home/kaiz0r/.wine/drive_c/Deus Ex GOTY/'+subdir+'/'
	filelist = ""
	ilines = 0
	
	for file in os.listdir(dlpath):
		filename = os.fsdecode(file)
		if filename.endswith(".dx") or filename.endswith(".umx") or filename.endswith(".u") or filename.endswith(".ini") or filename.endswith(".int") or filename.endswith(".utx") or filename.endswith(".uax") or filename.endswith(".uc"): 
			ilines += 1
			if ilines == 50:
				ilines = 0
				filelist = filelist+"\n"+filename
				await client.send_message(message.channel, filelist)
				filelist = ""
			else:
				filelist = filelist+"\n"+filename

				
	try:
		await client.send_message(message.channel, filelist)
		await client.add_reaction(message, "🔍")
	except discord.errors.HTTPException:
		await client.send_message(message.channel, 'No files were found.')
		await client.add_reaction(message, "⛔")
	except:
		await exception(message)
	
async def exception(message):
	await client.send_message(message.channel, 'That command returned an uncaught error (An error with no programmed response) and the following error code has been returned.\n'+discord.utils.get(message.server.members, name='Kaiz0r').mention+' ('+str(discord.utils.get(message.server.members, name='Kaiz0r').status)+') has been notified.\n```'+str(sys.exc_info()[0])+'\n'+str(sys.exc_info()[1])+'```')
	AddLog("EXCEPTION UNHANDLED: "+str(sys.exc_info()[0]))
	AddLog("EXCEPTION UNHANDLED: "+str(sys.exc_info()[1]))
	aNotify("Athena", "There was an error in the code...\n"+str(sys.exc_info()[0])+"\n"+ str(sys.exc_info()[1]))
	await client.add_reaction(message, "‼")
	
#======================
#Utility Functions
#======================
def equal(a, b):
    try:
        return a.lower() == b.lower()
    except AttributeError:
        return a == b
        		
def AddLog(logmsg):
	try:
		with open("/home/kaiz0r/PythenaDiscord/sys.log", "r+") as f:
			now = datetime.datetime.now()
			mt = f.read()
			#f.writelines(str(now.day)+"/"+str(now.month)+"/"+str(now.year)+": "+logmsg+"\n")
			f.writelines(now.strftime("%Y-%m-%d %H:%M:%S")+": "+logmsg+"\n")
			f.close()
			print(now.strftime("%Y-%m-%d %H:%M:%S")+": "+logmsg)
	except FileNotFoundError:
		print("FAILED TO LOG - Log file not found. Create sys.log.")

def byteconv(number_of_bytes):
    if number_of_bytes < 0:
        raise ValueError("!!! numberOfBytes can't be smaller than 0 !!!")

    step_to_greater_unit = 1024.

    number_of_bytes = float(number_of_bytes)
    unit = 'bytes'

    if (number_of_bytes / step_to_greater_unit) >= 1:
        number_of_bytes /= step_to_greater_unit
        unit = 'KB'

    if (number_of_bytes / step_to_greater_unit) >= 1:
        number_of_bytes /= step_to_greater_unit
        unit = 'MB'

    if (number_of_bytes / step_to_greater_unit) >= 1:
        number_of_bytes /= step_to_greater_unit
        unit = 'GB'

    if (number_of_bytes / step_to_greater_unit) >= 1:
        number_of_bytes /= step_to_greater_unit
        unit = 'TB'

    precision = 1
    number_of_bytes = round(number_of_bytes, precision)

    return str(number_of_bytes) + ' ' + unit

def isover9mb(number_of_bytes):
	if number_of_bytes < 0:
		raise ValueError("!!! numberOfBytes can't be smaller than 0 !!!")

	step_to_greater_unit = 1024.

	number_of_bytes = float(number_of_bytes)
	unit = 'bytes'

	if (number_of_bytes / step_to_greater_unit) >= 1:
		number_of_bytes /= step_to_greater_unit
		unit = 'KB'

	if (number_of_bytes / step_to_greater_unit) >= 1:
		number_of_bytes /= step_to_greater_unit
		unit = 'MB'

	if (number_of_bytes / step_to_greater_unit) >= 1:
		number_of_bytes /= step_to_greater_unit
		unit = 'GB'

	if (number_of_bytes / step_to_greater_unit) >= 1:
		number_of_bytes /= step_to_greater_unit
		unit = 'TB'

	precision = 1
	number_of_bytes = round(number_of_bytes, precision)

	if 'GB' in unit:
		return True
	elif 'MB' in unit:
		if number_of_bytes > 9:
			return True
	else:
		return False
    
#======================
#Background Tasks
#======================
async def wait_task(channel, senderuser, timewait, message):
	global bTimerRunning
	
	while not client.is_closed and bTimerRunning is False:
		sw = timewait*60
		print("Waiting for "+timewait+" minutes, or "+sw+" seconds.")
		await client.send_message(channel, "Timer set for "+timewait+" minutes.")
		await asyncio.sleep(int(sw))
		await client.send_message(channel, senderuser.mention+message)
		bTimerRunning=True

async def timer_task(channel, senderuser, timehour, timemins, message, bAll):
	#  await client.wait_until_ready()
	global bAlerting
	
	while not client.is_closed and bAlerting is False:
		await asyncio.sleep(60) # task runs every 60 seconds
		now = datetime.datetime.now()
		print("Checking "+now.strftime("%H")+":"+now.strftime("%M")+" against "+timehour+":"+timemins+" for "+message)
		if now.strftime("%M") == timemins and now.strftime("%H") == timehour:
			bAlerting = True
			await client.send_message(channel, senderuser.mention+' '+message)
			
async def status_task():
	while not client.is_closed:
		global statusvar, uptimemins, uptimehours
	
		statusvar += 1
		if statusvar == 0:#if statusvar % 2 == 0:
			await client.change_presence(game=discord.Game(name="Uptime: "+str(uptimehours)+"h, "+str(uptimemins)+"m"))
		elif statusvar == 1:
			now = datetime.datetime.now()
			await client.change_presence(game=discord.Game(name="Time: "+now.strftime("%H")+":"+now.strftime("%M")+" GMT"))
		elif statusvar == 2:
			if BlockAIReason == "":
				await client.change_presence(game=discord.Game(name="AI ONLINE"))
			else:
				await client.change_presence(game=discord.Game(name="AI OFFLINE"))
			statusvar = -1
			
		await asyncio.sleep(60) # task runs every 60 seconds
		uptimemins += 1
		if uptimemins == 60:
			uptimemins = 0
			uptimehours += 1
			
	 	
#======================
#Script initiation
#======================
try:
	with open('/home/kaiz0r/PythenaDiscord/token.txt', "r") as f:
		AddLog("Opening token file....")
		token = f.readline().strip()
		try:
			with open('/home/kaiz0r/PythenaDiscord/password1.txt', "r") as f:
				AddLog("Opening password file....")
				apass = f.readline().strip()
				f.close()
		except:
			AddLog("Error reading password file...")
			
		f.close()
		client.run(token)
		
except:
	AddLog("Error reading token file...")


#client.run(token)
