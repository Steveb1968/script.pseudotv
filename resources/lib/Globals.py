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

import os
import xbmcaddon, xbmc, xbmcgui, xbmcvfs
import Settings

from FileAccess import FileLock

def debug(msg, *args):
    try:
        txt=u''
        msg=unicode(msg)
        for arg in args:
            if type(arg) == int:
                arg = unicode(arg)
            if type(arg) == list:
                arg = unicode(arg)
            txt = txt + u"/" + arg
        if txt == u'':
            xbmc.log(u"PSTV: {0}".format(msg).encode('ascii','xmlcharrefreplace'), xbmc.LOGDEBUG)
        else:
            xbmc.log(u"PSTV: {0}#{1}#".format(msg, txt).encode('ascii','xmlcharrefreplace'), xbmc.LOGDEBUG)
    except:
        print "PSTV: Error in Debugoutput"
        print msg
        print args

ADDON = xbmcaddon.Addon(id='script.pseudotv')
ADDON_ID = ADDON.getAddonInfo('id')
ADDON_NAME = ADDON.getAddonInfo('name')
LANGUAGE = ADDON.getLocalizedString
CWD = ADDON.getAddonInfo('path').decode("utf-8")
VERSION = ADDON.getAddonInfo('version')
ICON = ADDON.getAddonInfo('icon')

def log(msg, level = xbmc.LOGDEBUG):
    try:
        xbmc.log(ADDON_ID + '-' + ascii(msg), level)
    except:
        pass


def uni(string, encoding = 'utf-8'):
    if isinstance(string, basestring):
        if not isinstance(string, unicode):
           string = unicode(string, encoding)

    return string

def ascii(string):
    if isinstance(string, basestring):
        if isinstance(string, unicode):
           string = string.encode('ascii', 'ignore')

    return string


TIMEOUT = 15 * 1000
PREP_CHANNEL_TIME = 60 * 60 * 24 * 5
NOTIFICATION_CHECK_TIME = 5
NOTIFICATION_TIME_BEFORE_END = 90
NOTIFICATION_DISPLAY_TIME = 8

MODE_RESUME = 1
MODE_ALWAYSPAUSE = 2
MODE_ORDERAIRDATE = 4
MODE_RANDOM = 8
MODE_REALTIME = 16
MODE_STARTMODES = MODE_RANDOM | MODE_REALTIME | MODE_RESUME

SETTINGS_LOC = ADDON.getAddonInfo('profile').decode("utf-8")
CHANNEL_SHARING = False
LOCK_LOC = xbmc.translatePath(os.path.join(SETTINGS_LOC, 'cache' + '/'))

if ADDON.getSetting('ChannelSharing') == "true":
    CHANNEL_SHARING = True
    LOCK_LOC = xbmc.translatePath(os.path.join(ADDON.getSetting('SettingsFolder'), 'cache' + '/'))

IMAGES_LOC = xbmc.translatePath(os.path.join(CWD, 'resources', 'images' + '/'))
LOGOS_LOC = xbmc.translatePath(os.path.join(CWD, 'resources', 'logos' + '/'))
CHANNELS_LOC = os.path.join(SETTINGS_LOC, 'cache' + '/')
GEN_CHAN_LOC = os.path.join(CHANNELS_LOC, 'generated' + '/')
MADE_CHAN_LOC = os.path.join(CHANNELS_LOC, 'stored' + '/')
CHANNELBUG_LOC = xbmc.translatePath(os.path.join(CHANNELS_LOC, 'ChannelBug' + '/'))

CHANNELBUG_POS =[[19,19],[1695,19],[1695,952],[19,952]]

SHORT_CLIP_ENUM = [15, 30, 60, 90, 120, 180, 240, 300, 360]
INFO_DUR = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
SEEK_FORWARD = [10, 30, 60, 180, 300, 600, 1800]
SEEK_BACKWARD = [-10, -30, -60, -180, -300, -600, -1800]
MEDIA_LIMIT = [10, 25, 50, 100, 250, 500, 1000, 0]
CHANNEL_DELAY = [25, 50, 100, 200, 300, 400, 500, 600, 700, 800, 900, 1000]
HOLD_ACTIONS = [.25, .5, 1, 1.5, 2, 2.5, 3, 3.5, 4]
ASSIGNED_DURATION = [1, 5, 10, 15, 30, 45, 60, 90, 120]
DIR_ASSIGNED_DURATION = [1, 5, 10, 15, 30, 45, 60, 90, 120]
BUG_BRIGHTNESS = [.25, .5, .75, 1.0, 1.25, 1.5, 1.75, 2.0, 2.25, 2.5, 2.75, 3.0]


NUM_COLOUR = ['0xFFFF0000', '0xFF00FF00', '0xFF0000FF', '0xFFFFFF00', '0xFF00FFFF', '0xFFFFA500', '0xFFFF00FF', '0xFF808080', '0xFFFFFFFF']

GlobalFileLock = FileLock()
ADDON_SETTINGS = Settings.Settings()

TIME_BAR = 'pstvTimeBar.png'
BUTTON_NO_FOCUS = 'pstvButtonNoFocus.png'
BUTTON_FOCUS = 'pstvButtonFocus.png'

RULES_ACTION_START = 1
RULES_ACTION_JSON = 2
RULES_ACTION_LIST = 4
RULES_ACTION_BEFORE_CLEAR = 8
RULES_ACTION_BEFORE_TIME = 16
RULES_ACTION_FINAL_MADE = 32
RULES_ACTION_FINAL_LOADED = 64
RULES_ACTION_OVERLAY_SET_CHANNEL = 128
RULES_ACTION_OVERLAY_SET_CHANNEL_END = 256

# Maximum is 10 for this
RULES_PER_PAGE = 7

ACTION_MOVE_LEFT = 1
ACTION_MOVE_RIGHT = 2
ACTION_MOVE_UP = 3
ACTION_MOVE_DOWN = 4
ACTION_PAGEUP = 5
ACTION_PAGEDOWN = 6
ACTION_SELECT_ITEM = 7
ACTION_SELECT_ITEM2 = 100 #Mouse Left Click
ACTION_PREVIOUS_MENU = (9, 10, 92, 216, 247, 257, 275, 61467, 61448,)
ACTION_SHOW_INFO = 11
ACTION_STOP = 13
ACTION_OSD = 117
ACTION_NUMBER_0 = 58
ACTION_NUMBER_9 = 67
ACTION_INVALID = 999
ACTION_MOUSE_RIGHT_CLICK = 101 #Mouse Right Click
CONTEXT_MENU = 117
ACTION_PREV_PICTURE = 29
