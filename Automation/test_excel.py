from utils.excel_reader import ExcelReader

reader = ExcelReader("testdata/login_data.xlsx")

data = reader.get_data("login")

print(data)