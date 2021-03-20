from __future__ import print_function
import sqlite3
import convert_prereq
import convert_coreq
import random
import json
import math
import re
import ast 
import random
import time
import gzip
import shutil
from random import randint
from datetime import datetime
from bs4 import BeautifulSoup
from flask import Flask, render_template, send_from_directory, request, make_response, flash, redirect, url_for
from werkzeug.utils import secure_filename
import pickle
import os.path
import os
from google_auth_oauthlib.flow import Flow, InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
from google.auth.transport.requests import Request
from googleapiclient.http import MediaFileUpload
import google.oauth2.credentials
import google_auth_oauthlib.flow

def Create_Service(client_secret_file, api_name, api_version, *scopes):
    CLIENT_SECRET_FILE = client_secret_file
    API_SERVICE_NAME = api_name
    API_VERSION = api_version
    SCOPES = [scope for scope in scopes[0]]

    cred = None
    pickle_file = f'token_{API_SERVICE_NAME}_{API_VERSION}.pickle'

    if os.path.exists(pickle_file):
        with open(pickle_file, 'rb') as token:
            cred = pickle.load(token)

    if not cred or not cred.valid:
        if cred and cred.expired and cred.refresh_token:
            cred.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                CLIENT_SECRET_FILE, SCOPES)
            cred = flow.run_local_server()

        with open(pickle_file, 'wb') as token:
            pickle.dump(cred, token)
    service = build(API_SERVICE_NAME, API_VERSION, credentials=cred)
    try:
        service = build(API_SERVICE_NAME, API_VERSION, credentials=cred)
        return service
    except:
        return None
def convert_to_RFC_datetime(year=1900, month=1, day=1, hour=0, minute=0):
    dt = datetime.datetime(year, month, day, hour, minute, 0).isoformat() + 'Z'
    return dt


app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'docx', 'doc'}
CLIENT_SECRET_FILE = 'credentials.json'
API_NAME = 'drive'
API_VERSION = 'v3'
SCOPES = ['https://www.googleapis.com/auth/drive']

mime_types = ['application/pdf']
SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
# course_url = os.path.join(SITE_ROOT, "static/data", "claremontcourses.json")
term1_url = os.path.join(SITE_ROOT, "static/data", "term1.txt.gz")
term2_url = os.path.join(SITE_ROOT, "static/data", "term2.txt.gz")
terms_url = os.path.join(SITE_ROOT, "static/data", "terms.txt.gz")
syllabus_url = os.path.join(SITE_ROOT, "static/data", "official_syllabus.json.gz")
requirements_url = os.path.join(SITE_ROOT, "static/data", "official_requirements.txt.gz")



academicyear = "2020/2021"
season = "Spring"
with gzip.open(term1_url, 'rb') as f:
    data = f.read().decode('ascii')
    term1 = list(ast.literal_eval(data))
with gzip.open(term2_url, 'rb') as f:
    data = f.read().decode('ascii')
    term2 = list(ast.literal_eval(data))
with gzip.open(terms_url, 'rb') as f:
    data = f.read().decode('ascii')
    terms = list(ast.literal_eval(data))
with gzip.open(requirements_url, 'rb') as f:
    data = f.read().decode('ascii')
    requirements = list(ast.literal_eval(data))

con = sqlite3.connect("claremontcourses.db", check_same_thread=False)
con.row_factory = sqlite3.Row

converted_prereqs = convert_prereq.main()
converted_coreqs = convert_coreq.main()

def querytoList(queries):
    result = list()
    for query in queries:
        result.append(query[0])
    return result

def intersection(lst):
    if len(lst) == 2:
        return list(set(lst[0]) & set(lst[1]))
    elif len(lst) == 1:
        return lst[0]
    return list(set(lst[0]) & set(intersection(lst[1:])))

