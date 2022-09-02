import xml.etree.ElementTree as XET
import pandas as pd 
import csv
import requests
import os

#xmlPath = 'C:/Users/andyr/Desktop/Special-Collections-Podcast-GUI-Project/XML'
#csvPath = 'C:/Users/andyr/Desktop/Special-Collections-Podcast-GUI-Project/CSV'

xmlPath = 'insert path here'
csvPath = 'insert path here'

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
         print(child.attrib.get('url'))
   



# for child in root: 
#     tag = child.tag
#     print(tag)
#     if tag == 'enclosure url':
#         print(child.text)
    

