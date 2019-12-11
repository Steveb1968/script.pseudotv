#   Copyright (C) 2011 Jason Anderson
#
#
# This file is part of PseudoTV.
#
# PseudoTV is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# PseudoTV is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with PseudoTV.  If not, see <http://www.gnu.org/licenses/>.

import xbmc
import xbmcgui
import xbmcaddon
import sys
import os

ADDON = xbmcaddon.Addon()
ADDON_ID = ADDON.getAddonInfo('id')
CWD = ADDON.getAddonInfo('path').decode("utf-8")
RESOURCE = xbmc.translatePath(os.path.join(CWD, 'resources', 'lib').encode("utf-8")).decode("utf-8")

sys.path.append(RESOURCE)

SkinID = xbmc.getSkinDir()
if SkinID != 'skin.estuary':
    import MyFont
    if MyFont.getSkinRes() == '1080i':
        MyFont.addFont("PseudoTv10", "NotoSans-Regular.ttf", "23")
        MyFont.addFont("PseudoTv12", "NotoSans-Regular.ttf", "25")
        MyFont.addFont("PseudoTv13", "NotoSans-Regular.ttf", "30")
        MyFont.addFont("PseudoTv14", "NotoSans-Regular.ttf", "32")
    else:
        MyFont.addFont("PseudoTv10", "NotoSans-Regular.ttf", "14")
        MyFont.addFont("PseudoTv12", "NotoSans-Regular.ttf", "16")
        MyFont.addFont("PseudoTv13", "NotoSans-Regular.ttf", "20")
        MyFont.addFont("PseudoTv14", "NotoSans-Regular.ttf", "22")

def Start():
    if xbmc.Player().isPlaying():
        xbmc.Player().stop()
    import Overlay as Overlay
    MyOverlayWindow = Overlay.TVOverlay("script.pseudotv.TVOverlay.xml", CWD, "default")
    del MyOverlayWindow
    xbmcgui.Window(10000).setProperty("PseudoTVRunning", '')

if xbmcgui.Window(10000).getProperty("PseudoTVRunning") != "True":
    xbmcgui.Window(10000).setProperty("PseudoTVRunning", "True")
    shouldrestart = False
    if shouldrestart == False:
        Start()
else:
    xbmc.log('script.PseudoTV - Already running, exiting', xbmc.LOGERROR)
