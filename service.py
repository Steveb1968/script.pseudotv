#!/usr/bin/python
# coding: utf-8

import xbmc
import xbmcaddon

ADDON = xbmcaddon.Addon()
ADDON_ID = ADDON.getAddonInfo('id')
LANGUAGE = ADDON.getLocalizedString
ADDON_NAME = ADDON.getAddonInfo('name')
ICON = ADDON.getAddonInfo('icon')

timer_amounts = [0, 5, 10, 15, 20]

IDLE_TIME = timer_amounts[int(ADDON.getSetting("timer_amount"))]
Msg = ADDON.getSetting('notify')
Enabled = ADDON.getSetting('enable')

def autostart():
    if (Msg == 'true'):
        xbmc.executebuiltin("Notification( %s, %s, %d, %s)" % (ADDON_NAME, LANGUAGE(30030), 4000, ICON))
    xbmc.sleep(IDLE_TIME*1000)
    xbmc.executebuiltin("RunScript("+ADDON_ID+")")
    xbmc.log("AUTOSTART PTV: Service Started...")

if (Enabled == 'true'):
    autostart()
