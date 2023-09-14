from xlsxwriter import Workbook
import labels_constant as labels_const
import excel_constants as excel_const


def write_labels(workbook: Workbook) -> Workbook:
    labels_format = workbook.add_format()
    labels_format.set_align(excel_const.HEADERS_LABELS_ALIGN_LEFT)
    labels_format.set_bg_color(excel_const.HEADERS_LABELS_BG_COLOR)

    labels_list = [
        labels_const.PARENT_OBJECT,
        labels_const.CMODEL,
        labels_const.OBJECT_LOCATION,
        labels_const.LABEL,
        labels_const.TITLE,
        labels_const.CREATOR,
        labels_const.CONTRIBUTORS,
        labels_const.TYPE,
        labels_const.GENRE,
        labels_const.GENRE_URI,
        labels_const.DATE_CREATED,
        labels_const.YEAR,
        labels_const.SEASON,
        labels_const.DATE_CAPTURED,
        labels_const.PUBLISHER,
        labels_const.LANGUAGE_CODE,
        labels_const.LANGUAGE_TEXT,
        labels_const.FORMAT,
        labels_const.FORMAT_URI,
        labels_const.FILE_FORMAT,
        labels_const.DIMENSIONS,
        labels_const.DIGITAL_ORIGIN,
        labels_const.DESCRIPTION_ABSTRACT,
        labels_const.SUBJECT_TOPIC,
        labels_const.WEBSITE,
        labels_const.RIGHTS,
        labels_const.VOLUME_NUMBER,
        labels_const.ISSUE_NUMBER
    ]

    worksheet = workbook.add_worksheet()

    for col_num, label in enumerate(labels_list):
        worksheet.write(0, col_num, label, labels_format)

    return workbook
