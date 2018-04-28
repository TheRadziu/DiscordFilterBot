# Discord FilterBot 2.0
This is simple Filter Bot for discord, written in Python 3.6.4 It's main function and purpose is to remove messages containing blacklisted urls or phrases. It's a great and lightweight precausion against people who report discord servers after posting some warez/illegal links just to get server removed and it's admin suspended from Discord platform.

## Main advantages
- Not case sensitive, doesn't matter if link is written in uppercase or lowercase or mixed, it will be detected,
- Phrase or domain will be always detected, no matter if person posts link to some subpage or file on that domain - example: if you blacklist `google.com` it will detect `www.google.com/maps` or `https://maps.google.com` links too,
- Very lightweight.

## Configuration
1. Edit `DiscordFilterBot.py` and set:
```python
more_info = False # [True/False] If enabled displays more info on bot start.
reports = True # [True/False] If enabled sends a report about message being deleted [who posted it in which channel] to channel set below
reporting_channel_id = Channel_id_here # ID of the channel where reports will be sent. Needs reports set to True
bot_token = 'BOT TOKEN' # Paste your bot token here.
playing_status = 'PLAYING STATUS HERE' # Bot will display this as Playing status.
blacklist_file = 'blacklist.txt' # File with forbidden phrases, mainly used for banning certain domains from discord server.
reconnect_every_sec = 5 # on connection failure bot will try to reconnect every set amount of secounds.
```
2. Also edit your blacklist file (default: `blacklist.txt`) with phrases or URLs that will be removed if posted by someone, separated with new lines. Example:
```
google.com
google.jp
baguette
```
3. (optional) you might want to edit 76th line to change what message is posted if someone triggers the bot by posting message with blacklisted url/phrase. Default bot's reply warns user not to post anything that contains copyrighted material.

## Run
1. Download and place both files (`DiscordFilterBot.py` and yet blacklist file) in same directory,
2. Either directly run `DiscordFilterBot.py` by double clicking it or through terminal/console `py DiscordFilterBot.py`
