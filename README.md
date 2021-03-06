# Discord FilterBot 2.0
This is simple Filter Bot for discord, written in Python 3.6.4 It's main function and purpose is to remove messages containing blacklisted urls, words or phrases. It's a great and lightweight precausion against people who report discord servers after posting some warez/illegal links just to get server removed and it's admin suspended from Discord platform.

## Main advantages
- Not case sensitive, doesn't matter if word, phrase or link is written in uppercase or lowercase or mixed, it will be detected,
- URLs will be always detected, no matter if person posts link to some subpage or file on that domain - example: if you blacklist `google.com` it will detect `www.google.com/maps` or `https://maps.google.com` links too,
- Very lightweight.

## Configuration
All user settings are stored in `config.ini`:
```ini
[LOGIN]
; Your bot token goes here:
bot_token = Your_bot_token

[SETTINGS]
; [on/off] If enabled displays more info on bot start.
more_info = off
;[on/off] If enabled sends a report about message being deleted [who posted it in which channel] to channel set in reporting_channel_id
reports = on
; ID of the channel where reports will be sent. Needs reports set to True
reporting_channel_id = Channel_id_here
; Bot will display this as Playing status. Set to off to disable status
playing_status = Example playing status
; Message that will be sent in the same channel as the message that was detected. You can use @user for mention the person who sent detected message.
message_on_trigger = Hey! @user Please do not link to anything containing copyright material!
; On connection failure bot will try to reconnect every set amount of seconds.
reconnect_every_sec = 5

[BLACKLIST]
; Words or URLs that will be removed if posted by someone, separated with new lines.
baguette
google.com
google.jp
YouTube.com
I don't like apples in my soup!
```

## Run
1. Download and place both files (`DiscordFilterBot.py` and `config.ini`) in same directory,
2. Either directly run `DiscordFilterBot.py` by double clicking it or through terminal/console `py DiscordFilterBot.py`
