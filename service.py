# modules
from time import sleep
import xbmc, xbmcgui, os
import xbmcaddon

# get addon info
__addon__       = xbmcaddon.Addon(id='script.pseudotv')
__addonid__     = __addon__.getAddonInfo('id')
__language__    = __addon__.getLocalizedString
__addonname__   = __addon__.getAddonInfo('name')
__icon__        = __addon__.getAddonInfo('icon')

timer_amounts = {}
timer_amounts['0'] = 0            
timer_amounts['1'] = 5           
timer_amounts['2'] = 10            
timer_amounts['3'] = 15
timer_amounts['4'] = 20

IDLE_TIME = int(timer_amounts[__addon__.getSetting('timer_amount')])
Msg = __addon__.getSetting('notify')
Enabled = __addon__.getSetting('enable')

# start service
def Notify():	
	if (Msg == 'true'):
		xbmc.executebuiltin("Notification( %s, %s, %d, %s)" % (__addonname__, __language__(30030), 4000, __icon__) )
		xbmc.log("AUTOSTART PTV: Notifications Enabled...")
	else:
		xbmc.log("AUTOSTART PTV: Notifications Disabled...")
	
def autostart():
	Notify()		
	sleep(IDLE_TIME)	
	xbmc.executebuiltin("XBMC.RunScript(script.pseudotv)")
	xbmc.log("AUTOSTART PTV: Service Started...")
				
if (Enabled == 'true'):	
	autostart()
