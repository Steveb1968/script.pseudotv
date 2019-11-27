![alt text](https://github.com/Steveb1968/script.pseudotv/blob/master/resources/images/Default.png?raw=true "PseudoTV Logo")

PseudoTV for Kodi
======

[View branch download information.](#branches-guide)


![screenshot](https://github.com/Steveb1968/script.pseudotv/blob/master/resources/screenshots/screenshot-01.png?raw=true)

### What is it?
It's channel-surfing for your media center. Never again will you have to actually pick what you want to watch. Use an electronic program guide (EPG) to view what's on or select a show to watch. This script will let you create your own channels and, you know, watch them. Doesn't actually sound useful when I have to write it in a readme. Eh, try it and decide if it works for you.

---
### Requirements
This **ONLY** uses your existing video library to play video. It will **NOT** play video from the internet. If you do not have a significant number of videos in your library, then this script probably isn't for you. Sorry.

---
### Features

* Automatic channel creation based on your library.
* Optionally customize the channels you want with the channel configuration tool.
* Utilize the Kodi smart playlist editor to create advanced channel setups.
* Use an EPG and view what was on, is on, and will be on. Would you rather see something that will be on later? Select it and watch it now!
* Want to pause a channel while you watch another? And then come back to it and have it be paused still? Sounds like a weird request to me, but if you want to do it you certainly can. It's a feature!
* An idle-timer makes sure you aren't spinning a hard-drive needlessly all night.
* Discover the other features on your own (so that I don't have to list them all...I'm lazy).

---
### Setup
1. First, install it.  This is self-explanatory (hopefully).  Really, that's all that is necessary.  Default channels will be created without any intervention.  You can choose to setup channels (next step) if you wish.
2. _Instructions to create your own channels:_ Inside of the addon config, you may open the channel configuration tool. Inside of here you can select a channel to modify. You may then select it's type and any options. For a basic setup, that's all you need to do. It's worth noting that you may create a playlist using the smart playlist editor and then select that playlist in the channel config tool (Custom Playlist channel type). Additionally, you may select to add advanced rules to certain channels. There are quite a few rules that are currently available, and hopefully they should be relatively self-explanitory.

	This is a readme and should include descriptions of them all... who knows, maybe it will some day.

---
### Controls
There are only a few things you need to know in order to control everything. First of all, the Stop button ('X') stops the video and exits the script. You may also press the Previous Menu ('Escape\Back') button to do this (don't worry, it will prompt you to verify first). Scroll through channels using the arrow up and down keys, or alternatively by pressing Page up or down. To open the EPG, press the Select key ('Enter'). Move around using the arrow keys. Start a program by pressing Select. Pressing Previous Menu ('Escape\Back') will close the EPG. Press the info key ('I') to display or hide the info window.  When it is displayed, you can look at the previous and next shows on this channel using the arrow keys left and right. To access the video osd window press the context menu key ('C\Menu'), to exit the osd press ('Escape\Back').

---
### Settings

**General Settings -**

* **Configure Channels:** This is the channel configuration tool.  From here you can modify the settings for each individual channel.    
* **Force Channel Reset:** If you want your channels to be reanalyzed then you can turn this on.
* **Auto-off Timer:** The amount of time (in minutes) of idle time before the script is automatically stopped.
* **Time Between Channel Resets:** This is how often your channels will be reset. Generally, this is done automatically based on the duration of the individual channels and how long they've been watched. You can change this to reset every certain time period (day, week, month).
* **Default channel times at startup:** This affects where the channels start playing when the script starts.  Resume will pick everything up where it left off. Random will start each channel in a random spot. Real-Time will act like the script was never shut down, and will play things at the time the EPG said they would play.
* **Background Updating:** The script uses multiple threads to keep channels up to date while other channels are playing. In general, this is fine. If your computer is too slow, though, it may cause stuttering in the video playback. This setting allows you to minimize or disable the use of these background threads.
* **Enable Channel Sharing:** Share the same configuration and channel list between multiple computers. If you're using real-time mode (the default) then you can stop watching one show on one computer and pick it up on the other. Or you can have both computers playing the same lists at the same time.
* **Shared Channels Folder:** If channel sharing is enabled, this is the location available from both computers that will keep the settings and channel information.


**Visual Settings -**

* **Info when Changing Channels:** Shows the current media information when changing channels. The duration of the info can be set in the sub-setting "Changing channel info duration".
* **Always show channel watermark:** Always display the current channel logo watermark. The position of the logo can be adjusted via the sub-setting "Set watermark position" (upper left, upper right, lower right, lower left).
* **Hide year and episode information:** Removes the year (movies) and SxEP (episodes). A force channel reset is needed for the setting to take effect.  
* **Always show channel logo in epg grid:** Shows the channel logo's in the epg grid.
* **Channel Logo Folder:** The place where channel logos are stored.
* **Clock Display:** Select between a 12-hour or 24-hour clock in the EPG.
* **Show Coming Up Next box:** A little box will notify you of what's coming up next when the current show is nearly finished.
* **Hide very short videos:** Don't show clips shorter than the "Duration of Short videos" setting. Effects the EPG, coming up next box and the info box. This is helpful if you use bumpers or commercials.


**Tweaks -**

* **Playlist Media Limit:** Limit the playlist items in a channel generated by pseudotv. Smaller values will result in quicker load/rebuild times.
* **OSD Channel Number Color:** Change the color of the channel number located at the top left, seen when changing channels and on startup.
* **Seek step forward:** Option to adjust the seek step forward (right arrow key in fullscreen video). Options include 10 sec,30 sec,60 sec,3 min,5 min,10 min,30 min.
* **Seek step backward:** Option to adjust the seek step backward (left arrow key in fullscreen video). Options include -10 sec,-30 sec,-60 sec,-3 min,-5 min,-10 min,-30 min.
* **Reset Watched Status:** Option to reset watched status and resume points of videos while watching PseudoTV.


**Auto Start -**

* **Activate Service:** Activate auto start. Pseudotv will automatically start when kodi is started.
* **Service Delay:** Delay the auto start of Pseudotv at Kodi start-up. This is useful for low end hardware or if your skin loads multi-pal scripts at start-up.
* **Show Notification:** Self explanatory I hope. Will show a notification of Pseudotv's attempt to auto-start.

---
### Addon boolean condition

**&lsaquo;visible&rsaquo;String.IsEmpty(Window(home).Property(PseudoTVRunning))&lsaquo;/visible&rsaquo;**  
Useful for hiding skin xml files such as DialogBusy.xml/DialogSeekBar.xml 
 
**Tip: DialogSeekBar.xml**  
Replace *"Player.DisplayAfterSeek"* with  
*"[Player.DisplayAfterSeek\+String.IsEmpty(Window(home).Property(PseudoTVRunning))]"*    

---
### Branches guide

* **Master branch:** Suitable for Kodi VER:18 and above.
* **Leia branch:** Suitable for Kodi VER:18.
* **Krypton branch:** Suitable for Kodi VER:17 and below. 

---
### Credits

**Developer:** Jason102, Steveb.<br>
**Code Additions:** Sranshaft, TheOddLinguist, Canuma, rafaelvieiras, fnord12.<br>
**Skins:** Sranshaft, Zepfan, Steveb.<br>
**Preset Images:** Jtucker1972.<br>
**Languages:** CyberXaz, Machine-Sanctum, rafaelvieiras, Eng2Heb.