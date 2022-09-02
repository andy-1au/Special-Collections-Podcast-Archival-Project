import xml.etree.ElementTree as XET
import csv
import requests
import os

#WORKING#

xmlPath = 'C:/Users/andyr/Downloads/Chrome Downloads/WorkStudy/Podcast Files/rossin/XML' #CHANGE directory path for where xml file is held
csvPath = 'C:/Users/andyr/Downloads/Chrome Downloads/WorkStudy/Podcast Files/rossin/CSV' #CHANGE directory path for where csv file is held
xmlFileName = 'rossin.xml' #CHANGE file name of xml file 
fullXMLPath = os.path.join(xmlPath, xmlFileName) # creates full directory path
tree = XET.parse(fullXMLPath) # parses the XML data
root = tree.getroot()
baseName = os.path.splitext(xmlFileName)[0] # splits the file name into the base name and file type (format), then takes only the base name ([0]) 
csvFileName = baseName + '.csv' # creates a name same as the xml file name but with csv format
fullCSVPath = os.path.join(csvPath, csvFileName)
podcast_data = open(fullCSVPath, 'w') # creates a new csv file 
csvwriter = csv.writer(podcast_data)
podcast_header = []
count = 0 
for i in root.findall('./channel/item'): # loops the appending of every channel which corresponds to the download too
    podcast_main = []
    if count == 0: # if loop used to control the writing of header titles 
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
        stringLength = len(fileFormat) # gets the length of the formatted file name
        lastChar = fileFormat[stringLength-1] # gets the last char of the file name
        second2lastChar = fileFormat[stringLength-2]
        if lastChar != '3' and second2lastChar != 'p': # if the file doesn't end with p3. that means it doesn't end with mp3 format
            extFileFormat = fileFormat.split(".mp3", 1)[0] # in case there's something after the mp3, max split of 1 of .mp3, take the first index  
            extFileFormat += ".mp3" #appends .mp3 back into the file name to have correct format
            print("Extrananeous link found: " + extFileFormat)  
            request = requests.get(enclosureF, allow_redirects=True) 
            save_path = 'C:/Users/andyr/Downloads/Chrome Downloads/WorkStudy/Podcast Files/mountainhawk/MP3' #CHANGE download path of MP3
            file_name = extFileFormat #file name
            completeFilePath = os.path.join(save_path, file_name) # adds the two together to be read in next line so that the download is correct
            open(completeFilePath, 'wb').write(request.content) # 'wb' means that the file is opened for writing in binary mode
        else:
            print(fileFormat) #DEBUG and tells me what gets downloaded 
            request = requests.get(enclosureF, allow_redirects=True) 
            save_path = 'C:/Users/andyr/Downloads/Chrome Downloads/WorkStudy/Podcast Files/mountainhawk/MP3' #CHANGE  download path of MP3
            file_name = fileFormat #file name
            completeFilePath = os.path.join(save_path, file_name) # adds the two together to be read in next line so that the download is correct
            open(completeFilePath, 'wb').write(request.content) # 'wb' means that the file is opened for writing in binary mode
    # #Download Section End
    podcast_main.append(enclosure1)
    season = i.find("iseason").text
    podcast_main.append(season)
    episode = i.find("iepisode").text 
    podcast_main.append(episode)

    csvwriter.writerow(podcast_main)
podcast_data.close()


