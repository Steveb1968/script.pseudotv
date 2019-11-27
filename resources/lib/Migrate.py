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
import xbmcaddon, xbmc, xbmcgui
import Settings
import Globals
import ChannelList



class Migrate:
    def log(self, msg, level = xbmc.LOGDEBUG):
        Globals.log('Migrate: ' + msg, level)


    def migrate(self):
        self.log("migration")
        curver = "0.0.0"

        try:
            curver = Globals.ADDON_SETTINGS.getSetting("Version")

            if len(curver) == 0:
                curver = "0.0.0"
        except:
            curver = "0.0.0"

        if curver == Globals.VERSION:
            return True

        Globals.ADDON_SETTINGS.setSetting("Version", Globals.VERSION)
        self.log("version is " + curver)

        if curver == "0.0.0":
            if self.initializeChannels():
                return True

        return True


    def initializeChannels(self):
        chanlist = ChannelList.ChannelList()
        chanlist.background = True
        chanlist.fillTVInfo(True)
        chanlist.fillMovieInfo(True)
        # Now create TV networks, followed by mixed genres, followed by TV genres, and finally movie genres
        currentchan = 1
        mixedlist = []

        for item in chanlist.showGenreList:
            curitem = item[0].lower()

            for a in chanlist.movieGenreList:
                if curitem == a[0].lower():
                    mixedlist.append([item[0], item[1], a[1]])
                    break

        mixedlist.sort(key=lambda x: x[1] + x[2], reverse=True)
        currentchan = self.initialAddChannels(chanlist.networkList, 1, currentchan)

        # Mixed genres
        if len(mixedlist) > 0:
            added = 0.0

            for item in mixedlist:
                if item[1] > 2 and item[2] > 1:
                    Globals.ADDON_SETTINGS.setSetting("Channel_" + str(currentchan) + "_type", "5")
                    Globals.ADDON_SETTINGS.setSetting("Channel_" + str(currentchan) + "_1", item[0])
                    added += 1.0
                    currentchan += 1
                    itemlow = item[0].lower()

                    # Remove that genre from the shows genre list
                    for i in range(len(chanlist.showGenreList)):
                        if itemlow == chanlist.showGenreList[i][0].lower():
                            chanlist.showGenreList.pop(i)
                            break

                    # Remove that genre from the movie genre list
                    for i in range(len(chanlist.movieGenreList)):
                        if itemlow == chanlist.movieGenreList[i][0].lower():
                            chanlist.movieGenreList.pop(i)
                            break

                    if added > 10:
                        break

        currentchan = self.initialAddChannels(chanlist.showGenreList, 3, currentchan)
        currentchan = self.initialAddChannels(chanlist.movieGenreList, 4, currentchan)

        if currentchan > 1:
            return True

        return False


    def initialAddChannels(self, thelist, chantype, currentchan):
        if len(thelist) > 0:
            counted = 0
            lastitem = 0
            curchancount = 1
            lowerlimit = 1
            lowlimitcnt = 0

            for item in thelist:
                if item[1] > lowerlimit:
                    if item[1] != lastitem:
                        if curchancount + counted <= 10 or counted == 0:
                            counted += curchancount
                            curchancount = 1
                            lastitem = item[1]
                        else:
                            break
                    else:
                        curchancount += 1

                    lowlimitcnt += 1

                    if lowlimitcnt == 3:
                        lowlimitcnt = 0
                        lowerlimit += 1
                else:
                    break

            if counted > 0:
                for item in thelist:
                    Globals.ADDON_SETTINGS.setSetting("Channel_" + str(currentchan) + "_type", str(chantype))
                    Globals.ADDON_SETTINGS.setSetting("Channel_" + str(currentchan) + "_1", item[0])
                    counted -= 1
                    currentchan += 1

                    if counted == 0:
                        break

        return currentchan
