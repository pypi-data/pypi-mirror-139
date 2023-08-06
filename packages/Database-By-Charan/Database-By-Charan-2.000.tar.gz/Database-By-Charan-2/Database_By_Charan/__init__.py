file='data.db'
import ast
import os.path
def getdata():
    global data
    if not os.path.isfile(file):
        data={}
        with open(file,'w') as dbs:
            dbs.write(str(data))
    with open(file,'r') as dbs:
            data=ast.literal_eval(dbs.readline())
    return data
def add(key,value):
    getdata()
    data[key]=value
    with open(file,'w') as dbs:
        dbs.write(str(data))
    return data
def val(key):
    getdata()
    if key in data:
        return data[key]
def delkey(key):
    getdata()
    if key in data:
        del data[key]
        with open(file,'w') as dbs:
            dbs.write(str(data))
        return data
def listkeys():
    getdata()
    lists=[]
    for x in data:
        lists.append(x)
    return lists
