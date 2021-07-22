import json
import re
import sqlite3

f = open("update/update_claremontcourses_test.json")
q = open("update/newCourses.json")

con = sqlite3.connect("claremontcourses.db", check_same_thread=False)
con.row_factory = sqlite3.Row

find = """
    SELECT id, leadto, concurrent FROM temp_claremontcourses WHERE code=?;
"""

update_leadto = """
    UPDATE temp_claremontcourses SET leadto = ? WHERE id=?;
"""

update = """
    UPDATE temp_claremontcourses SET concurrent = ? WHERE id=?;
"""

ref = json.load(f)

loops = json.load(q)

for loop in loops:
    print(loop)


        