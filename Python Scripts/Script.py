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
    
import xml.etree.ElementTree as XET
import pandas as pd 
import csv
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
        url = child.attrib.get('url')
        if url.find('/'): #finds the last '/' in the url
            fileName = url.rsplit('/', 1)[1] #gets the file name from the url
            filePath = os.path.join(podcastFolderPath, fileName) #creates a path for the file to be saved
        download = requests.get(url, allow_redirects=True) #downloads the file
        print(url + " has been downloaded") 
        open(filePath, 'wb').write(download.content) #writes the file to the path
        


         
        
   


