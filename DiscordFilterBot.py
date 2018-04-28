################# Discord Filter Bot                 #################
################# Version: 2.02                      #################
################# ---------------------------------- #################
################# Written by TheRadziu for Spoopy <3 #################
################# Only edit Settings below and       #################
################# selected blacklist_file itself     #################

### Settings ###
more_info = False # [True/False] If enabled displays more info on bot start.
reports = True # [True/False] If enabled sends a report about message being deleted [who posted it in which channel] to channel set below
reporting_channel_id = Channel_id_here # ID of the channel where reports will be sent. Needs reports set to True
bot_token = 'BOT TOKEN' # Paste your bot token here.
playing_status = 'PLAYING STATUS HERE' # Bot will display this as Playing status.
blacklist_file = 'blacklist.txt' # File with forbidden phrases, mainly used for banning certain domains from discord server.
reconnect_every_sec = 5 # on connection failure bot will try to reconnect every set amount of secounds.

############# Code Starts here - Do not touch #############
import asyncio
import platform
import time
from datetime import datetime
import ctypes

### Check if discord library is installed
try:
	import discord
except ImportError:
	print('Discord library is not installed! Please run this command to install it!:')
	print('python -m pip install -U discord.py')
	exit()

### Current date function
def current_time():
	ctime = datetime.now().strftime('[%H:%M:%S] ')
	return ctime

### Load and parse blacklist_file
bl_phrases =  set(open('./' + blacklist_file).read().split())
bl_phrases = list(map(lambda x: x.lower(), bl_phrases))

### Set window's title
ctypes.windll.kernel32.SetConsoleTitleW("FilterBot 2.0 by TheRadziu")

client = discord.Client()
already_connected = False


### On bot run:
@client.event
async def on_ready():
	global already_connected
	if not already_connected:
		print('\nWelcome to the FilterBot 2\n')
		print('Your selected banned phrases are:')
		print(bl_phrases)
		if more_info:
			print('--------')
			print('Current Discord.py Version: {} | Current Python Version: {}'.format(discord.__version__, platform.python_version()))
			print('--------')
			print('Use this link to invite {}:'.format(client.user.name))
			print('https://discordapp.com/oauth2/authorize?client_id={}&scope=bot&permissions=8'.format(client.user.id))
			print('--------')
			print(current_time() + 'Logged in as '+client.user.name+' (ID:'+client.user.id+') | Connected to '+str(len(client.servers))+' servers | Watching over '+str(len(set(client.get_all_members())))+' users')
		else: 
			print('--------')
			print(current_time() + 'Connected. Bot is now Online and Active.')
		already_connected = True
	else:
		print(current_time() + 'Successfuly reconnected!')
		
	#Set Playing as:
	return await client.change_presence(game=discord.Game(name=playing_status))

### Main Bot's code, everything happens in here
@client.event
async def on_message(message):
	if any(word in message.content.lower() for word in bl_phrases):
		###Report it to different channel and console if enabled:
		if reports:
			reporting_channel = client.get_channel("{}".format(reporting_channel_id))
			await client.send_message(destination=reporting_channel, content='Removed message by %s in channel #%s' % (message.author, message.channel))
		print(current_time() + 'Removed message - %s : %s' % (message.author, message.content))
		### Remove the message which triggered the bot	
		await client.delete_message(message)
		### Send reply/notification with mention
		mention = '{0.author.mention}'.format(message)
		await client.send_message(message.channel, 'Hey! ' + mention + ' Please do not link to anything containing copyright material!')
	elif message.content.startswith('???creator'):
		await client.send_message(message.channel, 'FilterBot 2 created by TheRadziu :joy:')

### Actually run the bot and try to reconnect on fail/disconnect
is_offline = False
while True:
	try:
		client.loop.run_until_complete(client.start(bot_token))
	except BaseException:
		if not is_offline:
			print(current_time() +'Disconnected! Attempting reconnect every {} seconds!'.format(reconnect_every_sec))
			is_offline = True
		time.sleep(reconnect_every_sec)
