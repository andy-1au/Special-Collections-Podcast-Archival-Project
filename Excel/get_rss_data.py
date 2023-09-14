import os
import re
import requests
import untangle

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
#
#
# def open_XML(xmlFile):
#     tree = XET.parse(xmlFile)
#     root = tree.getroot()
#     return root


def download_rss(url: str, file_name: str, file_extension: str, save_path: str):
    print('Downloading RSS Feed')
    response = requests.get(url, allow_redirects=True)
    rss_path = os.path.join(save_path, file_name + file_extension)
    open(rss_path, 'wb').write(response.content)
    print('RSS feed has been downloaded')
    return rss_path


if __name__ == "__main__":
    xml_file = download_rss(url=f_const.RSS_URL,
                            file_name=f_const.RSS_NAME,
                            file_extension=f_const.RSS_EXTENSION,
                            save_path=f_const.RSS_PATH)

    # cleaned_xml_destination = "/path/to/your/cleaned/xml/destination"
    # cleaned_xml_file_name = "cleanedXML"
    #
    # format_xml(xml_file, cleaned_xml_destination, cleaned_xml_file_name)
    #
    # podcast_destination = "/path/to/your/podcast/destination"
    # download_PD(xml_file, podcast_destination)
