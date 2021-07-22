import requests
from bs4 import BeautifulSoup
import json
from selenium.webdriver import Chrome
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
import re
import time
from selenium.webdriver.support.ui import Select
import xlrd
import pandas as pd
import numpy as np
import sqlite3

con = sqlite3.connect("claremontcourses.db", check_same_thread=False)
con.row_factory = sqlite3.Row

select = '''
    SELECT * FROM temp_claremontcourses;
'''
cur = con.cursor()
selects = cur.execute(select)
database_references = dict()

for select in selects:
    database_references[select["code"].strip()] = [select["title"].strip(), select["description"].strip()]

def retrieveText(ID):
    """
    Return a string from a css ID
    """
    text = driver.page_source
    soup = BeautifulSoup(text, 'html.parser')
    text = soup.find(id=ID).get_text()
    return text 

def getRequirements(tag):
    """
    Return a list of texts
    """
    text = driver.page_source
    soup = BeautifulSoup(text, 'html.parser')
    tds = soup.find_all(tag)
    l = len(tds)
    for i in range(l):
        td = tds[i]
        # Do something
        td = td.get_text()
        tds[i] = td
    return tds

perm_list = list()
special_list = set()
track_code = set()

f = open('update_claremontcourses.json')
datas = json.load(f)

new_data = dict()
for data in datas:
    for key, value in data.items():
        new_data[key] = value

def updatePERM(fulfillRequirement):
    j = 1
    while True:
        if j < 10:
            j = '0' + str(j)
        # Choose code
        try:
            j = str(j)
            print('pg0_V_rptCourses_ctl' + j + '_lnkCourse')
            select = driver.find_element_by_id('pg0_V_rptCourses_ctl' + j + '_lnkCourse')
            code = retrieveText('pg0_V_rptCourses_ctl' + j + '_lnkCourse')
            code = (code[:-3]).replace(' ', '')
            print("code=", code) 
            if new_data[code]["fulfillRequirements"] == "":
                new_data[code]["fulfillRequirements"] = [fulfillRequirement]
            else:
                new_data[code]["fulfillRequirements"] = list(set(new_data[code]["fulfillRequirements"] + [fulfillRequirement]))  
        except:
            print("Cant find code")
            print('==================================================')
            return new_data
        j = int(j) + 1             
    return

url = 'https://mycampus2.pitzer.edu/ics'
new_url = "https://mycampus2.pitzer.edu/ICS/Course_Schedule/"
driver = Chrome()
driver.get(url)
driver.find_element_by_id('siteNavBar_ctl00_btnLogin').click()
select = Select(driver.find_element_by_id('selCollege'))
select.select_by_visible_text('Pitzer College')
# Login
username = 'hoachu'
password = 'Ditmeping0.8'
# Username
inputUsername = driver.find_element_by_id("dispname")
inputUsername.send_keys(username)
# Password
inputPassword = driver.find_element_by_id("password")
inputPassword.send_keys(password)
time.sleep(30)
print("Done Sleeping...")


subjectLists = [27, 32, 34, 38, 39, 40, 42, 54, 87, 88, 89, 90, 71, 75, 76, 103, 138, 139, 140, 141, 142, 143, 144, 146, 147, 148, 149,
151, 152, 153, 154, 155, 156, 157, 158, 159, 178, 179, 180, 181, 182, 183, 184, 185, 186, 187]

subjectReferences = ['CMC History GE','CMC Lab Science GE', 'CMC Literature Humanities GE', 'CMC Mathematics GE', 'CMC Philosophy GE', 'CMC Psychology GE', 
'CMC Religious Studies GE', 'HMC Core Lab', 'HMC Common Core', 'HMC First Year PE', 'HMC HSA Courses', 'HMC HSA Writing Intensive', 'First Year Seminar', 
'Freshman Humanities Seminar', 'Freshman Writing Seminar', 'Interdisciplinary Studies', 'PO Analyzing Difference', 
'PO Area 1 Requirement', 'PO Area 2 Requirement', 'PO Area 3 Requirement', 'PO Area 4 Requirement', 'PO Area 5 Requirement', 
'PO Area 6 Requirement', 'PO Language Requirement', 'PO Phys Ed Requirement', 'PO Speaking Intensive', 'PO Writing Intensive', 
'PZ Humanities/Fine Arts', 'PZ Intercultural Understanding-Global', 'PZ Intercultural Understanding-Local', 'PZ Natural Science', 
'PZ Quantitative Reasoning', 'PZ Social Justice Theory', 'PZ Social Responsibility Praxis', 'PZ Social/Behavioral Science', 
'PZ Writing Educational Objective', 'SC 1st-year appropriate', 'SC Core GE', 'SC Fine Arts GE', 'SC Foreign Language GE', 
'SC Gender and Women\'s Studies GE', 'SC Letters GE', 'SC Mathematics GE', 'SC Natural Science GE', 'SC Race and Ethnic Studies GE', 'SC Social Science GE'
]

for i in range(len(subjectLists)):
    index = subjectLists[i]
    print(i, " ", subjectReferences[i])
    driver.get(new_url)
    dropdown = driver.find_element_by_id("pg0_V_tabSearch_ddlAdditional")
    droplist = Select(dropdown)
    droplist.select_by_index(index)
    driver.find_element_by_id('pg0_V_tabSearch_btnSearch').click()
    perm_dict = updatePERM(subjectReferences[i])
    with open("update_claremontcourses_test.json", "w") as fp:
        json.dump(perm_dict, fp, ensure_ascii = False, indent=4)     
driver.quit()