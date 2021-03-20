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

def Merge(dict1, dict2):
    res = {**dict1, **dict2}
    return res

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

def check_in(dict_select):
    key = list(dict_select.keys())[0]
    s = dict_select[key]
    return '(' in str(s)

def fixPrereq(dict_prereqs):
    key = list(dict_prereqs.keys())[0]
    prereqs = dict_prereqs[key]
    for i in range(len(prereqs)):
        if type(prereqs[i]) != dict and '(' not in prereqs[i]:
            pass
        else:
            prereq = addAndOr(prereqs[i])
            try:
                if not check_in(prereq):
                    prereqs[i] = prereq
                else:
                    prereqs[i] = fixPrereq(prereq)
            except:
                print('prereq=',prereqs[i])
    dict_prereqs[key] = prereqs
    return dict_prereqs

def addPrereq():
    result = {}
    select = '''
        SELECT id,prereq_id FROM temp_claremontcourses WHERE prereq_id LIKE "%/%" OR prereq_id LIKE '%&%' ORDER BY ID ASC;
    '''
    selects = cur.execute(select)
    for x in selects:
        id, select = x
        dict_prereqs = addAndOr(select) #dict
        if check_in(dict_prereqs):
            dict_prereqs = fixPrereq(dict_prereqs)
        result[id] = dict_prereqs
    return result

def addPrereq_single():
    result = {}
    select = '''
        SELECT id,prereq_id FROM temp_claremontcourses WHERE prereq_id != '' AND NOT (prereq_id LIKE "%/%" OR prereq_id LIKE '%&%') ORDER BY ID ASC;
    '''
    selects = cur.execute(select)
    for x in selects:
        id, select = x
        result[id] = str(select[1:-1])
    return result

def addPrereq_none():
    result = {}
    select = '''
        SELECT id,prereq_id FROM temp_claremontcourses WHERE prereq_id == '' ORDER BY ID ASC;
    '''
    selects = cur.execute(select)
    for x in selects:
        id, select = x
        result[id] = ''
    con.commit()
    return result

def main():
    prereqs_specials = addPrereq()
    prereqs_nones = addPrereq_none()
    prereqs_singles = addPrereq_single()
    merged_prereqs = Merge(prereqs_specials,prereqs_nones)
    prereqs = Merge(prereqs_singles,merged_prereqs)
    return prereqs