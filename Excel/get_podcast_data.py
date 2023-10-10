from datetime import datetime, timezone
from dateutil import parser
from bs4 import BeautifulSoup

from podcast_data import PodcastData
from constants import xml_constants as xml_const
from constants import excel_constants as excel_const


def get_podcast_data(xml_root: BeautifulSoup, episodes_file_name: list[str]) -> list[PodcastData]:
    """
    Extract podcast episode metadata from an XML root and create a list of PodcastData objects.
    :param xml_root: The XML root containing podcast episode data.
    :param episodes_file_name: A list of episode file names needed for object_location.
    :return: A list of PodcastData objects containing podcast episode metadata.
    """
    podcast_list: list[PodcastData] = []
    try:
        episodes = xml_root.find_all(xml_const.ITEM)
        for episode in episodes:
            parent_object = excel_const.PARENT_OBJECT
            cmodel = excel_const.CMODEL
            object_location = episodes_file_name.pop(0)
            try:
                title = episode.title.text
            except AttributeError:
                title = ''
            label = title
            try:
                creator = episode.creator.text
            except AttributeError:
                creator = ''
            try:
                author_tag = episode.find('itunes:title')
                contributors = author_tag.text if author_tag is not None else episode.author.text
            except AttributeError:
                contributors = ''
            type = excel_const.TYPE
            genre = excel_const.GENRE
            genre_uri = excel_const.GENRE_URI
            try:
                date_non_formatted_text = episode.pubDate.text
                date_object = parse_and_format_date(date_non_formatted_text)
                date_created = date_object.strftime('%Y-%m-%d')
                year = date_object.strftime('%Y')
            except AttributeError:
                date_created = ''
                year = ''
            try:
                season = episode.season.text
            except AttributeError:
                season = ''
            current_date = datetime.now()
            date_captured = current_date.strftime("%Y-%m-%d")
            publisher = excel_const.PUBLISHER
            language_code = excel_const.LANGUAGE_CODE
            language_text = excel_const.LANGUAGE_TEXT
            format = excel_const.FORMAT
            format_uri = excel_const.FORMAT_URI
            file_format = excel_const.FILE_FORMAT
            try:
                dimensions = episode.duration.text
            except:
                dimensions = ''
            digital_origin = excel_const.DIGITAL_ORIGIN
            try:
                raw_description = episode.description.text
                non_formatted_description = BeautifulSoup(raw_description, 'html.parser')
                description_abstract = non_formatted_description.get_text()
            except:
                description_abstract = ''
            subject_topic = ''
            website = ''
            try:
                rights = excel_const.RIGHTS
            except AttributeError:
                rights = ''
            try:
                volume_number = episode.season.text
            except AttributeError:
                volume_number = ''
            try:
                issue_number = episode.episode.text
            except AttributeError:
                issue_number = ''

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
            podcast_list.append(podcast_object)
        # print(f'Number of podcasts: {len(podcast_list)}')
        return podcast_list
    except Exception as e:
        print(f'Error in parsing XML: {str(e)}')
        return []


def filter_episodes_by_date(xml_root: BeautifulSoup):
    """
    This method filters podcast episode URLs based on the specified date
    :param xml_root: The XML root containing podcast episode data
    :return: List of filtered episode URLs
    """
    filtered_urls = []
    try:
        while True:
            date_str = input("Enter a start date for downloading podcasts (YYYY-MM-DD) or type 'default' to download all podcasts: ")
            try:
                if date_str == 'default':
                    date_str = '2000-01-01'
                # Parse the specified date and make it offset aware for comparison purposes
                specified_date = datetime.strptime(date_str, '%Y-%m-%d').replace(tzinfo=timezone.utc)
                print(f'Specified Date: {specified_date}')
                break
            except ValueError:
                print("Invalid date format. Please use the format YYYY-MM-DD.")

        for episode in xml_root.find_all('item'):
            episode_date = parse_and_format_date(episode.pubDate.text).replace(tzinfo=timezone.utc)

            # Check if the episode's publication date is equal to or after the specified date
            if episode_date >= specified_date:
                episode_url = episode.enclosure.get('url')
                filtered_urls.append(episode_url)
    except Exception as e:
        print(f'Error in filtering episodes by date: {str(e)}')

    return filtered_urls


def parse_and_format_date(date_text) -> datetime:
    """
    Parse a date text in various formats and return a datetime.datetime object
    :param date_text: The date text string in various formats
    :return: A datetime.datetime object representing the parsed date and time or None if parsing fails.
    """
    try:
        date_object = parser.parse(date_text)
        return date_object
    except ValueError:
        return None


def test(xml_root: BeautifulSoup):
    episodes = xml_root.find_all(xml_const.ITEM)

    for episode in episodes:
        author_tag = episode.find('itunes:titless')
        author = author_tag.text
        print(author)
