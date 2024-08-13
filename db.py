from datetime import datetime
from pymongo import MongoClient

def add(data, name):
    client = MongoClient("mongodb+srv://geravvene:NJxN8XPdTKMe84YF@wordigma.rmxf6nd.mongodb.net/")
    db = client['StataBot']
    collection = db[name]

    orders=[]

    for row in data:
        if row["ENTRY"] !=0:
            orders.append(row)
    for row in orders:
        row["DATE"]=datetime.strptime(row["DATE"], '%Y.%m.%d %H:%M:%S')

    collection.insert_many(orders)   

