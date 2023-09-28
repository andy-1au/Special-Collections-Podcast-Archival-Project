import xlsxwriter

import add_labels_section
import add_data_section
from podcast_data import PodcastData
from constants import file_constants as f_const


def generate_excel(podcast_episodes_list: list[PodcastData]):
    """
    This is the main method that calls the functions below to generate the entire XLSX worksheet for the podcast data
    :param podcast_episodes_list: The list of podcasts
    :return:
    """
    row_index = 0

    workbook = xlsxwriter.Workbook(f'{f_const.EXCEL_PATH}/{f_const.EXCEL_NAME}{f_const.EXCEL_EXTENSION}')
    row_index = add_labels_section.write_labels(workbook=workbook, row_index=row_index)
    add_data_section.write_podcast_object_data(workbook=workbook, podcast_object_list=podcast_episodes_list, row_index=row_index)

    workbook.close()


