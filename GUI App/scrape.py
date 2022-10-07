import requests
import xml.etree.ElementTree as XET
import PySimpleGUI as sg

#tutorial used https://codeburst.io/building-an-rss-feed-scraper-with-python-73715ca06e1f

def scraping(url):
    try:
        r = requests.get(url)
        newRSSName = url.split("/")+".xml"
        open("/Users/dennis/Work Study/Special-Collections-Podcast-GUI-Project/XML/"+newRSSName , "wb").write(r.content)
        return print('The scraping job succeeded', r.status_code)
    except Exception as e:
        print("The scraping job failed. See exception:")
        print(e)
    
def run(links):        
    print('Starting scraping Process')
    scraping(links)
    print("Finished scraping")

scraping("https://feeds.captivate.fm/gogetters/")
        