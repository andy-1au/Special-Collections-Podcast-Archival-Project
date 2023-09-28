import xlsxwriter
from io import BytesIO

import add_labels_section
import add_data_section
from podcast_data import PodcastData
from constants import file_constants as f_const


def generate_excel(podcast_episodes_list: list[PodcastData]) -> BytesIO:
    """
    This is the main method that calls the functions below to generate the entire Excel worksheet for the podcast data
    :param podcast_episodes_list: The list of podcasts
    :return: A
    """
    try:
        print('Creating Excel memory buffer')
        excel_buffer = BytesIO()
        row_index = 0

        workbook = xlsxwriter.Workbook(f'{f_const.EXCEL_PATH}/{f_const.EXCEL_NAME}{f_const.EXCEL_EXTENSION}')
        row_index = add_labels_section.write_labels(workbook=workbook, row_index=row_index)
        add_data_section.write_podcast_object_data(workbook=workbook, podcast_object_list=podcast_episodes_list, row_index=row_index)
        workbook.close()

        excel_buffer.seek(0)

        print('Returning Excel memory buffer')
        return excel_buffer
    except:
        return None

