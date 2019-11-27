# This file is part of PseudoTV.  It resets thee watched status (playcount and resume) for all files in all playlists
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

import xbmc, xbmcgui, xbmcaddon
import subprocess, os
import time, threading
import datetime
import sys, re
import random
import json

from xml.dom.minidom import parse, parseString

from Playlist import Playlist
from Globals import *
from Channel import Channel
from FileAccess import FileLock, FileAccess

class PlaylistItem:
    def __init__(self):
        self.duration = 0
        self.filename = ''
        self.description = ''
        self.title = ''
        self.episodetitle = ''
        self.playcount = 0
        self.resume = 0
        self.ID = 0
        self.lastplayed = ''

class ResetWatched:
    def __init__(self):
        self.itemlist = []
        self.channels = []
        self.processingSemaphore = threading.BoundedSemaphore()

    def readFile(self, maxChannels):
        channel = 1

        while channel <= maxChannels:
            filepath = CHANNELS_LOC + 'channel_' + str(channel) + '.m3u'
            index = self.load(filepath)
            channel = channel +1

    def findMaxChannels(self):
        self.log('findMaxChannels')
        self.maxChannels = 0

        for i in range(999):
            chtype = 9999

            try:
                chtype = int(ADDON_SETTINGS.getSetting('Channel_' + str(i + 1) + '_type'))
                if chtype != 9999:
                    self.maxChannels = i + 1
            except:
                pass

        self.log('findMaxChannels return: '  + str(self.maxChannels))
        return(self.maxChannels)


    def clear(self):
        del self.itemlist[:]

    def sendJSON(self, command):
        data = xbmc.executeJSONRPC(command)
        return unicode(data, 'utf-8', errors='ignore')

    def load(self, filename):
        self.log("Reset " + filename)
        self.processingSemaphore.acquire()
        self.clear()

        try:
            fle = FileAccess.open(filename, 'r')
        except IOError:
            self.log('Unable to open the file: ' + filename)
            self.processingSemaphore.release()
            return False

        # find and read the header
        try:
            lines = fle.readlines()
        except:
            self.log("ERROR loading playlist: " + filename)
            self.log(traceback.format_exc(), xbmc.LOGERROR)

        fle.close()
        realindex = -1

        for i in range(len(lines)):
            if lines[i].startswith('#EXTM3U'):
                realindex = i
                break

        if realindex == -1:
            self.log('Unable to find playlist header for the file: ' + filename)
            self.processingSemaphore.release()
            return False

        # past the header, so get the info
        for i in range(len(lines)):

            if realindex + 1 >= len(lines):
                break

            if len(self.itemlist) > 16384:
                break

            try:
                line = uni(lines[realindex].rstrip())
            except:
                self.log("ERROR: Invalid line in playlist - " + filename)
                self.log(traceback.format_exc(), xbmc.LOGERROR)

            if line[:8] == '#EXTINF:':
                tmpitem = PlaylistItem()
                index = line.find(',')

                if index > 0:
                    tmpitem.duration = int(line[8:index])
                    tmpitem.title = line[index + 1:]
                    index = tmpitem.title.find('//')

                    if index >= 0:
                        tmpitem.episodetitle = tmpitem.title[index + 2:]
                        tmpitem.title = tmpitem.title[:index]
                        index = tmpitem.episodetitle.find('//')

                        if index >= 0:
                            tmpitem.description = tmpitem.episodetitle[index + 2:]
                            tmpitem.episodetitle = tmpitem.episodetitle[:index]
                            index = tmpitem.description.find('//')

                            if index >= 0:
                                tmpitem.playcount = tmpitem.description[index + 2:]
                                tmpitem.description = tmpitem.description[:index]
                                index = tmpitem.playcount.find('//')

                                if index >= 0:
                                    tmpitem.resume = tmpitem.playcount[index + 2:]
                                    tmpitem.playcount = tmpitem.playcount[:index]
                                    index = tmpitem.resume.find('//')

                                    if index >= 0:
                                        tmpitem.lastplayed = tmpitem.resume[index + 2:]
                                        tmpitem.resume = tmpitem.resume[:index]
                                        index = tmpitem.lastplayed.find('//')

                                        if index >= 0:
                                            tmpitem.ID = tmpitem.lastplayed[index + 2:]
                                            tmpitem.lastplayed = tmpitem.lastplayed[:index]
                                            index = tmpitem.ID.find('//')

                                            if index >= 0:
                                                tmpitem.ID = tmpitem.resume[index + 2:]

                ID = int(tmpitem.ID)
                M3Ucount = int(tmpitem.playcount)
                M3Uresume = float(tmpitem.resume)
                M3Ulastplayed = tmpitem.lastplayed
                episodetitle = tmpitem.episodetitle
                self.log("Parsing index Count: " + str(M3Ucount) + " Resume: " + str(M3Uresume) + "  lastplayed: " + M3Ulastplayed + " ID: " + str(ID))

                if ID != 0:         #avoiding Directory channels or any other invalid
                    if episodetitle.find('x') != -1:
                        #episode

                        json_query = '{"jsonrpc": "2.0", "method": "VideoLibrary.GetEpisodeDetails", "params": {"episodeid": %d, "properties": ["lastplayed","playcount","resume"]}, "id": 1}' % ID

                        json_folder_detail = self.sendJSON(json_query)

                        #next two lines accounting for how JSON returns resume info; stripping it down to just get the position
                        json_folder_detail = json_folder_detail.replace('"resume":{', '')
                        json_folder_detail = re.sub(r',"total":.+?}', '', json_folder_detail)

                        try:
                            params = json.loads(json_folder_detail)
                            result = params['result']
                            details = result['episodedetails']
                            JSONcount = details.get('playcount')
                            JSONresume = details.get('position')
                            JSONlastplayed = details.get('lastplayed')

                            #if (JSONcount != 0) and (JSONresume !=0):

                            self.log("TV JSON playcount: " + str(JSONcount) + " resume: " + str(JSONresume) + " lastplayed: " + JSONlastplayed)
                            self.log("TV M3U playcount: " + str(M3Ucount) + " resume: " + str(M3Uresume) + " lastplayed: " + M3Ulastplayed)

                            if (JSONcount != M3Ucount) or (JSONresume != M3Uresume) or (JSONlastplayed != M3Ulastplayed):
                                self.log("TV Resetting: " + episodetitle)
                                response = xbmc.executeJSONRPC('{"jsonrpc": "2.0", "id": 1, "method": "VideoLibrary.SetEpisodeDetails", "params": {"episodeid" : %d, "lastplayed": "%s", "playcount": %d , "resume": {"position": %d}   }} ' % (ID, M3Ulastplayed, M3Ucount, M3Uresume))
                                self.log("Response: " + response)
                        except:
                            self.log("Failed to reset " + str(ID), xbmc.LOGWARNING)

                    else:
                        #movie
                        json_query = '{"jsonrpc": "2.0", "method": "VideoLibrary.GetMovieDetails", "params": {"movieid": %d, "properties": ["lastplayed","playcount","resume"]}, "id": 1}' % ID

                        json_folder_detail = self.sendJSON(json_query)

                        #next two lines accounting for how JSON returns resume info; stripping it down to just get the position
                        json_folder_detail = json_folder_detail.replace('"resume":{', '')
                        json_folder_detail = re.sub(r',"total":.+?}', '', json_folder_detail)

                        try:

                            params = json.loads(json_folder_detail)
                            result = params['result']
                            details = result['moviedetails']
                            JSONcount = details.get('playcount')
                            JSONresume = details.get('position')
                            JSONlastplayed = details.get('lastplayed')

                            #if (JSONcount != 0) and (JSONresume !=0):

                            self.log("Movie JSON playcount: " + str(JSONcount) + " resume: " + str(JSONresume) + " lastplayed: " + JSONlastplayed)
                            self.log("Movie M3U playcount: " + str(M3Ucount) + " resume: " + str(M3Uresume) + " lastplayed: " + M3Ulastplayed)

                            if (JSONcount != M3Ucount) or (JSONresume != M3Uresume) or (JSONlastplayed != M3Ulastplayed):
                                self.log("Movie Resetting: " + str(ID))
                                response = xbmc.executeJSONRPC('{"jsonrpc": "2.0", "id": 1, "method": "VideoLibrary.SetMovieDetails", "params": {"movieid" : %d, "lastplayed": "%s", "playcount": %d , "resume": {"position": %d}   }} ' % (ID, M3Ulastplayed, M3Ucount, M3Uresume))
                                self.log("Response: " + response)

                        except:
                            self.log("Failed to reset " + str(ID), xbmc.LOGWARNING)

                realindex += 1
                tmpitem.filename = uni(lines[realindex].rstrip())
                self.itemlist.append(tmpitem)


            realindex += 1

        self.processingSemaphore.release()

        if len(self.itemlist) == 0:
            return False

        return index

    def Resetter (self):
        maxChannels = self.findMaxChannels()
        EndTime = datetime.datetime.now()
        self.readFile(maxChannels)

    def log(self, msg, level = xbmc.LOGDEBUG):
        log('ResetWatched: ' + msg, level)
