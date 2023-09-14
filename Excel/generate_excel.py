import xlsxwriter

from constants import file_paths_constants as fp_const
import add_labels_section


workbook = xlsxwriter.Workbook(f'{fp_const.PATH}/{fp_const.NAME}.{fp_const.EXTENSION}')
add_labels_section.write_labels(workbook)
workbook.close()

