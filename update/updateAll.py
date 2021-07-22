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

def reference_list():
    c = set()
    # checks = ['PERM', "permission", "PZ only", "PZ students only", "CMC students only"]
    for y in range(2, worksheet.nrows):
        # checkPerm = str(worksheet.cell_value(y, 11))
        # if any(check in checkPerm for check in checks):
        #     pass
        # else:
        code = str(worksheet.cell_value(y,0).replace(' ','').strip('.'))
        # prof = str(worksheet.cell_value(y,3)).rstrip('.')
        if code == '':
            j = y-1
            while (str(worksheet.cell_value(j,0).replace(' ','').strip('.')) == ''):
                j -= 1
            code = str(worksheet.cell_value(j,0).replace(' ','').strip('.'))
        # if prof == '':
        #     p = y-1
        #     while(str(worksheet.cell_value(p,3)) == ''):
        #         p -= 1
        #     prof = str(worksheet.cell_value(p,3)).rstrip('.')
        c.add(code[:-2])
    return c



# Structure
###########################################################
# final = [
#         {
#         code (Text) : {
#         college (Text),
#         major (Text),
#         title (Text),
#         description (Text),
#         link (None),
#         syllabus (None),
#         equivalent (None),
#         leadto (''),
#         fulfillRequirements (List/''),
#         term ('2021FA'),
#         perm (List/''),
#         prereq (Text, ''),
#         prereq_id (''),
#         corequisite (Text / 'None'),
#         corequisite_id (''),
#         concurrent (Text / 'None'),
#         concurrent_id (''),     
#         }  
#      }
# ]
###########################################################

perm_list = list()
def updatePERM(keyword):
    print("keyword=", keyword)
    j = 1
    while True:
        select = Select(driver.find_element_by_id('pg0_V_tabSearch_ddlCourseRestrictor')) 
        select.select_by_index(3)
        inputCode = driver.find_element_by_id("pg0_V_tabSearch_txtCourseRestrictor")
        inputCode.send_keys(Keys.CONTROL, 'a')
        inputCode.send_keys(Keys.BACKSPACE)
        inputCode.send_keys(keyword)
        driver.find_element_by_id('pg0_V_tabSearch_btnSearch').click()
        # Found!
        if j < 10:
            j = '0' + str(j)
        # Choose code
        try:
            j = str(j)
            select = driver.find_element_by_id('pg0_V_rptCourses_ctl' + j + '_lnkCourse')
            code = retrieveText('pg0_V_rptCourses_ctl' + j + '_lnkCourse')
            code = (code[:-3]).replace(' ', '')
            print("code=", code, end=" ")
            select.click()
        except:
            print("Cant find code")
            print('==================================================')
            return

        # initiate the ultimate dictionary

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

        # College, Major, Title, Description stuffs
        ################################################################
        ref_colleges = {"SC":"Scripps", "CM":"CMC", "PZ":"Pitzer", "PO":"Pomona", "HM": "Mudd"}

        

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
                print("profs=", profs, end=" ")
                k = int(k) + 1
            except:
                break
        # Choose course requirements
        try:
            driver.find_element_by_id('pg0_V_lnkbCourseRequisites').click()
            tds = getRequirements('td')  # list
            restrictions = []
            for restriction in tds:
                if "Section Requirement".lower() in restriction.lower():
                    restrictions.append(restriction)
            print('restrictions=', restrictions)
            # Pick to dict
            if len(restrictions) == 0:
                try: 
                    perm_dict[code]["perm"] += [profs]
                except:
                    perm_dict[code] = [profs]
        except:
            try: 
                perm_dict[code]["perm"] += [profs]
            except:
                perm_dict[code]["perm"] = [profs]
        j = int(j) + 1
        ################################################################  
        perm_list.append(perm_dict)
        with open("update_claremontcourses.json", "w") as file:
            file.write(json.dumps(perm_list, ensure_ascii = False, indent=4))

        driver.get(new_url)        
    return perm_list

path = r"FA21-5C-Sched.xls"
workbook = xlrd.open_workbook(path)
worksheet = workbook.sheet_by_index(0)

references = reference_list()
print(references)

url = 'https://mycampus2.pitzer.edu/ics'
new_url = "https://mycampus2.pitzer.edu/ICS/Course_Schedule/"
driver = Chrome()
# driver.get(url)
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

# driver.find_element_by_id('pg0_V_tabSearch_gblAdvSearch').click()

# for code in references:
#     driver.get(new_url)
#     perm_list = updatePERM(code)

# print('perm_list=', perm_list)
# with open("update_claremontcourses.json", "w") as file:
#     file.write(json.dumps(perm_list, ensure_ascii = False, indent=4))

driver.quit()