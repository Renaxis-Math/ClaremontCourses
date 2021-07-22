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


f = open("update/update_claremontcourses_test.json")
q = open("update/newCourses.json")

ref = json.load(f)
loops = json.load(q)

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


regex = r'[0-9]+[A-Z]+'


con = sqlite3.connect("claremontcourses.db", check_same_thread=False)
con.row_factory = sqlite3.Row

find = """
    SELECT id, leadto, concurrent FROM temp_claremontcourses WHERE code=?;
"""

inp = """
    INSERT INTO temp_claremontcourses
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
"""

 #[id, code, college, major, title, description, link, syllabus, equivalent, leadto, fulfillRequirements, term, perm, prereq, prereq_id, corequisite, corequisite_id, concurrent, concurrent_id]

id_start = 3954
for loop in loops:
    static_attributes = []
    for key, value in loop.items():
        keyword_major = re.sub(regex, "", key)
        value["major"] = majors[keyword_major]
        value["fulfillRequirements"] = listToString(value["fulfillRequirements"])
        if value["perm"] != "":
            value["perm"] = value["perm"][0]
            value["perm"] = listToString(value["perm"])
        static_attributes += [id_start, key]
        for subvalue in value.values():
            static_attributes += [subvalue]
    id_start += 1
    cur = con.cursor()
    cur.execute(inp, tuple(static_attributes))
    con.commit()    


        