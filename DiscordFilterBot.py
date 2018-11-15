################# Written by TheRadziu for Spoopy <3 #################
################# Script Version: 2.04               #################

import asyncio
import platform
import time
from datetime import datetime
import os, os.path
import configparser

### Current date function
def current_time():
	ctime = datetime.now().strftime('[%H:%M:%S] ')
	return ctime

### Check if discord library is installed
try:
	import discord
except ImportError:
	print('Discord library is not installed! Please run this command to install it!:')
	print('python -m pip install -U discord.py')
	exit()
	
### Check if config.ini exists
if os.path.isfile('config.ini') and os.path.getsize('config.ini') > 0:
	pass
else:
	print(current_time() + 'ERROR! config.ini file is missing or empty!')
	quit()

### Load external configuration file
config = configparser.ConfigParser(allow_no_value=True)
try:
	config.read('config.ini')
except Exception as err:
	print(current_time() + 'ERROR! config.ini file is corrupted!')
	quit()

### Load and parse blacklist
bl_phrases = [option for option in config['BLACKLIST']]

### Set window's title on windows machines
if os.name == 'nt':
	import ctypes
	ctypes.windll.kernel32.SetConsoleTitleW("FilterBot 2 by TheRadziu")

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
		if config.getboolean('SETTINGS', 'more_info'):
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
		
	#Set Playing as if not disabled:
	if config['SETTINGS']['playing_status'] != 'off':
		return await client.change_presence(game=discord.Game(name=config['SETTINGS']['playing_status']))
	else:
		await client.change_presence(game=None)

### Main Bot's code, everything happens in here
@client.event
async def on_message(message):
	if message.author == client.user:
		return
	if any(word in message.content.lower() for word in bl_phrases):
		###Report it to different channel and console if enabled:
		if config.getboolean('SETTINGS', 'reports'):
			reporting_channel = client.get_channel("{}".format(config['SETTINGS']['reporting_channel_id']))
			await client.send_message(destination=reporting_channel, content='Message from %s removed in channel #%s, message content: %s' % (message.author, message.channel, message.content))
		### Print log in console:
		print(current_time() + 'Removed message - %s : %s' % (message.author, message.content))
		### Remove the message which triggered the bot	
		await client.delete_message(message)
		### Send reply/notification
		mention = '{0.author.mention}'.format(message)
		await client.send_message(message.channel, config['SETTINGS']['message_on_trigger'].replace("@user", mention, 1))
	elif message.content.startswith('???creator'):
		await client.send_message(message.channel, 'FilterBot 2.0 created by TheRadziu :joy:')

### Actually run the bot and try to reconnect on fail/disconnect
is_offline = False
while True:
	try:
		client.loop.run_until_complete(client.start(config['LOGIN']['bot_token']))
	except KeyboardInterrupt:
		print(current_time() + 'Pressed Ctrl+C! Quitting FilterBot 2!')
		exit()
	except BaseException:
		if not is_offline:
			print(current_time() +'Disconnected! Attempting reconnect every {} seconds!'.format(config['SETTINGS']['reconnect_every_sec']))
			is_offline = True
		time.sleep(int(config['SETTINGS']['reconnect_every_sec']))
