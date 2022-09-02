import xml.etree.ElementTree as XET
import pandas as pd 
import csv
import requests
import os

#NOTE: when commiting to main branch, comment out users' specific paths

# xmlPath = 'C:/Users/andyr/Desktop/Special-Collections-Podcast-GUI-Project/XML'
# csvPath = 'C:/Users/andyr/Desktop/Special-Collections-Podcast-GUI-Project/CSV'

xmlPath = 'insert path here'
csvPath = 'insert path here'

#for loop to iterate through xml files in xmlPath
for fileName in os.listdir(xmlPath):
    if not fileName.endswith('.xml'):
        continue
    xmlFilePath = os.path.join(xmlPath, fileName) #

tree = XET.parse(xmlFilePath)
root = tree.getroot()

podcastFolderPath = 'insert path here'
# podcastFolderPath = 'C:/Users/andyr/Desktop/Special-Collections-Podcast-GUI-Project/Podcasts'

for child in root.findall('./channel/item/'):
    tag = child.tag
    if tag == 'enclosure':
        url = child.attrib.get('url')
        if url.find('./'):
            fileName = url.rsplit('/', 1)[1]
            filePath = os.path.join(podcastFolderPath, fileName)
        download = requests.get(url, allow_redirects=True)
        print(url + " has been downloaded")
        open(filePath, 'wb').write(download.content)
        


         
        
   


