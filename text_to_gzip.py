import gzip
import shutil

names = ['term1.txt', 'term2.txt', 'terms.txt', 'official_syllabus.json', 'official_requirements.txt']
for name in names:
    input_text = 'C:/upload_claremontcourses/static/data/' + name
    with open(input_text, 'rb') as f_in:
        with gzip.open(input_text + '.gz', 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)