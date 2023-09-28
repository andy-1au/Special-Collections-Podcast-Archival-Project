from xlsxwriter import Workbook
from xlsxwriter.workbook import Worksheet

from podcast_data import PodcastData
from constants import labels_constant as labels_const
from constants import excel_constants as excel_const


def write_podcast_object_data(workbook: Workbook, podcast_object_list: list[PodcastData], row_index: int):
    """
    This method writes the podcast episode data into the Excel sheet
    :param workbook: To help write the Excel file, for creating and referencing the worksheet
    :param podcast_object_list: The list of podcasts and their data
    :param row_index: To keep track of the index
    :return: None
    """
    internal_row_offset = 0
    try:
        data_format = workbook.add_format()
        data_format.set_font_name(excel_const.DATA_FONT_TYPE)
        data_format.set_font_size(excel_const.DATA_FONT_SIZE)
        data_format.set_align(excel_const.DATA_ALIGN_LEFT)

        worksheet = workbook.worksheets()[0]
        print('Writing data to excel sheet')
        for podcast_object in podcast_object_list:
            col = 0
            for attr, value in podcast_object.__dict__.items():
                worksheet.write(row_index + internal_row_offset, col, value, data_format)
                col += 1
            internal_row_offset += 1
        print('Successfully writen data to excel sheet')
    except:
        print('Failed to write data to excel sheet')



