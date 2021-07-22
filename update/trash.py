import sqlite3
import json
import re

con = sqlite3.connect("claremontcourses.db", check_same_thread=False)
con.row_factory = sqlite3.Row

select = '''
    SELECT id, concurrent, concurrent_id FROM temp_claremontcourses WHERE concurrent == "None" AND concurrent_id != "";
'''
find = '''
    SELECT id FROM temp_claremontcourses WHERE code=?;
'''
update = '''
    UPDATE temp_claremontcourses SET concurrent_id = ? WHERE id=?;
'''
cur = con.cursor()
selects = cur.execute(select)
con.commit()

for select in selects:
    i = select[0]
    c = select[1]
    cid = select[2]
    print(i, " ", c, " ", cid)