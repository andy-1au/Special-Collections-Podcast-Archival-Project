from datetime import datetime
from bs4 import BeautifulSoup

from podcast_data import PodcastData
from constants import xml_constants as xml_const
from constants import excel_constants as excel_const


def get_podcast_data(xml_root: BeautifulSoup, episodes_file_name: list[str]) -> list[PodcastData]:
    """
    This method gets all metadata needed for the list of podcast objects
    :param xml_root: The xml tree root
    :param episodes_file_name: The episode file name needed for object_location
    :return: A list of podcast episodes objects
    """
    podcast_list: list[PodcastData] = []
    try:
        episodes = xml_root.find_all(xml_const.ITEM)
        for episode in episodes:
            # print('Creating podcast object')
            parent_object = excel_const.PARENT_OBJECT
            cmodel = excel_const.CMODEL
            object_location = episodes_file_name.pop(0)
            label = ''
            title = episode.title.text
            creator = episode.creator.text
            author_tag = episode.find('itunes:title')
            contributors = author_tag.text if author_tag is not None else episode.author.text
            type = excel_const.TYPE
            genre = excel_const.GENRE
            genre_uri = excel_const.GENRE_URI
            date_non_formatted_text = episode.pubDate.text
            date_object = datetime.strptime(date_non_formatted_text, '%a, %d %b %Y %H:%M:%S %z')
            date_created = date_object.strftime('%Y-%m-%d')
            year = date_object.strftime('%Y')
            season = episode.season.text
            current_date = datetime.now()
            date_captured = current_date.strftime("%Y-%m-%d")
            publisher = excel_const.PUBLISHER
            language_code = excel_const.LANGUAGE_CODE
            language_text = excel_const.LANGUAGE_TEXT
            format = excel_const.FORMAT
            format_uri = excel_const.FORMAT_URI
            file_format = excel_const.FILE_FORMAT
            dimensions = episode.duration.text
            digital_origin = excel_const.DIGITAL_ORIGIN
            raw_description = episode.description.text
            non_formatted_description = BeautifulSoup(raw_description, 'html.parser')
            description_abstract = non_formatted_description.get_text()
            subject_topic = ''
            website = ''
            rights = excel_const.RIGHTS
            volume_number = episode.season.text if episode.season.text is not None else ''
            issue_number = episode.episode.text if episode.episode.text is not None else ''

            podcast_object = PodcastData(parent_object=parent_object, cmodel=cmodel, object_location=object_location,
                                         label=label,
                                         title=title, creator=creator, contributors=contributors, type=type,
                                         genre=genre, genre_uri=genre_uri,
                                         date_created=date_created, year=year, season=season,
                                         date_captured=date_captured, publisher=publisher, language_code=language_code,
                                         language_text=language_text, format=format, format_uri=format_uri,
                                         file_format=file_format, dimensions=dimensions, digital_origin=digital_origin,
                                         description_abstract=description_abstract, subject_topic=subject_topic,
                                         website=website, rights=rights, volume_number=volume_number,
                                         issue_number=issue_number)
            # print('Podcast object created')
            podcast_list.append(podcast_object)
        print(f'Number of podcasts: {len(podcast_list)}')
        return podcast_list
    except:
        print('Failed to find episodes. Error in parsing XML')
        return []


def test(xml_root: BeautifulSoup):
    episodes = xml_root.find_all(xml_const.ITEM)

    for episode in episodes:
        author_tag = episode.find('itunes:titless')
        author = author_tag.text
        print(author)
