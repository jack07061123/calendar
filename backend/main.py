import gspread
from oauth2client.service_account import ServiceAccountCredentials as SAC
from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel
from key import sheet_key
Json = "calendar.json"
Url = ["https://spreadsheets.google.com/feeds"]
Connect = SAC.from_json_keyfile_name(Json, Url)
GoogleSheets = gspread.authorize(Connect)
Sheet = GoogleSheets.open_by_key(sheet_key)
Sheets = Sheet.sheet1


##########Insert Data Into Database
# dataTitle = ['date', 'time', 'event', 'place']
# datas = ["03/11", "15:00", "dinner", "taipei"]
# #先塞一筆假資料
# Sheets.append_row(dataTitle)
# Sheets.append_row(datas)
# print("寫入成功")
# print(Sheets.get_all_values())


# ----- fast api -----
app = FastAPI()

from fastapi.middleware.cors import CORSMiddleware
origins = [
    "http://localhost",
    "http://localhost:3000",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def getAllData():
    return Sheets.get_all_records()

class Info(BaseModel):
    id: int
    data: list
@app.post("/addNewEvents")
def getInformation(info: Info):
    Sheets.append_row(info.data)
    return {"status": "SUCCESS", "data": info}