def activateJson(courses):
    size = len(courses)
    for j in range(size):
        course = courses[j]
        for key in course.keys():
            if key == 'prereq_id':
                course[key] = converted_prereqs[course['id']]
                str_value = str(course[key])
                regex = r"[0-9]+"
                numbers = re.findall(regex, str_value)
                length = len(numbers)
                if length > 0:
                # Convert to code
                    for i in range(length):
                        number = numbers[i]
                        int_number = int(number)
                        select = '''
                            SELECT code FROM temp_claremontcourses
                            WHERE id=?;
                        '''
                        cur = con.cursor()
                        select_prereqs = cur.execute(select, (int_number,))
                        for select_prereq in select_prereqs:
                            str_value = str_value.replace(numbers[i],select_prereq[0])
                            try:
                                course[key] = ast.literal_eval(str_value)
                            except:
                                course[key] = str_value
                    con.commit()
                else:
                    course[key] = ""
            elif key == 'corequisite_id':
                course[key] = converted_coreqs[course['id']]
                str_value = str(course[key])
                regex = r"[0-9]+"
                numbers = re.findall(regex, str_value)
                length = len(numbers)
                if length > 0:
                # Convert to code
                    for i in range(length):
                        number = numbers[i]
                        int_number = int(number)
                        select = '''
                            SELECT code FROM temp_claremontcourses
                            WHERE id=?;
                        '''
                        cur = con.cursor()
                        select_corequisites = cur.execute(select, (int_number,))
                        for select_corequisite in select_corequisites:
                            str_value = str_value.replace(numbers[i],select_corequisite[0])
                            try:
                                course[key] = ast.literal_eval(str_value)
                            except:
                                course[key] = str_value
                    con.commit()
                else:
                    course[key] = ""
            elif key == 'concurrent_id':
                str_value = str(course[key])
                regex = r"[0-9]+"
                numbers = re.findall(regex, str_value)
                length = len(numbers)
                if length > 0:
                    for i in range(length):
                        number = numbers[i]
                        int_number = int(number)
                        cur = con.cursor()
                        select = '''
                            SELECT code FROM temp_claremontcourses
                            WHERE id=?;
                        '''
                        select_others = cur.execute(select, (int_number,))
                        con.commit()
                        for select_other in select_others:
                            str_value = str_value.replace(numbers[i],select_other[0])
                            course[key] = str_value  
            elif key in ['equivalent', 'leadto', 'fulfillRequirements', 'term', 'perm']:
                course[key] = course[key].split('; ')
                if course[key][0] == '':
                    if key == 'fulfillRequirements':
                        course[key] = ""
                    else:
                        course[key] = ["None"]
        courses[j] = course
    return courses

def totalLength():
    cur = con.cursor()
    cur.execute("SELECT COUNT(id) FROM temp_claremontcourses;")
    con.commit()
    total = querytoList(cur.fetchall())
    return total[0]

def generateMajorSet():
    cur = con.cursor()
    cur.execute("SELECT DISTINCT major FROM temp_claremontcourses;")
    con.commit()
    majors = querytoList(cur.fetchall())
    return sorted(majors)

def getAll():
    cur = con.cursor()
    sql = "SELECT code, term from temp_claremontcourses;"
    cur.execute(sql)
    con.commit()
    rows = cur.fetchall()
    courses = list()
    for course in rows:
        course = dict(course)
        courses.append(course)

    return activateJson(courses)

def getCourses(idTuple):
    cur = con.cursor()
    length = len(idTuple)
    sql = "SELECT * from temp_claremontcourses WHERE id IN (" + "?" + ",?"*(length-1) + ");"
    cur.execute(sql, idTuple)
    con.commit()
    rows = cur.fetchall()
    courses = list()
    for course in rows:
        course = dict(course)
        courses.append(course)
    return courses

def markText(texts, original):
    for text in texts:
        founds = re.findall(text, original, re.IGNORECASE)
        for found in founds:
            original = original.replace(found, "<mark>" + found + "</mark>")
    return original

@app.route('/')
def root():
    count = 0
    numberofcourses = 60
    previous = True
    notlast = True

    if request.args.get('page'):
        pagenumber = int(request.args.get('page'))
    else:
        pagenumber = 1
    if pagenumber == 1:
        previous = False

    totalList = list()
    i = ""
    permclicked = False
    collegeclickeds = []
    majorclickeds = []
    prereqclickeds = []
    schoolclickeds = "All"
    concurrentclicked = False
    corequisiteclicked = False
    searches = [""]
    search = ""
    semesterclicked = False
    genedclickeds = []
    filterPERM = []
    filterCourses = [] 
    filterColleges = []
    filterMajors = []
    filterPreReqs = []
    filterSchools = []
    filterConcurrents = []
    filterCorequisites = []
    filterSemester = []
    filterGeneds = []
    count_special = 0

