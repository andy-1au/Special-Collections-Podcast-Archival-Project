import xml.etree.ElementTree as XET
import pandas as pd 
import csv
import requests
import os

#TEST#

xmlPath = 'C:/Users/andyr/Downloads/Chrome Downloads/WorkStudy/Podcast Files/XML'
csvPath = 'C:/Users/andyr/Downloads/Chrome Downloads/WorkStudy/Podcast Files/CSV'
for fileName in os.listdir(xmlPath): 
    if not fileName.endswith('xml'): continue #goes to the next file if file doesn't end with .xml format 
    fullXMLPath = os.path.join(xmlPath, fileName)
    tree = XET.parse(fullXMLPath)
    root = tree.getroot() 
    baseName = os.path.splitext(fileName)[0] #splits the file name into the base name and file type (format), then takes only the base name ([0])       
    csvName = baseName + '.csv' #naming a new file as .csv
    fullCSVPath = os.path.join(csvPath, csvName)
    podcast_data = open(fullCSVPath, 'w')
    csvwriter = csv.writer(podcast_data)
    podcast_header = []
    count = 0 
    for i in root.findall('./channel/item'): #loops the appending of every channel which corresponds to the download too
        podcast_main = []
        if count == 0: #if loop used to control the writing of header titles 
            title = i.find("title").tag # tags are just the header title, only appended once 
            podcast_header.append(title)
            description =  i.find("description").tag
            podcast_header.append(description)
            link = i.find("link").tag
            podcast_header.append(link)
            pubDate = i.find("pubDate").tag
            podcast_header.append(pubDate)
            duration = i.find("iduration").tag
            podcast_header.append(duration)
            enclosure = i.find("enclosure").tag
            podcast_header.append(enclosure)
            season = i.find("iseason").tag
            podcast_header.append(season)
            episode = i.find("iepisode").tag
            podcast_header.append(episode)

            csvwriter.writerow(podcast_header)
            count+=1 #ends if loop, writes it only once 
        # not sure if the order in which I write the appending matters for the format of the csv file, I think it does
        title = i.find("title").text # gets the text details 
        podcast_main.append(title)
        description = i.find("description").text
        podcast_main.append(description)
        link = i.find("link").text
        podcast_main.append(link)
        pubDate = i.find("pubDate").text
        podcast_main.append(pubDate)
        duration = i.find("iduration").text
        podcast_main.append(duration)
        enclosure = i.find("enclosure").attrib # the url is an attribute of enclosure
        enclosure1 = enclosure.get("url") # get's the text file of the url in enclosure
        enclosureF = enclosure1
        #Download Section Begin
        if enclosureF.find('/'): 
            fileFormat = enclosureF.rsplit('/', 1)[1] # gets file name from url: 
                                                        # splits the string from the right the first / into two elements in a string arr
                                                        # [1] gets the second index of the array 
            print(fileFormat) #DEBUG and tells me what gets downloaded 
        request = requests.get(enclosureF, allow_redirects=True) 
        save_path = 'C:/Users/andyr/Downloads/Chrome Downloads/WorkStudy/Podcast Files/MP3' # download path
        file_name = fileFormat #file name
        completeFilePath = os.path.join(save_path, file_name) # adds the two together to be read in next line so that the download is correct
        open(completeFilePath, 'wb').write(request.content) # 'wb' means that the file is opened for writing in binary mode
        #Download Section End
        podcast_main.append(enclosure1)
        season = i.find("iseason").text
        podcast_main.append(season)
        episode = i.find("iepisode").text
        podcast_main.append(episode)

        csvwriter.writerow(podcast_main)
podcast_data.close()






