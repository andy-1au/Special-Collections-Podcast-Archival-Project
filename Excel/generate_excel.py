import xlsxwriter

from constants import file_constants as f_const
import add_labels_section


workbook = xlsxwriter.Workbook(f'{f_const.EXCEL_PATH}/{f_const.EXCEL_NAME}{f_const.EXCEL_EXTENSION}')
add_labels_section.write_labels(workbook)
workbook.close()