# Search
    if request.args.get('search'):   
        # filterCourses
        filterCourses = list()
        count += 1
        count_special += 1
        search = request.args.get('search').replace("%20", " ")
        subsearch = search.lower()
        subsearch = re.sub(' +', ' ', search)
        search_regex = '\"(.*?)\"'
        searches = re.findall(search_regex, subsearch)
        query_start = "SELECT id FROM temp_claremontcourses WHERE"
        if len(searches) > 0:
            length = len(searches)
            sql = ''
            for i in range(length):
                search_i = searches[i]
                if i > 0:
                    sql += " AND"
                sql += " (code LIKE '%" + search_i + "%'" + " OR title LIKE '%" + search_i + "%'" + " OR description LIKE '%" + search_i + "%'" + " OR major LIKE '%" + search_i + "%'" + " OR college LIKE '%" + search_i + "%')"
            cur = con.cursor()
            cur.execute(query_start + sql)
            con.commit()
            filterCourses += querytoList(cur.fetchall())

        for mustSearch in searches:
            subsearch = subsearch.replace('"' + mustSearch + '"', "").strip()
        
        if subsearch != "":
            cur = con.cursor()
            query = "'%" + subsearch + "%'"
            sub_sql = query_start + " code LIKE ? OR title LIKE ? OR description LIKE ? OR major LIKE ? OR college LIKE ?"
            cur.execute(sub_sql, (query, query, query, query, query))
            filterCourses += querytoList(cur.fetchall())
            searches += subsearch.split()
            if len(filterCourses) == 0:
                length = len(searches)
                sql = ''
                for i in range(length):
                    search_i = searches[i]
                    if i > 0:
                        sql += " OR"
                    sql += " (code LIKE '%" + search_i + "%'" + " OR title LIKE '%" + search_i + "%'" + " OR description LIKE '%" + search_i + "%'" + " OR major LIKE '%" + search_i + "%'" + " OR college LIKE '%" + search_i + "%')"
                cur.execute(query_start + sql)
                con.commit()
                filterCourses += querytoList(cur.fetchall())
        # print(searches)
        totalList.append(filterCourses)
# \Search

# Perm
    if request.args.get('perm'):
        # filterPERM
        count += 1
        permclicked = request.args.get('perm')
        cur = con.cursor()
        if permclicked == 'no':     
            cur.execute("SELECT id FROM temp_claremontcourses WHERE perm != '';")               
        if permclicked == "yes":
            cur.execute("SELECT id FROM temp_claremontcourses WHERE perm == '';")
        con.commit()
        filterPERM = querytoList(cur.fetchall())
        totalList.append(filterPERM)
# \Perm
# Concurrent
    if request.args.get('concurrent'):
        # filterConcurrents
        count += 1
        concurrentclicked = request.args.get('concurrent')
        cur = con.cursor()
        if concurrentclicked == 'yes':
            cur.execute("SELECT id FROM temp_claremontcourses WHERE concurrent_id != '';")
        if concurrentclicked == "no":
            cur.execute("SELECT id FROM temp_claremontcourses WHERE concurrent_id == '';")
        con.commit()
        filterConcurrents = querytoList(cur.fetchall())
        totalList.append(filterConcurrents)
# \Concurrent
# Corequisite
    if request.args.get('corequisite'):
        # filterCorequisites
        count += 1
        corequisiteclicked = request.args.get('corequisite')
        cur = con.cursor()
        if corequisiteclicked == 'yes':
            cur.execute("SELECT id FROM temp_claremontcourses WHERE corequisite_id != '';")
        if corequisiteclicked == "no":
            cur.execute("SELECT id FROM temp_claremontcourses WHERE corequisite_id == '';")
        con.commit()
        filterCorequisites = querytoList(cur.fetchall())
        totalList.append(filterCorequisites)
# \Corequisite

