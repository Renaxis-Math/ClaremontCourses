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

majors = {'THEA':"Theater", 
'MUS':"Music", 
'LEAD':"Leadership", 
'NEUR':"Neuroscience", 
'EA':"Environmental Analysis", 
'PHYS':"Physics", 
'GLAS':"Institute for Global/Local Action Studies", 'WRIT':"Writing", 'CHLT':"Chicanx Latinx Studies", 
'BIOL':"Biology", 'ITAL':"Italian", 'POLI':"Politics and Political Studies", 'AFRI':"Africana Studies", 
'SPCH':"Speech", 
'ANTH':"Anthropology", 'PORT':"Portuguese", 'GEOG':"Geography", 'SPAN':"Spanish", 'ENGR':"Engineering", 'GEOL':"Geology", 
'MS':"Media Studies", 'ASAM':"Asian American Studie", 'FREN':"French", 'GRMT':"German Literature in English Translation", 
'GERM':"German", 'ECON':"Economics", 'HMSC':"Humanities and Study of Culture", 'PE':"Physical Education", 'CSCI':"Computer Science", 
'FIN':"Master of Arts in Finance", 'GOVT':"Government", 'GWS':"Gender and Women's Studies", 'CHEM':"Chemistry", 'ID':"Interdisciplinary", 'ASTR':"Astronomy", 
'ORST':"Organizational Studies", 
'POST':"Politics and Political Studies", 
'ENGL':"English", 
'MATH':"Mathematics", 
'LGCS':"Linguistics and Cognitive Science", 
'RLST':"Religious Studies", 
'STS':"Science, Technology, and Society", 
'ART':"Art", 
'ARHI':"Art History", 
'LIT':"Literature", 
'SOC':"Sociology", 
'HIST':"History", 
'PSYC':"Psychology"}

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
        code = code[:-2]
        regex = r'[0-9]'
        i = code.find(re.findall(regex, code)[0])
        c.add(code[:i].strip())
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
special_list = set()
track_code = set()

# initiate the ultimate dictionary



