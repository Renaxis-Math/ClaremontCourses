import json
import re
import sqlite3

def listToString(l):
    l = list(set(l))
    res = ""
    for i in l:
        res = res + i + "; "
    res = res[:-2]
    return res

con = sqlite3.connect("claremontcourses.db", check_same_thread=False)
con.row_factory = sqlite3.Row




select = '''
    SELECT * FROM temp_claremontcourses;
'''
update = '''
    UPDATE temp_claremontcourses SET fulfillRequirements = ?, term = ?, perm = ?
    WHERE code = ?;
'''
cur = con.cursor()
selects = cur.execute(select)
database_references = dict()

for select in selects:
    database_references[select["code"]] = [select["fulfillRequirements"], select["term"], select['perm']]
# for key,value in database_references.items():
#     print(value[1])

  
# Opening JSON file
f = open('update_claremontcourses_test.json')
n = open('special_update.json')
# returns JSON object as 
# a dictionary
data = json.load(f)
# new = json.load(n)
keys = list(data)
regex = r'[0-9]'
# Iterating through the json
# list
collected = dict()
trash = list()
count = 1
for key in keys:
    value = data[key]
    if value["fulfillRequirements"] != "":
        value["fulfillRequirements"] = list(set(value["fulfillRequirements"]))
        value["fulfillRequirements"] = listToString(value["fulfillRequirements"])
    try:
        database_references[key][0] = value["fulfillRequirements"]

        if database_references[key][1] == "":
            database_references[key][1] = "2021FA"
        else:
            database_references[key][1] = database_references[key][1] + "; 2021FA"
    
        if value["perm"] != "":
            value["perm"][0] = list(set(value["perm"][0]))
            value["perm"][0] = listToString(value["perm"][0])
            database_references[key][2] = value["perm"][0]
        else:
            database_references[key][2] = ""
        t = (database_references[key][0], database_references[key][1], database_references[key][2], key)
        cur.execute(update, t)   
        con.commit()         
    except KeyError:
        trash += [key]
        count += 1
        pass

# Closing file
f.close()