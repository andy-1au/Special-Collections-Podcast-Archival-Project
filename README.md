# Special-Collections-Podcast-Archival-CLI-Tool
The Podcast Archival CLI Tool is a Python command-line application that allows you to download and archive podcast episodes from RSS feeds. You can also generate CSV and Excel files to organize the podcast episode data. This README provides information on how to use the tool effectively.

## Prerequisites
Before using the Podcast Archival CLI Tool, make sure you have the following prerequisites installed on your system:

- Python 3.7 or higher 
  - Here's a [link](https://www.python.org/downloads/) to download the current latest version of python
- Required Python libraries (install them using pip): 
  
  - ```pip install requirements.txt```

## Installation 
Clone the repository or download the source code to your local machine.
```commandline
git clone https://github.com/andy-1au/Special-Collections-Podcast-GUI-Project.git
```
Navigate to the project directory:
```commandline
cd CLI
```
Install the required Python libraries using pip: 
```commandline
pip install requirements.txt
```

## Usage
To use the Podcast Archival CLI Tool, follow these steps:

Run the tool using the following command (make sure you are in the CLI/ directory): 
```commandline
make run
```

You will see the main menu with the following options:

1. Download Podcasts and CSV: This option downloads podcast episodes, generates CSV and Excel files, and archives the episodes.

2. Download ONLY Podcasts: This option downloads podcast episodes and archives them without generating CSV or Excel files.

3. Download ONLY CSV: This option generates only the CSV and Excel files without downloading the podcast episodes.

4. Check Number of Podcasts: This option only checks the number of podcasts in an RSS feed.

5. Exit: Exit the tool.

Choose the option that best fits your needs and follow the on-screen instructions.

For options 1, 2, and 3, you will be prompted to enter the RSS feed URL. Follow the prompts and enter the RSS link or type "q" to exit.

Option 4 allows you to check the number of podcasts in an RSS feed.

Option 5 exits the tool.

## Contributing
If you want to contribute to the Podcast Archival CLI Tool, feel free to submit issues, suggestions, or pull 
requests on the [GitHub repository](https://github.com/andy-1au/Special-Collections-Podcast-GUI-Project).

## License 
This project is licensed under the MIT License - see the [LICENSE](https://github.com/andy-1au/Special-Collections-Podcast-GUI-Project/blob/main/LICENSE) file for details.

## Author
Andy Lau - andyolau888@gmail.com

## Acknowledgements
- Alex Japha: Provided valuable project oversight and guidance. 
- Dennis Lam: Played a key role in the development of the initial version of this tool, particularly in parsing iTunes 
tags within the RSS feed.