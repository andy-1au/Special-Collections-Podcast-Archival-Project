from pathlib import Path #for path validation

import lxml.etree as ET #for xml parsing built on top of xml.etree
import xml.etree.ElementTree as ET #for xml parsing 
import csv 
import requests #for downloading the RSS feed
import os #for path manipulation
import re #for regex
 
def format_xml(xmlFile): #formats the file and return a list of all tags excluding the channel tag
    tree = ET.parse(xmlFile) #parse the xml file
    root = tree.getroot() #get the root of the xml file
    pattern = re.compile(r'{.*}') #regex pattern
    pattern = re.compile(r'.*:.*') #regex pattern
    tags = [] #list of tags
    for i in root.findall('./channel/item/'): #find all the items in the xml file
        # if('itunes' in i.tag):
        #     rep = re.sub(pattern, 'itunes_', i.tag) #remove the {STRING} from the tag
        #     i.tag = rep #replace the tag with the new tag
        if(':' in i.tag):
            print(i.tag[0])
            # namespace = i.tag.split(':') #remove the {STRING} from the tag
            # i.tag = namespace[0]+'_'+namespace[1] #replace the tag with the new tag
        if(i.tag not in tags and i.tag != 'channel'): #if the tag is not in the list of tags
            tags.append(i.tag)
    tree.write('test.xml', xml_declaration=True) #write the new xml file
    return tags

tags = format_xml('rss.xml')
print(tags)
