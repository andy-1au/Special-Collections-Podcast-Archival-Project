import pandas as pd
import io


def excel_to_csv(input_excel_file) -> io.StringIO:
    """
    Converts an Excel file to a CSV file and returns it as a file object.
    :param input_excel_file: Path to the input Excel file.
    :return: io.StringIO: A file-like object containing the CSV data.
    """
    try:
        df = pd.read_excel(input_excel_file, sheet_name=0)
        csv_buffer = io.StringIO()
        df.to_csv(csv_buffer, index=False)

        # Reset the buffer position to the beginning, so that it can be read from the beginning
        csv_buffer.seek(0)
        return csv_buffer
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None
