import xml.etree.ElementTree as XET
# import pandas as pd 
# import csv
import requests
import os

#NOTE: when commiting to main branch, comment out users' specific paths

# xmlPath = 'C:/Users/andyr/Desktop/Special-Collections-Podcast-GUI-Project/XML'
# csvPath = 'C:/Users/andyr/Desktop/Special-Collections-Podcast-GUI-Project/CSV'

xmlPath = 'insert your path here' #XML Folder
csvPath = 'insert your path here' #CSV Folder

#for loop to iterate through xml files in xmlPath
for fileName in os.listdir(xmlPath):
    if not fileName.endswith('.xml'):
        continue
    xmlFilePath = os.path.join(xmlPath, fileName) #path to xml file

tree = XET.parse(xmlFilePath)
root = tree.getroot()

# podcastFolderPath = 'C:/Users/andyr/Desktop/Special-Collections-Podcast-GUI-Project/Podcasts'

podcastFolderPath = 'insert your path here'


#Script for downloading podcasts(mp3) using rss feed(xml) tags
for child in root.findall('./channel/item/'): #finds all tags in xml file under the item tag
    tag = child.tag
    if tag == 'enclosure':
         print(child.attrib.get('url'))
   



# for child in root: 
#     tag = child.tag
#     print(tag)
#     if tag == 'enclosure url':
#         print(child.text)
    

