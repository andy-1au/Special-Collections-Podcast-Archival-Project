import xlsxwriter

import add_labels_section
import add_data_section
from podcast_data import PodcastData
from constants import file_constants as f_const


def generate_excel(podcast_episodes_list: list[PodcastData]):
    """

    :param podcast_episodes_list:
    :return:
    """
    row_index = 0
    workbook = xlsxwriter.Workbook(f'{f_const.EXCEL_PATH}/{f_const.EXCEL_NAME}{f_const.EXCEL_EXTENSION}')

    row_index, worksheet = add_labels_section.write_labels(workbook=workbook, row_index=row_index)

    add_data_section.write_podcast_object_data(workbook=workbook, worksheet=worksheet,podcast_object_list=podcast_episodes_list, row_index=row_index)

    workbook.close()
