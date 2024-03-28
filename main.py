from fastapi import FastAPI
from db import DataHandler
import datetime
from pymongo import MongoClient
from fastapi_utils.tasks import repeat_every
import pytz
import os

tz = pytz.timezone('Asia/Kolkata')


app = FastAPI()

usrnm = os.getenv('USER', 'manav')
passwrd = os.getenv('PASSWORD', '')

uri = "mongodb+srv://"+usrnm+":"+passwrd+"@jobbl.0rotaoy.mongodb.net/"

client = MongoClient(uri)
db = client['my11']
table = db['matches']

mc = DataHandler(table=table)
start = datetime.datetime(2024,1,1,19,30,0).time()
end = datetime.datetime(2024,1,1,23,59,0).time()

@app.on_event('startup')
@repeat_every(seconds=60*5) 
def updateDB():

    print("repeat function active")
    now = datetime.datetime.now(tz).time()

    if  start <= now and now <= end:
        print('update requested')
        mc.updateMatches()
    
    pass