import xlsxwriter
from io import BytesIO

import add_labels_section

output = BytesIO()
workbook = xlsxwriter.Workbook(output)

add_labels_section.write_labels(workbook)

workbook.close()
output.write(workbook)


