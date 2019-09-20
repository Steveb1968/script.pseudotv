#!/usr/bin/python
# coding: utf-8

import os
import xml.etree.ElementTree as ET
import xbmc, xbmcaddon, xbmcvfs

ADDON = xbmcaddon.Addon(id='script.pseudotv')
SkinPath = xbmc.translatePath('special://skin')
ScriptPath = xbmc.translatePath(ADDON.getAddonInfo('path'))
SourceFontPath = os.path.join(ScriptPath, 'resources', 'fonts', 'NotoSans-Regular.ttf')
ListDir = os.listdir(SkinPath)

class PCParser(ET.XMLTreeBuilder):
   def __init__(self):
       ET.XMLTreeBuilder.__init__(self)
       self._parser.CommentHandler = self.handle_comment

   def handle_comment(self, data):
       self._target.start(ET.Comment, {})
       self._target.data(data)
       self._target.end(ET.Comment)

def getFontsXML():
    fontxml_paths = []
    try:
        for item in ListDir:
            item = os.path.join(SkinPath, item)
            if os.path.isdir(item):
                font_xml = os.path.join(item, "Font.xml")
                if os.path.exists(font_xml):
                    fontxml_paths.append(font_xml)
    except:
        pass
    return fontxml_paths

def isFontInstalled(fontxml_path, fontname):
    name = "<name>%s</name>" % fontname
    if not name in file(fontxml_path, "r").read():
        return False
    else:
        return True

def copyFont(SourceFontPath, SkinPath):
    dest = os.path.join(SkinPath, 'fonts', 'NotoSans-Regular.ttf')
    if os.path.exists(dest):
        return
    xbmcvfs.copy(SourceFontPath, dest)

def getSkinRes():
    SkinRes = '720p'
    SkinResPath = os.path.join(SkinPath, SkinRes)
    if not os.path.exists(SkinResPath):
        SkinRes = '1080i'
    return SkinRes

def addFont(fontname, filename, size, style=""):
    try:
        reload_skin = False
        fontxml_paths = getFontsXML()
        if fontxml_paths:
            for fontxml_path in fontxml_paths:
                if not isFontInstalled(fontxml_path, fontname):
                    parser = PCParser()
                    tree = ET.parse(fontxml_path, parser=parser)
                    root = tree.getroot()
                    for sets in root.getchildren():
                        sets.findall("font")[-1].tail = "\n\t\t"
                        new = ET.SubElement(sets, "font")
                        new.text, new.tail = "\n\t\t\t", "\n\t"
                        subnew1 = ET.SubElement(new, "name")
                        subnew1.text = fontname
                        subnew1.tail = "\n\t\t\t"
                        subnew2 = ET.SubElement(new, "filename")
                        subnew2.text = (filename, "Arial.ttf")[sets.attrib.get("id") == "Arial"]
                        subnew2.tail = "\n\t\t\t"
                        subnew3 = ET.SubElement(new, "size")
                        subnew3.text = size
                        subnew3.tail = "\n\t\t\t"
                        last_elem = subnew3
                        if style in ["normal", "bold", "italics", "bolditalics"]:
                            subnew4 = ET.SubElement(new, "style")
                            subnew4.text = style
                            subnew4.tail = "\n\t\t\t"
                            last_elem = subnew4
                        reload_skin = True
                        last_elem.tail = "\n\t\t"
                    tree.write(fontxml_path)
                    reload_skin = True
    except:
        pass

    if reload_skin:
        copyFont(SourceFontPath, SkinPath)
        xbmc.executebuiltin("XBMC.ReloadSkin()")
        return True

    return False