# Equivalent
    colleges = [0, 1, 2, 3, 4, 5, 6]
    new_colleges = list()
    recognitions = {'mckenna': 'CM', 'pomona': 'PO', 'mudd': 'HM', 'pitzer': 'PZ', 'scripps': 'SC', 'keck':'KS', "none":"None"}
    for _ in colleges:
        if request.args.get('college[' + str(_) + "]"):
            count += 1
            college = request.args.get('college[' + str(_) + "]")
            new_colleges.append(recognitions[college])
            collegeclickeds.append(college.lower())
    query_start = "SELECT id FROM temp_claremontcourses WHERE"
    length = len(new_colleges)
    sql = ''
    for i in range(length):
        new_college = new_colleges[i]
        if i > 0:
            sql += " AND "
        sql += " (equivalent LIKE '%" + new_college + "' OR equivalent LIKE '%" + new_college + ";%')"
    if length > 0:
        cur = con.cursor()
        cur.execute(query_start + sql)
        con.commit()
        filterColleges = querytoList(cur.fetchall())
        totalList.append(filterColleges)
# \ Equivalent

# Major
    majors = generateMajorSet()
    subjects = [i for i in range(len(majors))]
    new_majors = list()
    filterMajors = list()
    for _ in subjects:
        s = str(_)
        if request.args.get("major" + s):
            count += 1
            subject = request.args.get("major"+s).replace("%20", " ")
            new_majors.append(subject)
            majorclickeds.append((subject,s))
    for new_major in new_majors:
        cur = con.cursor()
        cur.execute("SELECT id FROM temp_claremontcourses WHERE major == ?;", (new_major,))
        filterMajors += querytoList(cur.fetchall())
    con.commit()
    if len(new_majors) > 0:
        totalList.append(filterMajors)
# \Major
        
# Gened
    geneds = [i for i in range(len(requirements))]
    # filterGeneds
    new_geneds = []
    for _ in geneds:
        s = str(_)
        if request.args.get('gened' + s):
            count += 1
            gened = request.args.get('gened' + s).replace("%20", " ").replace("%27", "'")
            new_geneds.append(gened)
            genedclickeds.append((gened, s))
    filterGeneds = list()
    length = len(new_geneds)

    query_start = "SELECT id FROM temp_claremontcourses WHERE"
    sql = ''
    for i in range(length):
        new_gened = new_geneds[i]
        if new_gened == "SC Gender and Women's Studies GE":
            new_gened = "SC Gender and Women"  
        if i > 0:
            sql += " AND "
        sql += " (fulfillRequirements LIKE '%" + new_gened + "%')"
    if length > 0:
        cur = con.cursor()
        cur.execute(query_start + sql)
        filterGeneds += querytoList(cur.fetchall())
        con.commit()
        totalList.append(filterGeneds)
# \Gened

# Prereq
    noprereqs = ["0","1","2"]
    filterPreReqs = list()
    for noprereq in noprereqs:
        # filterPreReqs
        if request.args.get('noprereq' + noprereq):
            count += 1
            prereq_request = request.args.get('noprereq' + noprereq)
            i = int(prereq_request)
            cur = con.cursor()
            if i == 0:
                cur.execute("SELECT id FROM temp_claremontcourses WHERE prereq_id == '';")
            if i == 2:
                cur.execute("SELECT id FROM temp_claremontcourses WHERE prereq_id LIKE '%&%' AND NOT (prereq_id LIKE '%/%');")
            if i == 1:
                sql = "SELECT id FROM temp_claremontcourses WHERE NOT (prereq_id LIKE '%&%' AND NOT (prereq_id LIKE '%/%') OR prereq_id == '');"
                cur.execute(sql)
            filterPreReqs += querytoList(cur.fetchall())
            prereqclickeds.append(prereq_request)
    con.commit()
    if len(prereqclickeds) > 0:
        totalList.append(filterPreReqs)
# \Prereqr

# School
    if request.args.get('school'):
        # filterSchools
        count += 1
        school = request.args.get('school').replace("%20", " ").strip()
        query_school = school.split(' ')[-1]
        cur = con.cursor()
        cur.execute("SELECT id FROM temp_claremontcourses WHERE college == ?;", (query_school,))
        con.commit()
        filterSchools = querytoList(cur.fetchall())
        schoolclickeds = school
        totalList.append(filterSchools)
# \School

# Current Semester
    if request.args.get('semester'):
        # filterSemester
        count += 1
        semester = request.args.get('semester')
        cur = con.cursor()
        sql = "SELECT id FROM temp_claremontcourses WHERE term LIKE '%" + semester + "%';"
        cur.execute(sql)
        con.commit()
        filterSemester = querytoList(cur.fetchall())
        semesterclicked = semester
        totalList.append(filterSemester)
