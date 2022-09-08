import gspread
from db import engine
import pandas
from gspread_dataframe import set_with_dataframe


def upload():
    gc = gspread.service_account(filename='creds.json')
    sh = gc.open('Dataox_test').sheet1
    sql = "SELECT * FROM ad_list"
    df = pandas.read_sql(sql, engine)
    set_with_dataframe(sh, df)
