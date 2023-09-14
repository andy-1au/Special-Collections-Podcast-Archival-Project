import os
import re
import requests
from bs4 import BeautifulSoup

from constants import file_constants as f_const


# def format_xml(xmlFile, rssDest, fileName):
#     print("Cleaning up XML file")
#     savePath = os.path.join(rssDest, fileName + ".xml")
#
#     tree = XET.parse(xmlFile)
#     root = tree.getroot()
#     pattern = re.compile(r'{.*}')
#
#     for i in root.findall('./channel/item/'):
#         if (pattern.match(i.tag) and 'itunes' in i.tag):
#             i.tag = re.sub(r'{.*}', 'itunes_', i.tag)
#
#     tree.write(savePath, encoding='utf-8', xml_declaration=True)
#
#
# def download_PD(xmlFile, podcastDest):
#     print("Downloading Podcasts")
#     root = open_XML(xmlFile)
#
#     for child in root.findall('./channel/item/'):
#         tag = child.tag
#         if tag == 'enclosure':
#             url = child.attrib.get('url')
#             if url.find('/'):
#                 fileName = url.rsplit('/', 1)[1]
#                 filePath = os.path.join(podcastDest, fileName)
#             download = requests.get(url, allow_redirects=True)
#             print(fileName + " has been downloaded")
#             open(filePath, 'wb').write(download.content)
#     print("All podcasts have been downloaded")
#     download.close()
#     print("Connection to server has been closed")


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


def get_episodes(xml_root: BeautifulSoup) -> list[str]:
    """

    :param xml_root:
    :return:
    """
    episodes_list = [str]
    try:
        print('Finding episodes')
        episodes = xml_root.find_all('item')
        for episode in episodes:
            print(episode.title.text)
            episodes_list.append(episode.title.text)

        return episodes_list
    except:
        print('Failed to find episodes. Error in parsing XML')
        return []


def get_episodes_urls(xml_root: BeautifulSoup) -> list[str]:
    """

    :param xml_root:
    :return:
    """
    urls: list[str] = []
    try:
        print('Finding episodes urls')
        episodes = xml_root.find_all('item')
        for episode in episodes:
            print(episode.enclosure.get('url'))
            urls.append(episode.enclosure.get('url'))

        return urls
    except:
        print('Failed to find episodes url. Error in parsing XML')
        return []


def download_episodes(urls: list[str], save_path: str):
    """

    :param urls:
    :param save_path:
    :return:
    """
    # try:
    print('Downloading episodes')
    for url in urls:
        print(url)
        episode_name = url.split('/')[-1]
        print(episode_name)
        file_path = os.path.join(save_path, episode_name)
        # print(file_path)
        response = requests.get(url)
        open(file_path, 'wb').write(response.content)
        print(f'{episode_name} has been downloaded')
        response.close()
    print('All podcasts have been downloaded')
    print('Connection to server has been closed')
    # except Exception as e:
    #     print(e)


if __name__ == "__main__":
    xml_file_path = download_rss(url=f_const.RSS_URL,
                                 file_name=f_const.RSS_NAME,
                                 file_extension=f_const.RSS_EXTENSION,
                                 save_path=f_const.RSS_PATH)
    print(f'XML is saved at: {xml_file_path}')

    podcast = get_xml_root(file_path=xml_file_path)
    episodes_urls = get_episodes_urls(xml_root=podcast)
    # print(episodes_urls)
    download_episodes(urls=episodes_urls, save_path=f_const.PODCAST_PATH)

    # episodes = get_episodes(xml_root=podcast)

    # cleaned_xml_destination = "/path/to/your/cleaned/xml/destination"
    # cleaned_xml_file_name = "cleanedXML"
    #
    # format_xml(xml_file, cleaned_xml_destination, cleaned_xml_file_name)
    #
    # podcast_destination = "/path/to/your/podcast/destination"
    # download_PD(xml_file, podcast_destination)
