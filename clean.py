from pathlib import Path #for path validation

import lxml.etree as ET #for xml parsing built on top of xml.etree
import xml.etree.ElementTree as XET #for xml parsing
import csv 
import requests #for downloading the RSS feed
import os #for path manipulation
import re #for regex

def get_namespaces(xmlFile): #returns a list of namespaces in the xml file
    treeIter = ET.iterparse(xmlFile, events=['start-ns']) #create an iterator for the xml file
    namespaces = [] #list of namespaces
    for _, ns in treeIter:
        namespaces.append(ns) #add the namespace to the list
    return namespaces
 
def format_xml(xmlFile): #formats the file and return a list of all tags excluding the channel tag
    #for itunes tags only
    tree = ET.parse(xmlFile) #parse the xml file
    root = tree.getroot() #get the root of the xml file
    pattern = re.compile(r'{.*}') #regex pattern to match the namespace
    for i in root.findall('./channel/item/'):
        if(pattern.match(i.tag) and 'itunes' in i.tag): #if the tag is an itunes tag'):
            i.tag = re.sub(r'{.*}', 'itunes_', i.tag) #remove the namespace
        
    tree.write('test.xml', encoding='utf-8', xml_declaration=True) #write the changes to the file

tags = format_xml('rss.xml')
# print(tags)
