import os
import glob
import requests
import sys
from bs4 import BeautifulSoup
import feedparser

import generate_csv
import generate_excel
import get_podcast_data
from constants import file_constants as f_const
from constants import xml_constants as xml_const


def download_rss(url: str, file_name: str, file_extension: str, save_path: str) -> str:
    """
    Download an RSS feed from the specified URL and save it as an XML file.
    :param url: The URL of the RSS feed to download.
    :param file_name: The desired name of the downloaded file (excluding extension).
    :param file_extension: The file extension for the downloaded file (e.g., '.xml').
    :param save_path: The directory path where the downloaded file should be saved.
    :return: The full path of the saved XML file.
    """
    try:
        print('Downloading RSS Feed.')
        response = requests.get(url, allow_redirects=True)
        rss_path = os.path.join(save_path, file_name + file_extension)

        if response.status_code == 404:
            print('RSS Feed not found (404).')
            return ''

        response.raise_for_status()  # Raise an exception for other HTTP error codes

        print('Writing XML file.')
        open(rss_path, 'wb').write(response.content)
        print('An XML file has been generated.')

        return rss_path
    except requests.exceptions.RequestException as e:
        print(f'Failed to download RSS feed: {str(e)}')
        return ''


def get_xml_root(file_path: str) -> BeautifulSoup | None:
    """
    Parse an XML file and return its root as a BeautifulSoup object.
    :param file_path: The path to the XML file to be parsed.
    :return: A BeautifulSoup object representing the root of the XML.
    """
    try:
        print('Reading in XML file')
        with open(file_path, 'r', encoding='utf-8') as f:
            xml_content = f.read()
    except FileNotFoundError:
        print(f'Error: XML file not found at {file_path}')
        return None
    except Exception as e:
        print(f'Failed to read XML file: {str(e)}')
        return None

    try:
        print('Parsing XML file')
        return BeautifulSoup(xml_content, 'xml')
    except Exception as e:
        print(f'Failed to parse XML file: {str(e)}')
        return None


def get_podcast_episodes_file_name(urls: list[str]) -> list[str]:
    """
    Extract file names from a list of podcast episode URLs.
    :param urls: A list of podcast episode URLs.
    :return: A list of file names extracted from the URLs.
    """
    podcast_episode_file_name: list[str] = []
    try:
        print('Retrieving podcast episodes file name')
        for url in urls:
            # print(url)
            podcast_episode_name = url.split('/')[-1]
            # print(podcast_episode_name)
            podcast_episode_file_name.append(podcast_episode_name)
        print('Successfully retrieved a list of podcast episodes file name')
        return podcast_episode_file_name
    except Exception as e:
        print(f'Failed to retrieve a list of podcast episode file name: {str(e)}')
        return []


def get_podcast_episodes_urls(xml_root: BeautifulSoup) -> list[str]:
    """
    Extract podcast episode URLs from an XML root.
    :param xml_root: The BeautifulSoup object representing the root of the XML.
    :return: A list of podcast episode URLs.
    """
    urls: list[str] = []
    try:
        print('Finding podcast episodes URLs')
        podcast_episodes = xml_root.find_all('item')
        for podcast_episode in podcast_episodes:
            enclosure = podcast_episode.enclosure
            if enclosure and 'url' in enclosure.attrs:
                episode_url = enclosure['url']
                urls.append(episode_url)

        # print(f'Successfully found {len(urls)} podcast episodes URLs')
        print('Successfully found podcast episodes URLs')
        return urls
    except Exception as e:
        print(f'Failed to find podcast episodes URLs: {str(e)}')
        return []


def download_podcast_episodes(urls: list[str], save_path: str):
    """
    Download podcast episodes from a list of URLs and save them to the specified path.
    :param urls: A list of podcast episode URLs.
    :param save_path: The directory path where the episodes should be saved.
    :return: None
    """
    try:
        print('Downloading podcast episodes')
        for url in urls:
            podcast_episode_name = url.split('/')[-1]
            file_path = os.path.join(save_path, podcast_episode_name)

            try:
                response = requests.get(url)
                response.raise_for_status()  # Raise an exception for HTTP errors

                with open(file_path, 'wb') as episode_file:
                    episode_file.write(response.content)

                print(f'{podcast_episode_name} has been downloaded')
            except requests.exceptions.RequestException as e:
                print(f'Failed to download episode {podcast_episode_name}: {str(e)}')

        print('All podcasts have been downloaded')
        print('Connection to the server has been closed')
        print(f'Podcast episodes are saved at {f_const.PODCAST_PATH}/')
    except Exception as e:
        print(f'Failed to download podcast episodes: {str(e)}')


def display_cli_section_lines():
    """
    Display a section separator in the command line interface.
    :return: None
    """
    print('=========================================')


