from pathlib import Path

import PySimpleGUI as sg 
import pandas as pd



# def convert_to_csv():



#Layout
layout = [
        #each line in the layout list is a row 
        #LATER - add placeholder and disappear when clicked
        [sg.Text("RSS Feed Link:"), sg.Input(key="-IN2-")],
        [sg.Text("XML File:"), sg.Input(key="-IN-"), sg.FileBrowse(file_types=(("XML Files", "*.xml"),))], 
        [sg.Text("Podcast Destination Folder:"), sg.Input(key="-POD-"), sg.FolderBrowse()],
        [sg.Text("CSV Destination Folder:"), sg.Input(key="-CSV-"), sg.FolderBrowse()],
        [sg.Exit(), sg.Button("Download Podcasts"), sg.Button("Convert To CSV")]    
]

window = sg.Window("Podcast Downloader", layout)

while True: 
    event, values = window.read() #get values and events from the GUI
    print(event, values) #DEBUG
    if event == sg.WIN_CLOSED or event == "Exit": #WIN_CLOSED = X button, Exit = Exit button
        break #break out of the loop and close the window
    if event == "Download Podcasts":
        print("Download Podcasts") #DEBUG
        
    if event == "Convert To CSV":
        print("Convert To CSV") #DEBUG
window.close() 