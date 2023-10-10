import os
import requests
import sys
from bs4 import BeautifulSoup
import feedparser

import generate_csv
import generate_excel
import get_podcast_data
from constants import file_constants as f_const


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


def get_xml_root(file_path: str) -> BeautifulSoup:
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
    print('=========================================')


def display_menu():
    """

    :return:
    """
    print("Please select an option:")
    print("1. Download Podcasts and CSV")
    print("2. Download ONLY Podcasts")
    print("3. Download ONLY CSV")
    print("4. Check Number of Podcasts")
    print("5. Exit")


def get_user_choice():
    """

    :return:
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

    :return:
    """
    while True:
        try:
            user_input = input('Please enter an RSS link or "q" to exit: ')
            # Strip whitespace from the input
            user_input = user_input.strip()

            if user_input == 'q':
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


if __name__ == "__main__":
    print('Welcome to the Podcast Archival CLI Tool!')
    display_cli_section_lines()
    while True:
        display_menu()
        display_cli_section_lines()
        user_choice = get_user_choice()

        if user_choice == 1:
            print('You have selected Download Podcasts and CSV')
            url = enter_valid_rss_link()
            xml_file_path = download_rss(url=url,
                                         file_name=f_const.RSS_NAME,
                                         file_extension=f_const.RSS_EXTENSION,
                                         save_path=f_const.RSS_PATH)
            print(f'The XML file is saved at: {xml_file_path}')
            display_cli_section_lines()

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

        if user_choice == 5:
            print('Thanks for using the Podcast Archival CLI Tool')
            sys.exit()


    # EDIT date here, will change later into cmd line interface