def display_menu():
    """
    Display a menu of options in the command line interface.
    :return: None
    """
    print("Please select an option:")
    print("1. Download Podcasts and CSV")
    print("2. Download ONLY Podcasts")
    print("3. Download ONLY CSV")
    print("4. Check Number of Podcasts")
    print("5. Exit")


def get_user_choice():
    """
    Get the user's choice by prompting for a number input.
    :return: The user's choice as an integer.
    """
    while True:
        try:
            choice = int(input('Enter the number corresponding to your choice: '))
            if 1 <= choice <= 5:
                return choice
            else:
                print('Invalid choice. Please enter a number between 1 and 5.')
        except ValueError:
            print('Invalid input. Please enter a valid number.')


def enter_valid_rss_link():
    """
    Prompt the user to enter a valid RSS link and check its validity.
    :return: A valid RSS link as a string or None if canceled or invalid.
    """
    while True:
        try:
            user_input = input('Please enter an RSS link or "q" to exit: ')
            # Strip whitespace from the input
            user_input = user_input.strip()

            if user_input.lower() == 'q':
                print('Thanks for using the Podcast Archival CLI :)')
                sys.exit()

            # Attempt to parse the user's input as an RSS feed
            rss_feed = feedparser.parse(user_input)

            # Check if the parsing was successful
            if rss_feed.entries:
                print('RSS link is valid.')
                return user_input  # Return the rss link
            else:
                print('Invalid RSS link. Please enter a valid RSS URL.')
        except KeyboardInterrupt:
            print('\nOperation canceled by user.')
            return None  # Return None if the user cancels
        except Exception as e:
            print(f'An error occurred: {str(e)}. Please try again.')
            

def require_xml_file(): 
    """
    Prompt the user if they want to download the rss feed or they already have it in the XML folder
    :return: A boolean value, yes == True, no == False
    """
    while True:
        try:
            user_input = input("Do you want to download an RSS file via a link?\nEnter 'yes' or 'no' or 'q' to quit: ")
            # Strip whitespace from the input
            user_input = user_input.strip()

            if user_input.lower() == 'q':
                print('Thanks for using the Podcast Archival CLI :)')
                sys.exit()

            if user_input.lower() == 'yes':
                return True
            elif user_input.lower() == 'no':
                return False 
            else: 
                print("Invalid choice. Please enter 'yes' or 'no' or 'q' to quit")
        except KeyboardInterrupt:
            print('\nOperation canceled by user.')
            return None  # Return None if the user cancels
        except Exception as e:
            print(f'An error occurred: {str(e)}. Please try again.')
            

def display_and_choose_xml(folder_path):
    """
    Display a list of XML files in the specified folder and let the user choose one
    :param folder_path (str): The path to the folder containing XML files
    :return: str or None: The path of the chosen XML file, or None if no file was chosen or if the folder doesn't contain any XML files
    """
    # Get a list of XML files in the specified folder
    xml_files = glob.glob(os.path.join(folder_path, '*.xml'))

    if not xml_files:
        print(f"No XML files found in {folder_path}")
        return None

    print(f"Available XML files in {folder_path}:")
    for i, xml_file in enumerate(xml_files, start=1):
        print(f"{i}. {os.path.basename(xml_file)}")

    while True:
        try:
            # Get user input for choosing a file
            choice = int(input("Enter the number of the XML file you want to choose (or 0 to exit): "))
            
            if choice == 0:
                sys.exit()
            elif 1 <= choice <= len(xml_files):
                chosen_file = xml_files[choice - 1]
                print(f"You've chosen: {os.path.basename(chosen_file)}")
                return chosen_file
            else:
                print("Invalid choice. Please enter a valid number.")
        except ValueError:
            print("Invalid input. Please enter a number.")


