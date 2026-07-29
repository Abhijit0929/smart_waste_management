import openpyxl


def get_excel_data(file_path, sheet_name):
    """
    Reads rows from the specified Excel sheet and returns them as a list of dicts.
    Each dict represents a row with keys as the header values from the first row.
    """
    workbook = openpyxl.load_workbook(file_path)
    sheet = workbook[sheet_name]
    data = []

    # Get header row
    headers = [cell.value for cell in sheet[1]]

    # Read values starting from row 2
    for row in sheet.iter_rows(min_row=2, values_only=True):
        if any(row):  # skip entirely empty rows
            row_dict = dict(zip(headers, row))
            data.append(row_dict)

    return data
