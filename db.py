from datetime import datetime
from pymongo import MongoClient

def find_by_key(iterable, key, value):
    for index, dict_ in enumerate(iterable):
        if dict_[key] == value:
            return index
        
def add(data, name):
    client = MongoClient("mongodb+srv://geravvene:NJxN8XPdTKMe84YF@wordigma.rmxf6nd.mongodb.net/")
    db = client['StataBot']
    collection = db[name]
    
    orders=[]

    for row in data:
        row["DATE"]=datetime.strptime(row["DATE"], '%Y.%m.%d %H:%M:%S')
        orders.append(row)

    orders.reverse()
    
    collection.insert_many(orders)   


