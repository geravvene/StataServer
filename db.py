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
    
    last_order_date=collection.find().sort({'$natural': -1}).limit(1)[0]["DATE"]
    orders=[]

    for row in data:
        row["DATE"]=datetime.strptime(row["DATE"], '%Y.%m.%d %H:%M:%S')
        if row["DATE"] > last_order_date:
            orders.append(row)
        else: 
            break
        
    sub='to #'
    removes=[]
    for row in orders:
        print(row)
        if sub in row['COMMENT']:
            id=int(row['COMMENT'].replace(sub,''))
            index=find_by_key(orders, '_id', id)
            if index:
                row['PROFIT']+=orders[index]['PROFIT']
                row['SWAP']+=orders[index]['SWAP']
                row['COMMISSION']+=orders[index]['COMMISSION']
                row['TO']=orders[index]['COMMISSION']
                if sub in orders[index]['COMMENT']:
                    row['TO']=int(orders[index]['COMMISSION'].replace(sub,''))
                    
                removes.append(orders[index])
            else:
                row['TO']=id
   
    for row in removes:
        orders.remove(row)
        
    orders.reverse()
    
    collection.insert_many(orders)   


