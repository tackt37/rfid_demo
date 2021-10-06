import pandas as pd
import time
import datetime
import os
import csv
import urllib.request
from sqlalchemy import create_engine
import requests
import shutil
from inputimeout import inputimeout, TimeoutOccurred

server = 'fdx.database.windows.net'
database = 'FDX'
username = 'cips_root'
password = 'MI6-fallout!'
odbc_connect = urllib.parse.quote_plus(
    'DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD=' + password)
engine = create_engine('mssql+pyodbc:///?odbc_connect=' + odbc_connect,fast_executemany=True,encoding="utf-8")




def make_df(epc):
    df = pd.DataFrame({
        'datatime':[time_df,],
        'place':['DressingRoom',],
        'epc':[epc,]
    })
    return df

def insert_db(df):
    df.to_sql(
    'trace_record',
    index = False, 
    con = engine,
    if_exists = 'append',
    schema = "rfid_demo")

if __name__ == '__main__':
    while True:
        set_time = time.time()
        time_df = datetime.datetime.now()
        df = pd.DataFrame(columns=['timestamp','place','epc'])
        data_list = []
        while time.time() - set_time < 30:
            try:
                epc = inputimeout(prompt='>>', timeout=5)
                data_list.append(epc)
            except TimeoutOccurred:
                print('Timeout!')
                something = 'something'
            
        data_list = list(set(data_list))
        if len(data_list) > 0:
            for target in data_list:
                df = df.append({'timestamp' : time_df , 'place' : 'DressingRoom', 'epc' : target } , ignore_index=True)
            insert_db(df)