def updatePERM(fulfillRequirement):
    j = 1
    while True:
        # select = Select(driver.find_element_by_id('pg0_V_tabSearch_ddlCourseRestrictor')) 
        # select.select_by_index(3)
        # inputCode = driver.find_element_by_id("pg0_V_tabSearch_txtCourseRestrictor")
        # inputCode.send_keys(Keys.CONTROL, 'a')
        # inputCode.send_keys(Keys.BACKSPACE)
        # inputCode.send_keys(keyword)
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
            if code not in track_code:
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
        except:
            print("Cant find code")
            print('==================================================')
            return perm_list 

        # College, Major, Title, Description stuffs
        ################################################################
        if code and not (code in track_code):
            ref_colleges = {"SC":"Scripps", "CM":"CMC", "PZ":"Pitzer", "PO":"Pomona", "HM": "Mudd"}
            description = retrieveText("pg0_V_lblCourseDescValue").strip()
            description = re.sub(r'[^A-Za-z0-9.,;:\- ]+', '', description)
            perm_dict[code]["description"] = description
            # Get title
            title = driver.find_element_by_class_name('col-lg-10').text.strip()
            regex = r'[a-zA-Z].*\('
            title = re.findall(regex, title)[0]
            title = title[:-1].strip()        
            perm_dict[code]["title"] = title
        # Get fulfillRequirements
        try:
            # hasFulfill = driver.find_element_by_id("pg0_V_lblCourseAreaValue")
            # fulfillRequirements = hasFulfill.find_elements_by_tag_name("div")
            # for fulfillRequirement in fulfillRequirements:
            #     fulfillRequirement = fulfillRequirement.text
            #     regex = r'[a-zA-Z].*\('
            #     fulfillRequirement = re.findall(regex, fulfillRequirement)[0]
            #     fulfillRequirement = fulfillRequirement[:-1].strip()
            #     print("fulfillRequirement=",fulfillRequirement)
            #     try:
            #         perm_dict[code]["fulfillRequirements"] += [fulfillRequirement]
            #         perm_dict[code]["fulfillRequirements"] = list(set(perm_dict[code]["fulfillRequirements"]))
            #     except:
            #         perm_dict[code]["fulfillRequirements"] = [fulfillRequirement]
            #         pass
            perm_dict[code]["fulfillRequirements"] += [fulfillRequirement]
        except:
            perm_dict[code]["fulfillRequirements"] = [fulfillRequirement]
            pass
        try:
            temp = database_references[code]
            #     if perm_dict[code]["title"].lower() == database_references[code][0].lower() or perm_dict[code]["description"].lower() in database_references[code][1].lower():
            #         pass
            #     else:
            #         special_list.append(code)
            # else:
            #     special_list.append(code)
        except:
            special_list.add(code)
            with open("special_update_new.json", "w") as file:
                file.write(json.dumps(list(special_list), ensure_ascii = False, indent=4))              
            print("new_code=", code)
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
        print("profs=", profs, end=" ")
        # Choose course requirements
        try:
            driver.find_element_by_id('pg0_V_lnkbCourseRequisites').click()
            tds = getRequirements('td')  # list
            restrictions = []
            for restriction in tds:
                if "Section Requirement".lower() in restriction.lower():
                    restrictions += [restriction]
                    restrictions = list(set(restrictions))
                if "Concurrent".lower() in restriction.lower():
                    perm_dict[code]["concurrent"] = code[:-2] + "L" + code[-2:]
            print('restrictions=', restrictions)
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
        if code and not (code in track_code):
            try:
                perm_list.append(perm_dict)
                # with open("update_claremontcourses.json", "w") as file:
                #     file.write(json.dumps(perm_list, ensure_ascii = False, indent=4))
                track_code.add(code)
            except:
                print("WRONG HERE: ", code)
                print("WRONG HERE: ", perm_dict)    
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
time.sleep(180)
print("Done Sleeping...")

# driver.find_element_by_id('pg0_V_tabSearch_gblAdvSearch').click()
# references = {'ECON', 'LIT', 'PPE', 'RUSS', 'ART', 'GWS', 'MCBI', 'CSCI', 'CHIN', 'POST', 'CGS', 'CHNT', 'RLST', 'GREK', 'ENGR', 'RUST', 'SOSC', 
# 'ID', 'MLLC', 'AMST', 'STS', 'SPAN', 'DANC', 'BIOL', 'EA', 'ANTH', 'PSYC', 'GRMT', 'CLAS', 'KORE', 'LEAD', 'FREN', 'GOVT', 
# 'MOBI', 'ORST', 'ARBC', 'NEUR', 'FIN', 'IR', 'CASA', 'MATH', 'CORE', 'JAPN', 'CSMT', 'CHLT', 'HMSC', 'EDUC', 'SOC', 
# 'PONT', 'PHYS', 'ENGL', 'DS', 'SPCH', 'THEA', 'PE', 'POLI', 'ASIA', 'PPA', 'GEOG', 'CHEM', 'ASTR', 'AFRI', 'LATN', 
# 'MS', 'WRIT', 'ARHI', 'CHST', 'FWS', 'MUS', 'GEOL', 'GERM', 'ITAL', 'HIST', 'ARCN', 'COGS', 'PHIL', 'FGSS', 'PORT', 'ASAM', 'MSL', 'LGCS', 'FHS', 'GLAS'}
# for code in references:
#     driver.get(new_url)
#     perm_list = updatePERM(code)
#     if perm_list != []:
#         with open("update_claremontcourses.json", "w") as file:
#             file.write(json.dumps(perm_list, ensure_ascii = False, indent=4))

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
    perm_list = updatePERM(subjectReferences[i])
    if perm_list != []:
        with open("update_claremontcourses_new.json", "w") as file:
            file.write(json.dumps(perm_list, ensure_ascii = False, indent=4))
driver.quit()