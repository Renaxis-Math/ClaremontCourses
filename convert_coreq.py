import pandas as pd
import numpy as np
import sqlite3
import requests
import json
from bs4 import BeautifulSoup
import re
import time

con = sqlite3.connect("claremontcourses.db", check_same_thread=False)
cur = con.cursor()

def addAnd(prereqs):
    result = {
        'and':None
    }
    prereqs_and = re.split(r'&\s*(?![^()]*\))', prereqs[1:-1])
    temp = prereqs_and[0]
    if ':' in temp:
        s = ""
        temp = temp.replace('(','').replace(')','')
        where = temp.find(':')
        start = int(temp[:where])
        end = int(temp[where+1:])+1
        for x in range(start,end):
            s += str(x) + '/'
        s = s.rstrip('/')
        xs = ('('+ s + ")")
        xs = str(xs)
        # print("xs=",xs)
        return addOr(xs)
    if temp != prereqs[1:-1]:
        result['and'] = prereqs_and
        return result
    else:
        return None
        
def addOr(prereqs):
    result = {
        'or':None
    }
    prereqs_or = re.split(r'/\s*(?![^()]*\))', prereqs[1:-1])
    result['or'] = prereqs_or
    return result

def addAndOr(select):
    prereqs = None
    if '(' not in select:
        return
    else:
        prereqs = addAnd(select)
        if prereqs == None:
            prereqs = addOr(select)
        return prereqs

def addCorereq():
    result = {}
    select = '''
        SELECT id,corequisite_id FROM temp_claremontcourses ORDER BY ID ASC;
    '''
    selects = cur.execute(select)
    con.commit()
    for x in selects:
        id, select = x
        if select != '-1':
            select = '(' + str(select) + ')'
            dict_prereqs = addAndOr(select) #dict
            # print(dict_prereqs)
        else:
            dict_prereqs = ''
        result[id] = dict_prereqs
    return result

def main():
    corequisites = addCorereq() 
    return corequisites