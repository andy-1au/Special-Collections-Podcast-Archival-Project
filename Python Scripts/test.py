import xml.etree.ElementTree as XET
import pandas as pd
import csv
import requests
import os

xmlPath = 'C:/Users/andyr/Downloads/Chrome Downloads/WorkStudy/Podcast Files/XML'
for xmlName in os.listdir(xmlPath): 
    if not xmlName.endswith('xml'): continue #goes to the next file if file doesn't end with .xml format 
    fullPath = os.path.join(xmlPath, xmlName)
    changeFormat = os.path.splitext(xmlName)[0]
    csvName = changeFormat + '.csv'
    print(csvName)

    