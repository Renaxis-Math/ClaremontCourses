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

perm_list = list()

def listToString(l):
    l = list(set(l))
    res = ""
    for i in l:
        res = res + i + "; "
    res = res[:-2]
    return res

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

def update(keyword, originalCode):
    print("keyword=", keyword)
    j = 1
    while True:
        # select = Select(driver.find_element_by_id('pg0_V_tabSearch_ddlCourseRestrictor')) 
        # select.select_by_index(3)
        # Found!
        if j < 10:
            j = '0' + str(j)
        # Choose code
        try:
            j = str(j)
            select = driver.find_element_by_id('pg0_V_rptCourses_ctl' + j + '_lnkCourse')
            code = retrieveText('pg0_V_rptCourses_ctl' + j + '_lnkCourse')
            code = (code[:-3]).replace(' ', '')                 
        except:
            print("Cant find code")
            print('==================================================')
            return perm_list 

        if code == originalCode:
            select.click()
            perm_dict = {
                code:  {
                    "college": str(),
                    "major": str(),
                    "title": str(),
                    "description": str(),
                    "link": "None",
                    "syllabus": "None",
                    "equivalent": "None",
                    "leadto" :'',
                    "fulfillRequirements" : "", #(List/'')
                    "term": '2021FA',
                    "perm": "", #(List/'')
                    "prereq": "", #(Text, '')
                    "prereq_id": '',
                    "corequisite": "None", #(Text / 'None')
                    "corequisite_id": '',
                    "concurrent":"None", #(Text / 'None')
                    "concurrent_id": '',     
                }  
            } 
        else:
            j = int(j) + 1
            continue           

        # College, Major, Title, Description stuffs
        ################################################################
        if code == originalCode:
            # Fluctuate each semester
            ref_colleges = {"SC":"Scripps", "CM":"CMC", "PZ":"Pitzer", "PO":"Pomona", "HM": "Mudd", "JP": "CMC", "AF": "Scripps", "KS": "Keck", "JT": "Scripps", "CH": "Pitzer"}
            description = retrieveText("pg0_V_lblCourseDescValue").strip()
            description = re.sub(r'[^A-Za-z0-9.,;:\- ]+', '', description)
            perm_dict[code]["description"] = description
            # Get title
            title = driver.find_element_by_class_name('col-lg-10').text.strip()
            regex = r'[a-zA-Z].*\('
            title = re.findall(regex, title)[0]
            title = title[:-1].strip()        
            perm_dict[code]["title"] = title
            # Get college
            perm_dict[code]["college"] = ref_colleges[code[-2:]]
            # Get fulfillRequirements
            try:
                hasFulfill = driver.find_element_by_id("pg0_V_lblCourseAreaValue")
                fulfillRequirements = hasFulfill.find_elements_by_tag_name("div")
                for fulfillRequirement in fulfillRequirements:
                    fulfillRequirement = fulfillRequirement.text
                    regex = r'[a-zA-Z].*\('
                    fulfillRequirement = re.findall(regex, fulfillRequirement)[0]
                    fulfillRequirement = fulfillRequirement[:-1].strip()
                    print("fulfillRequirement=",fulfillRequirement)
                    try:
                        perm_dict[code]["fulfillRequirements"] = list(set(perm_dict[code]["fulfillRequirements"] + [fulfillRequirement]))
                    except:
                        perm_dict[code]["fulfillRequirements"] = [fulfillRequirement]
                        pass
            except:
                pass

            ################################################################


            # PERM stuff
            ################################################################
            # Choose professor
            k = 1
            profs = []
            while True:
                if k < 10:
                    k = '0' + str(k)
                k = str(k)
                try:
                    select = driver.find_element_by_id(
                        'pg0_V_rptInst_ctl'+ k + '_lblInstructorValue')
                    prof = retrieveText('pg0_V_rptInst_ctl' +
                                        k + '_lblInstructorValue')
                    prof = prof.strip()
                    profs.append(prof)
                    k = int(k) + 1
                except:
                    break
            # Choose course requirements
            try:
                driver.find_element_by_id('pg0_V_lnkbCourseRequisites').click()
                tds = getRequirements('td')  # list
                restrictions = []
                print(tds)
                prerequisites = []
                corequisites = []
                for i in range(len(tds)):
                    restriction = tds[i]
                    coursecode_regex = r'[A-Z]+ *[0-9]+ *[A-Z]+'
                    if "Section Requirement".lower() in restriction.lower():
                        restrictions += [restriction]
                        restrictions = list(set(restrictions))
                    if "Concurrent".lower() in restriction.lower():
                        perm_dict[code]["concurrent"] = listToString(re.findall(coursecode_regex, tds[i+1]))
                        perm_dict[code]["concurrent"] = perm_dict[code]["concurrent"].replace(" ", '')
                        print("concurrent=", perm_dict[code]["concurrent"])
                    if "Prerequisite".lower() in restriction.lower():
                        prerequisites.append(re.findall(coursecode_regex, tds[i+1]))

                    if ("Co-Requisite".lower() in restriction.lower()) or ("CoRequisite".lower() in restriction.lower()):
                        corequisites.append(re.findall(coursecode_regex, tds[i+1]))

                if len(prerequisites) > 1:
                    perm_dict[code]["prereq"] = listToString(prerequisites)
                    perm_dict[code]["prereq"] = perm_dict[code]["prereq"].replace(" ", '')
                    print('prereq=', perm_dict[code]["prereq"])         
                if len(corequisites) > 1:
                    perm_dict[code]["corequisite"] = listToString(corequisites)
                    perm_dict[code]["corequisite"] = perm_dict[code]["corequisite"].replace(" ", '')
                    print("coreq=",perm_dict[code]["corequisite"])                               
                # Pick to dict
                if len(restrictions) == 0:
                    try: 
                        perm_dict[code]["perm"] += [profs]
                    except:
                        perm_dict[code]["perm"] = [profs]
            except:
                try: 
                    perm_dict[code]["perm"] += [profs]
                except:
                    perm_dict[code]["perm"] = [profs]
            j = int(j) + 1
            ################################################################  
            if code:
                try:
                    perm_list.append(perm_dict)
                    with open("newCourses.json", "w") as file:
                        file.write(json.dumps(perm_list, ensure_ascii = False, indent=4))
                except:
                    print("WRONG HERE: ", code)
                    print("WRONG HERE: ", perm_dict)    
            driver.get(new_url)              
        return perm_list


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

f = open("special_update.json")
new = json.load(f)

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

for code in new:
    regex = r'[0-9]+[A-Z]+'
    keyword = re.sub(regex, "", code)
    inputCode = driver.find_element_by_id("pg0_V_tabSearch_txtCourseRestrictor")
    inputCode.send_keys(Keys.CONTROL, 'a')
    inputCode.send_keys(Keys.BACKSPACE)
    inputCode.send_keys(keyword)
    driver.find_element_by_id('pg0_V_tabSearch_btnSearch').click()    
    perm_list = update(keyword, code)  
    if perm_list != []:
        with open("newCourses.json", "w") as file:
            file.write(json.dumps(perm_list, ensure_ascii = False, indent=4))      