# \Current Semester
# Filters
    finalList = list()
    if count == 0 and count_special == 0:
        length = totalLength()
        sql = "SELECT * from temp_claremontcourses WHERE id BETWEEN ? AND ?;"
        cur = con.cursor()
        cur.execute(sql, (str(numberofcourses*(pagenumber-1) + 1), str(numberofcourses*pagenumber)))
        con.commit()
        rows = cur.fetchall()
        for course in rows:
            course = dict(course)
            finalList.append(course)
    else:
        # Filter the filters
        sortedList = intersection(totalList)
        if len(sortedList) > 0:
            finalList = getCourses(tuple(sortedList))
        else:
            finalList = []
        length = len(finalList)
        finalList = finalList[numberofcourses*(pagenumber-1):numberofcourses*pagenumber]

    finalList = activateJson(finalList)

    if count_special > 0:
        for course in finalList:
            course['code'] = markText(searches, course['code'])
            course['title'] = markText(searches, course['title'])
            course['description'] = markText(searches, course['description'])
            course['major'] = markText(searches, course['major'])

    if count_special == 0:
        random.seed()
        random.shuffle(finalList)

    # Execute
    n = int(pagenumber) + 1
    p = int(pagenumber) - 1
    if pagenumber == (length // numberofcourses) + 1:
        notlast = False       
    totalPages = (length // numberofcourses) + 1

    if 'darkmode' in request.cookies:
        cookies = "yes"
    else:
        cookies = "no"

    return render_template(
        'app.html', courses=finalList, cookies=cookies,
        count=length, pagenumber=pagenumber, previous=previous, Previous=p, notlast=notlast, schools=schoolclickeds,
        next=n, majors=majors, input=search, perm=permclicked, colleges=collegeclickeds, majorclickeds=majorclickeds,
        prereqs=prereqclickeds, concurrentclicked=concurrentclicked, corequisiteclicked=corequisiteclicked, searches=searches,
        terms=terms,term1=term1,term2=term2, totalPages=totalPages, semester=semesterclicked, academicyear=academicyear, 
        season=season, requirements=requirements, genedclickeds=genedclickeds
        )   

@app.route('/<code>')
def course(code):
    prereqs = "None"
    cur = con.cursor()
    cur.execute("SELECT * FROM temp_claremontcourses WHERE code=?;", (code,))
    con.commit()
    rows = cur.fetchall()
    course = None
    for row in rows:
        course = dict(row)
    course = activateJson([course])
    course = course[0]
    prereqs = course['prereq_id']
    courses = getAll()
    if 'darkmode' in request.cookies:
        cookies = "yes"
    else:
        cookies = "no"
    return render_template(
        'course.html', courses=courses, cookies=cookies, course=course, prereqs=prereqs, terms=terms, 
        academicyear=academicyear, season=season, code=code, term1=term1,term2=term2
    )


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/<code>/upload', methods=['GET', 'POST'])
def upload(code):
    if request.method == "POST":    
        with gzip.open(syllabus_url, "rb") as f:
            data = f.read()
            syllabus_link = json.loads(data.decode('utf-8'))
        UPLOAD_FOLDER = '/tmp'
        app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        uploaded_files = request.files.getlist("file")
        for file in uploaded_files:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            folder_id = syllabus_link[code]
            file_metadata = {
                'name': filename,
                'parents': [folder_id]
            }
            try:
                service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)
                location = UPLOAD_FOLDER + '/{0}'
                media = MediaFileUpload(location.format(filename), chunksize=3 * 1024 * 1024, mimetype=mime_types[0], resumable=True)
                time.sleep(2)
                service.files().create(
                    body=file_metadata,
                    media_body=media,
                    fields='id'
                ).execute()
                time.sleep(3)
            except:
                os.remove("token_drive_v3.pickle")
                os.system("pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib")
                pass
        message = "Upload Succesfully! Returning..."
        code = str(code)
        return render_template(
            'upload.html', message=message, code=code
        )

    return render_template(
        'upload.html', code=code
    )
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),'favicon.ico', mimetype='image/vnd.microsoft.icon')
  













