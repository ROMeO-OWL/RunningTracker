# import gspread
# from oauth2client.service_account import ServiceAccountCredentials

# class GoogleSheetsService:
#     def __init__(self, credentials_path: str, sheet_id: str):
#         scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
#         creds = ServiceAccountCredentials.from_json_keyfile_name(credentials_path, scope)
#         self.client = gspread.authorize(creds)
#         self.sheet = self.client.open_by_key(sheet_id).sheet1

#     def add_run(self, date: str, distance: float, time: str, pace: str):
#         # Inserta una nueva fila al final de la hoja de cálculo
#         self.sheet.append_row([date, distance, time, pace])