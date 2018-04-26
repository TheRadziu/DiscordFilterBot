################# Written by TheRadziu for Spoopy <3 #################
################# Script Version: whatever           #################
################# Only edit Settings below and       #################
################# selected blacklist_file itself     #################

### Settings and shit
more_info = False
reports = True
reporting_channel_id = Channel_id_here
bot_token = 'BOT TOKEN HERE'
playing_status = 'PLAYING STATUS HERE'
blacklist_file = 'blacklist.txt'
reconnect_every_sec = 5

############# Code Starts here - Do not touch #############
import asyncio
import platform
import time
from time import gmtime, strftime

### Check if discord library is installed
try:
	import discord
except ImportError:
	print('Discord library is not installed! Please run this command to install it!:')
	print('python -m pip install -U discord.py')
	exit()

### Load and parse blacklist_file
bl_phrases =  set(open('./' + blacklist_file).read().split())
bl_phrases = list(map(lambda x: x.lower(), bl_phrases))

client = discord.Client()
already_connected = False
current_time = strftime("[%H:%M:%S] ", gmtime())

### On bot run:
@client.event
async def on_ready():
	global already_connected
	if not already_connected:
		print('\nWelcome to the FilterBot 2.0\n')
		print('Your selected banned phrases are:')
		print(bl_phrases)
		if more_info:
			print('--------')
			print('Current Discord.py Version: {} | Current Python Version: {}'.format(discord.__version__, platform.python_version()))
			print('--------')
			print('Use this link to invite {}:'.format(client.user.name))
			print('https://discordapp.com/oauth2/authorize?client_id={}&scope=bot&permissions=8'.format(client.user.id))
			print('--------')
			print(current_time + 'Logged in as '+client.user.name+' (ID:'+client.user.id+') | Connected to '+str(len(client.servers))+' servers | Watching over '+str(len(set(client.get_all_members())))+' users')
		else: 
			print('--------')
			print(current_time + 'Connected. Bot is now Online and Active.')
		already_connected = True
	else:
		print(current_time + 'Successfuly reconnected!')
		
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
			print(current_time + 'Removed message - %s : %s' % (message.author, message.content))
		### Remove the message which triggered the bot	
		await client.delete_message(message)
		### Send reply/notification with mention
		mention = '{0.author.mention}'.format(message)
		await client.send_message(message.channel, 'Hey! ' + mention + ' Please do not link to anything containing copyright material!')
	elif message.content.startswith('???creator'):
		await client.send_message(message.channel, 'FilterBot 2.0 created by TheRadziu :joy:')

### Actually run the bot and try to reconnect on fail/disconnect
is_offline = False
while True:
	try:
		client.loop.run_until_complete(client.start(bot_token))
	except BaseException:
		if not is_offline:
			print(current_time +'Disconnected! Attempting reconnect every {} seconds!'.format(reconnect_every_sec))
			is_offline = True
		time.sleep(reconnect_every_sec)
