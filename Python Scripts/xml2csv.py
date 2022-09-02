import xml.etree.ElementTree as XET
import csv

tree = XET.parse('nasdaq.xml')
root = tree.getroot()

nasdaq_data = open('nasdaq.csv', 'w')

csvwriter = csv.writer(nasdaq_data)
nasdaq_header = []

count = 0 
for i in root.findall('./channel/item'):
    nasdaq_main = []
    if count == 0:
        title = i.find("title").tag
        nasdaq_header.append(title)
        description =  i.find("description").tag
        nasdaq_header.append(description)
        link = i.find("link").tag
        nasdaq_header.append(link)
        pubDate = i.find("pubDate").tag
        nasdaq_header.append(pubDate)
        duration = i.find("iduration").tag
        nasdaq_header.append(duration)
        enclosure = i.find("enclosure").tag
        nasdaq_header.append(enclosure)
        season = i.find("iseason")
        nasdaq_header.append(season)
        episode = i.find("iepisode").tag
        nasdaq_header.append(episode)

        csvwriter.writerow(nasdaq_header)
        count+=1
    
    title = i.find("title").text
    nasdaq_main.append(title)
    description = i.find("description").text
    nasdaq_main.append(description)
    link = i.find("link").text
    nasdaq_main.append(link)
    pubDate = i.find("pubDate").text
    nasdaq_main.append(pubDate)
    duration = i.find("iduration").text
    nasdaq_main.append(duration)
    enclosure = i.find("enclosure").attrib
    enclosure1 = enclosure.get("url")
    nasdaq_main.append(enclosure1)
    season = i.find("iseason").text
    nasdaq_main.append(season)
    episode = i.find("iepisode").text
    nasdaq_main.append(episode)
    csvwriter.writerow(nasdaq_main)

nasdaq_data.close()





