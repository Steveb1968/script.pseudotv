# modules
import xbmc
import xbmcaddon

# get addon info
__addon__       = xbmcaddon.Addon(id='script.pseudotv')
__addonid__     = __addon__.getAddonInfo('id')
__language__    = __addon__.getLocalizedString
__addonname__   = __addon__.getAddonInfo('name')
__icon__        = __addon__.getAddonInfo('icon')

timer_amounts = [0, 5, 10, 15, 20]

IDLE_TIME = timer_amounts[int(__addon__.getSetting("timer_amount"))]
Msg = __addon__.getSetting('notify')
Enabled = __addon__.getSetting('enable')

# start service
def Notify():
    if (Msg == 'true'):
        xbmc.executebuiltin("Notification( %s, %s, %d, %s)" % (__addonname__, __language__(30030), 4000, __icon__))
        xbmc.log("AUTOSTART PTV: Notifications Enabled...")
    else:
        xbmc.log("AUTOSTART PTV: Notifications Disabled...")

def autostart():
    Notify()
    xbmc.sleep(IDLE_TIME*1000)
    xbmc.executebuiltin("RunScript("+__addonid__+")")
    xbmc.log("AUTOSTART PTV: Service Started...")

if (Enabled == 'true'):
    autostart()
