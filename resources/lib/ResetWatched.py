# This file is part of PseudoTV.  It resets the watched status (playcount and resume) for all files in all playlists
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
import json

from xml.dom.minidom import parse, parseString

from Playlist import Playlist
from Globals import *
from Channel import Channel
from FileAccess import FileLock, FileAccess

class ResetWatched:
    def __init__(self):
        self.itemlist = []
        self.channels = []
        self.updateIndex = 0
        self.processingSemaphore = threading.BoundedSemaphore()
        self.maxNeededChannels = int(ADDON.getSetting("maxNeededChannels"))*50 + 100

    def readFile(self,maxChannels,watchedList):
        channel = 1
        
        debug('watchedList = ', watchedList)
        
        updateDialog = xbmcgui.DialogProgressBG()
        updateDialog.create(ADDON_NAME, '')
        uIndex = self.updateIndex
            
        while channel <= maxChannels:
            uIndex = int((channel/float(maxChannels))*100)
            updateDialog.update(uIndex, message='Exiting - Resetting Watched Status')
            
            filepath = CHANNELS_LOC + 'channel_' + str(channel) + '.m3u'
            index = self.load(filepath,watchedList)
            channel = channel +1
        updateDialog.close()
        
    def findMaxChannels(self):
        self.log('findMaxChannels')
        self.maxChannels = 0

        for i in range(self.maxNeededChannels):
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

    def load(self,filename,watchedList):
        self.log("RESET CHANNEL " + filename)
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
        
        for itemPath in watchedList:
            if itemPath in lines:
                previousline = int(lines.index(itemPath)) - 1
                dataline=lines[previousline].split('//')

                if len(dataline) != 7:
                    #avoiding Directory channels or any other invalid
                    self.log ("Skipping line with no reset fields: " + str(dataline))
                else: 
                    ID = dataline[6]
                    M3Ucount = int(dataline[3])
                    M3Uresume = float(dataline[4])
                    M3Ulastplayed = dataline[5]
                    episodetitle = dataline[1]
                    
                    self.log ("GETTING READY TO DO COMPARISON FOR ID: " + str(ID))

                    if ID != 0 and "MTV" not in ID:         #avoiding music videos
                        ID = int(ID)
                        
                        #if HideYearEpInfo is turned on, episodetitle will be blank for movies.  If it's off, episodetitle will contain an x (movies will have just a year)
                        debug("ADDON.getSetting('HideYearEpInfo') = ", ADDON.getSetting('HideYearEpInfo'))
                        debug('episodetitle = ', episodetitle)
                        
                        if ADDON.getSetting('HideYearEpInfo') == "true":
                            if episodetitle:
                                asset = "episode"
                            else:
                                asset = "movie"
                        else:
                            if episodetitle.find('x') != -1:
                                 asset = "episode"
                            else:
                                asset = "movie"
                        debug('asset = ', asset)
                        
                        
                        
                        if asset == "episode":
                            
                            #episode
                            json_query = '{"jsonrpc": "2.0", "method": "VideoLibrary.GetEpisodeDetails", "params": {"episodeid": %d, "properties": ["lastplayed","playcount","resume"]}, "id": 1}' % ID

                            json_folder_detail = self.sendJSON(json_query)

                            #next two lines accounting for how JSON returns resume info; stripping it down to just get the position
                            json_folder_detail = json_folder_detail.replace('"resume":{', '')
                            json_folder_detail = re.sub(r',"total":.+?}', '', json_folder_detail)

                            if 'error":{"code"' in json_folder_detail:
                                self.log("JSON Error: " +  json_folder_detail, xbmc.LOGWARNING)
                                assetMsg = "Possible Failure.  Check log."
                                xbmc.executebuiltin("Notification(\"PseudoTV Reset\", \"%s\")" % assetMsg)
                                self.log("Failed to reset Episode " + str(ID), xbmc.LOGWARNING)
                            
                            else:
                                params = json.loads(json_folder_detail)
                                result = params['result']
                                details = result['episodedetails']
                                JSONcount = details.get('playcount')
                                JSONresume = details.get('position')
                                JSONlastplayed = details.get('lastplayed')

                                self.log("TV JSON playcount: " + str(JSONcount) + " resume: " + str(JSONresume) + " lastplayed: " + JSONlastplayed)
                                self.log("TV M3U  playcount: " + str(M3Ucount) + " resume: " + str(M3Uresume) + " lastplayed: " + M3Ulastplayed)

                                if (JSONcount != M3Ucount) or (JSONresume != M3Uresume) or (JSONlastplayed != M3Ulastplayed):
                                    self.log("TV Resetting: " + episodetitle)
                                    response = xbmc.executeJSONRPC('{"jsonrpc": "2.0", "id": 1, "method": "VideoLibrary.SetEpisodeDetails", "params": {"episodeid" : %d, "lastplayed": "%s", "playcount": %d , "resume": {"position": %d}   }} ' % (ID, M3Ulastplayed, M3Ucount, M3Uresume))
                                    self.log("Response: " + response)
                        else:
                            #movie
                            json_query = '{"jsonrpc": "2.0", "method": "VideoLibrary.GetMovieDetails", "params": {"movieid": %d, "properties": ["lastplayed","playcount","resume"]}, "id": 1}' % ID

                            json_folder_detail = self.sendJSON(json_query)

                            #next two lines accounting for how JSON returns resume info; stripping it down to just get the position
                            json_folder_detail = json_folder_detail.replace('"resume":{', '')
                            json_folder_detail = re.sub(r',"total":.+?}', '', json_folder_detail)

                            if 'error":{"code"' in json_folder_detail:
                                self.log("JSON Error: " +  json_folder_detail, xbmc.LOGWARNING)
                                assetMsg = "Possible Failure.  Check log."
                                xbmc.executebuiltin("Notification(\"PseudoTV Reset\", \"%s\")" % assetMsg)
                                self.log("Failed to reset Movie " + str(ID), xbmc.LOGWARNING)
                                
                            else: 

                                params = json.loads(json_folder_detail)
                                result = params['result']
                                details = result['moviedetails']
                                JSONcount = details.get('playcount')
                                JSONresume = details.get('position')
                                JSONlastplayed = details.get('lastplayed')

                                self.log("Movie JSON playcount: " + str(JSONcount) + " resume: " + str(JSONresume) + " lastplayed: " + JSONlastplayed)
                                self.log("Movie M3U  playcount: " + str(M3Ucount) + " resume: " + str(M3Uresume) + " lastplayed: " + M3Ulastplayed)

                                if (JSONcount != M3Ucount) or (JSONresume != M3Uresume) or (JSONlastplayed != M3Ulastplayed):
                                    self.log("Movie Resetting: " + str(ID))
                                    
                                    response = xbmc.executeJSONRPC('{"jsonrpc": "2.0", "id": 1, "method": "VideoLibrary.SetMovieDetails", "params": {"movieid" : %d, "lastplayed": "%s", "playcount": %d , "resume": {"position": %d}   }} ' % (ID, M3Ulastplayed, M3Ucount, M3Uresume))
                                    self.log("Response: " + response)

        self.processingSemaphore.release()

        if len(self.itemlist) == 0:
            return False
        return
    
    def Resetter (self,watchedList):
        maxChannels = self.findMaxChannels()
        self.readFile(maxChannels,watchedList)
        

    def log(self, msg, level = xbmc.LOGDEBUG):
        log('ResetWatched: ' + msg, level)
