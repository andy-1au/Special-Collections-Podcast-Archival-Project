import xml.etree.ElementTree as XET
#import pandas as pd 
#import csv
import requests
import os

#xmlPath = 'C:/Users/andyr/Desktop/Special-Collections-Podcast-GUI-Project/XML'
#csvPath = 'C:/Users/andyr/Desktop/Special-Collections-Podcast-GUI-Project/CSV'

xmlPath = '/Users/dennis/Work Study/Special-Collections-Podcast-GUI-Project/XML'
#csvPath = 'insert path here'

#for loop to iterate through xml files in xmlPath
for fileName in os.listdir(xmlPath):
    if not fileName.endswith('.xml'):
        continue
    xmlFilePath = os.path.join(xmlPath, fileName) #

tree = XET.parse(xmlFilePath)
root = tree.getroot()


for child in root.findall('./channel/item/'):
    tag = child.tag
    if tag == 'enclosure':
        url = child.attrib.get('url')
        download = requests.get(url, allow_redirects=True)
        podcastFolderPath = "/Users/dennis/Work Study/Special-Collections-Podcast-GUI-Project/Podcasts"
        downloadedFileName = url.rsplit("/",1)[1]
        podcastFolderPath = os.path.join(podcastFolderPath, downloadedFileName)
        open(podcastFolderPath, 'wb').write(download.content)
        print(url + "has been downloaded")
    