if __name__ == "__main__":
    print('Welcome to the Podcast Archival CLI Tool!')
    display_cli_section_lines()
    while True:
        display_menu()
        display_cli_section_lines()
        user_choice = get_user_choice()
        if user_choice == 1:
            print('You have selected Download Podcasts and CSV')
            if require_xml_file(): 
                url = enter_valid_rss_link()
                xml_file_path = download_rss(url=url,
                                            file_name=f_const.RSS_NAME,
                                            file_extension=f_const.RSS_EXTENSION,
                                            save_path=f_const.RSS_PATH)
                print(f'The XML file is saved at: {xml_file_path}')
                display_cli_section_lines()
            else: 
                xml_file_path = display_and_choose_xml(folder_path=f_const.RSS_PATH)
                
            xml_root = get_xml_root(file_path=xml_file_path)
            podcast_episodes_urls = get_podcast_episodes_urls(xml_root=xml_root)
            podcast_episodes_file_name = get_podcast_episodes_file_name(urls=podcast_episodes_urls)
            display_cli_section_lines()

            podcast_episodes_list = get_podcast_data.get_podcast_data(xml_root=xml_root,
                                                                      episodes_file_name=podcast_episodes_file_name)
            generate_excel.generate_excel(podcast_episodes_list=podcast_episodes_list)
            generated_excel_file = f'{f_const.EXCEL_PATH}/{f_const.EXCEL_NAME}{f_const.EXCEL_EXTENSION}'
            print(f'The excel file is saved at: {generated_excel_file}')
            display_cli_section_lines()

            csv_buffer = generate_csv.excel_to_csv(input_excel_file=generated_excel_file)
            with open(f'{f_const.CSV_PATH}/{f_const.CSV_NAME}{f_const.CSV_EXTENSION}', 'wb') as f:
                f.write(csv_buffer.read().encode('utf-8'))
            print(f'The CSV file is saved at: {f_const.CSV_PATH}/{f_const.CSV_NAME}{f_const.CSV_EXTENSION}')
            display_cli_section_lines()

            filtered_urls = get_podcast_data.filter_episodes_by_date(xml_root=xml_root)
            download_podcast_episodes(urls=filtered_urls, save_path=f_const.PODCAST_PATH)
            display_cli_section_lines()
        elif user_choice == 2:
            print('You have selected Download ONLY Podcasts')
            if require_xml_file(): 
                url = enter_valid_rss_link()
                xml_file_path = download_rss(url=url,
                                            file_name=f_const.RSS_NAME,
                                            file_extension=f_const.RSS_EXTENSION,
                                            save_path=f_const.RSS_PATH)
                print(f'The XML file is saved at: {xml_file_path}')
                display_cli_section_lines()
            else: 
                xml_file_path = display_and_choose_xml(folder_path=f_const.RSS_PATH)

            xml_root = get_xml_root(file_path=xml_file_path)
            filtered_urls = get_podcast_data.filter_episodes_by_date(xml_root=xml_root)
            download_podcast_episodes(urls=filtered_urls, save_path=f_const.PODCAST_PATH)
            display_cli_section_lines()
        elif user_choice == 3:
            print('You have selected Download ONLY CSV')
            if require_xml_file(): 
                url = enter_valid_rss_link()
                xml_file_path = download_rss(url=url,
                                            file_name=f_const.RSS_NAME,
                                            file_extension=f_const.RSS_EXTENSION,
                                            save_path=f_const.RSS_PATH)
                print(f'The XML file is saved at: {xml_file_path}')
                display_cli_section_lines()
            else: 
                xml_file_path = display_and_choose_xml(folder_path=f_const.RSS_PATH)

            xml_root = get_xml_root(file_path=xml_file_path)
            podcast_episodes_urls = get_podcast_episodes_urls(xml_root=xml_root)
            podcast_episodes_file_name = get_podcast_episodes_file_name(urls=podcast_episodes_urls)
            display_cli_section_lines()

            podcast_episodes_list = get_podcast_data.get_podcast_data(xml_root=xml_root,
                                                                      episodes_file_name=podcast_episodes_file_name)
            generate_excel.generate_excel(podcast_episodes_list=podcast_episodes_list)
            generated_excel_file = f'{f_const.EXCEL_PATH}/{f_const.EXCEL_NAME}{f_const.EXCEL_EXTENSION}'
            print(f'The excel file is saved at: {generated_excel_file}')
            display_cli_section_lines()

            csv_buffer = generate_csv.excel_to_csv(input_excel_file=generated_excel_file)
            with open(f'{f_const.CSV_PATH}/{f_const.CSV_NAME}{f_const.CSV_EXTENSION}', 'wb') as f:
                f.write(csv_buffer.read().encode('utf-8'))
            print(f'The CSV file is saved at: {f_const.CSV_PATH}/{f_const.CSV_NAME}{f_const.CSV_EXTENSION}')
            display_cli_section_lines()
        elif user_choice == 4:
            print('You have selected Check Number of Podcasts')
            if require_xml_file(): 
                url = enter_valid_rss_link()
                xml_file_path = download_rss(url=url,
                                            file_name=f_const.RSS_NAME,
                                            file_extension=f_const.RSS_EXTENSION,
                                            save_path=f_const.RSS_PATH)
                print(f'The XML file is saved at: {xml_file_path}')
                display_cli_section_lines()
            else: 
                xml_file_path = display_and_choose_xml(folder_path=f_const.RSS_PATH)
                
            xml_root = get_xml_root(file_path=xml_file_path)
            num_podcasts = xml_root.find_all(xml_const.ITEM)
            print(f'There are {len(num_podcasts)} podcasts')
            # print(f'Removing the downloaded XML file at {xml_file_path}')
            os.remove(xml_file_path)
            # print(f'THe XML file at {xml_file_path} has been removed')
            display_cli_section_lines()
        elif user_choice == 5:
            print('Thanks for using the Podcast Archival CLI Tool')
            sys.exit()
