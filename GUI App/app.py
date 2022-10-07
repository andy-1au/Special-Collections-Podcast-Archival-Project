import tkinter as tk #for GUI
from tkinter import filedialog, Text #pick the apps 
import os 

root = tk.Tk() 

# xmlPath = 'C:/Users/andyr/Desktop/Special-Collections-Podcast-GUI-Project/XML'
# csvPath = 'C:/Users/andyr/Desktop/Special-Collections-Podcast-GUI-Project/CSV'

# podcastFolderPath = 'C:/Users/andyr/Desktop/Special-Collections-Podcast-GUI-Project/Podcasts'

# def downloadPodcast():
#     print("Downloading Podcast")
#     for child in root.findall('./channel/item/'): #finds all tags in xml file under the item tag
#         tag = child.tag
#         if tag == 'enclosure':
#             url = child.attrib.get('url')
#             if url.find('/'): #finds the last '/' in the url
#                 fileName = url.rsplit('/', 1)[1] #gets the file name from the url
#                 filePath = os.path.join(podcastFolderPath, fileName) #creates a path for the file to be saved
#             download = requests.get(url, allow_redirects=True) #downloads the file
#             print(url + " has been downloaded") 
#             open(filePath, 'wb').write(download.content) #writes the file to the path


#asks user to select a folder to save the podcasts
#askdirectory() only lets user select a folder
def podcast_Folder():
    podcastFolderPath = filedialog.askdirectory(initialdir="/", title="Select Desired Folder") 
    pdPathLabel = tk.Label(root, text="Save Podcasts Path: " + podcastFolderPath)
    # Create a label to display the path of the podcast folder
    pdPathLabel.pack()
    print(podcastFolderPath)

#asks user to select the RSS xml file and save the path 
def RSS_Feed():
    xmlPath = filedialog.askopenfilename(initialdir="/", title="Select Desired RSS", filetypes=(("xml files", "*.xml"), ("all files", "*.*")))
    # Create a label to display the path of the rss feed
    xmlPathLabel = tk.Label(root, text="RSS Feed Path: " + xmlPath)
    xmlPathLabel.pack()
    print(xmlPath)

# def downloadPodcast():
#     print("Downloading Podcast")
#     for child in root.findall('./channel/item/'): #finds all tags in xml file under the item tag
#         tag = child.tag
#         if tag == 'enclosure':
#             url = child.attrib.get('url')
#             if url.find('/'): #finds the last '/' in the url
#                 fileName = url.rsplit('/', 1)[1] #gets the file name from the url
#                 filePath = os.path.join(podcastFolderPath, fileName) #creates a path for the file to be saved
#             download = requests.get(url, allow_redirects=True) #downloads the file
#             print(url + " has been downloaded") 
#             open(filePath, 'wb').write(download.content) #writes the file to the path


#attach the canvas to the root
canvas = tk.Canvas(root, height=700, width=700, bg="#263D42") 
canvas.pack() #pack the canvas to the root so it can be seen

frame = tk.Frame(root, bg="white") #create a frame
frame.place(relwidth=0.8, relheight=0.8, relx=0.1, rely=0.1) #place the frame in the middle of the canvas

# button for selecting the rss feed
chooseRSS = tk.Button(root, text="Select RSS Feed", padx=10, pady=5, fg="white", bg="#263D42", command=RSS_Feed) 
chooseRSS.pack() 

# button for selecting the folder to save the podcasts
choosePodcastFolder = tk.Button(root, text="Select Podcasts Folder", padx=10, pady=5, fg="white", bg="#263D42", command=podcast_Folder) 
choosePodcastFolder.pack() 

# make an entry box for rss feed, add a float label in the entry box
enterRSS = tk.Entry(root, width=50, borderwidth=5)
enterRSS.insert(0, "Enter RSS Feed")
enterRSS.pack()

root.mainloop() #similar to html, this is what keeps the window open