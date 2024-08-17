from datetime import datetime
from pymongo import MongoClient

def add(data, name):
    client = MongoClient("mongodb+srv://geravvene:NJxN8XPdTKMe84YF@wordigma.rmxf6nd.mongodb.net/")
    db = client['StataBot']
    collection = db[name]
    
    last_order_date=collection.find().sort({'$natural': -1}).limit(1)[0]["DATE"]
    orders=[]

    for row in data:
        row["DATE"]=datetime.strptime(row["DATE"], '%Y.%m.%d %H:%M:%S')
        if row["DATE"] > last_order_date:
            orders.append(row)
        else: 
            break
    orders.reverse()
    collection.insert_many(orders)   


