import os
import requests
from bs4 import BeautifulSoup

import generate_csv
import generate_excel
import get_podcast_data
from constants import file_constants as f_const


def download_rss(url: str, file_name: str, file_extension: str, save_path: str) -> str:
    """

    :param url:
    :param file_name:
    :param file_extension:
    :param save_path:
    :return:
    """
    try:
        print('Downloading RSS Feed')
        response = requests.get(url, allow_redirects=True)
        rss_path = os.path.join(save_path, file_name + file_extension)

        print('Writing XML file')
        open(rss_path, 'wb').write(response.content)
        print('An XML file has been generated')

        return rss_path
    except:
        print('Failed to generate XML file')
        return ''


def get_xml_root(file_path: str) -> BeautifulSoup:
    """

    :param file_path:
    :return:
    """
    try:
        print('Reading in XML file')
        with open(file_path, 'r', encoding='utf-8') as f:
            xml_content = f.read()
    except:
        print('Failed to read in XML file')

    try:
        print('Parsing XML file')
        return BeautifulSoup(xml_content, 'xml')
    except:
        print('Failed to parse XML file')
        return None


def get_podcast_episodes_file_name(urls: list[str]) -> list[str]:
    """
    
    :param urls: 
    :return: a list of podcast_episodes file name
    """
    podcast_episode_file_name: list[str] = []
    try:
        print('Getting podcast episodes file name')
        for url in urls:
            # print(url)
            podcast_episode_name = url.split('/')[-1]
            # print(podcast_episode_name)
            podcast_episode_file_name.append(podcast_episode_name)
        print('Successfully retrieved a list of podcast episodes file name')
        return podcast_episode_file_name
    except:
        print('Failed to retrieve a list of podcast episode file name')
        return []


def get_podcast_episodes_urls(xml_root: BeautifulSoup) -> list[str]:
    """

    :param xml_root:
    :return:
    """
    urls: list[str] = []
    try:
        print('Finding podcast episodes urls')
        podcast_episodes = xml_root.find_all('item')
        for podcast_episode in podcast_episodes:
            print(podcast_episode.enclosure.get('url'))
            urls.append(podcast_episode.enclosure.get('url'))

        return urls
    except:
        print('Failed to find podcast episodes url. Error in parsing XML')
        return []


def download_podcast_episodes(urls: list[str], save_path: str):
    """
    
    :param urls: 
    :param save_path: 
    :return: 
    """
    try:
        print('Downloading podcast episodes')
        for url in urls:
            # print(url)
            podcast_episode_name = url.split('/')[-1]
            # print(podcast episode_name)
            file_path = os.path.join(save_path, podcast_episode_name)
            # print(file_path)
            response = requests.get(url)
            open(file_path, 'wb').write(response.content)
            print(f'{podcast_episode_name} has been downloaded')
            response.close()
        print('All podcasts have been downloaded')
        print('Connection to server has been closed')
    except:
        print('Failed to download podcast episodes')


if __name__ == "__main__":
    xml_file_path = download_rss(url=f_const.RSS_URL,
                                 file_name=f_const.RSS_NAME,
                                 file_extension=f_const.RSS_EXTENSION,
                                 save_path=f_const.RSS_PATH)
    print(f'XML is saved at: {xml_file_path}')
    xml_root = get_xml_root(file_path=xml_file_path)
    podcast_episodes_urls = get_podcast_episodes_urls(xml_root=xml_root)
    podcast_episodes_file_name = get_podcast_episodes_file_name(urls=podcast_episodes_urls)
    podcast_episodes_list = get_podcast_data.get_podcast_data(xml_root=xml_root,
                                                              episodes_file_name=podcast_episodes_file_name)
    generate_excel.generate_excel(podcast_episodes_list=podcast_episodes_list)
    generated_excel_file = f'{f_const.EXCEL_PATH}/{f_const.EXCEL_NAME}{f_const.EXCEL_EXTENSION}'
    print(generated_excel_file)

    csv_buffer = generate_csv.excel_to_csv(input_excel_file=generated_excel_file)
    with open(f'{f_const.CSV_PATH}/{f_const.CSV_NAME}{f_const.CSV_EXTENSION}', 'wb') as f:
        f.write(csv_buffer.read().encode('utf-8'))

    download_podcast_episodes(urls=podcast_episodes_urls, save_path=f_const.PODCAST_PATH)
