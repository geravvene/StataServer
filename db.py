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
    try:
        last_date=''
        with open("date.txt", "r") as file:
            last_date = datetime.strptime(file.readline(), '%Y.%m.%d %H:%M:%S.')
        print(last_date)
        for row in data:
            row["DATE"]=datetime.strptime(row["DATE"]["$date"], '%Y-%m-%dT%H:%M:%S.000Z')
            if row["DATE"]>last_date:
                orders.append(row)
            else:
                with open("date.txt", "w+") as file:
                    file.write(datetime.strftime(orders[0]["DATE"]["$date"], '%Y.%m.%d %H:%M:%S.'))
                break                          
    except:
        orders=data
        for row in orders:
            row["DATE"]=datetime.strptime(row["DATE"]["$date"], '%Y-%m-%dT%H:%M:%S.000Z')
            row['TYPE']= 's' if row['TYPE']==1 else 'b'
        with open("date.txt", "w+") as file:
            file.write(datetime.strftime(orders[0]["DATE"], '%Y.%m.%d %H:%M:%S.'))
        
    sub1='to #' 
    removes=[]

    def rec_order(row):
        if sub1 in row['COMMENT']:
                id=int(row['COMMENT'].replace(sub1,''))
                index=find_by_key(orders, '_id', id)
                if index:
                    row['slices']=orders[index]
                    removes.append(orders[index])
                    return rec_order(orders[index])
                else:
                    return int(row['COMMENT'].replace(sub1,''))
        else:
            if 'from #' in row['COMMENT']:
                return row['COMMENT'][-4:][1 : -1] 
            else:
                return row['COMMENT'][1 : -1]  
        
    for row in orders:
        row['end']=rec_order(row)
    for row in removes:
        try:
            orders.remove(row)
        except:
            continue          

    removes=[]
    older=collection.find({ 'end' : {'$type':"number"}}).sort({'$natural': -1}).limit(10)

    for row in older:
        index=find_by_key(orders, '_id', row['end'])
        if index:
            removes.append(orders[index])
            collection.update_one({'_id': row['_id']}, {"$set": {'slices':orders[index], 'end':orders[index]['end']}})
    for row in removes:
        try:
            orders.remove(row)
        except:
            continue 
            
    orders.reverse()
    collection.insert_many(orders)


