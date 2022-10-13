import xml.etree.ElementTree as XET 
import os 
import pandas as pd

def openXML(xmlFile):
    tree = XET.parse(xmlFile)
    root = tree.getroot()
    return root



allTags = [] 

def getTags(root):
