import os
import requests
import shutil
import sys
import traceback
from lxml import html
MAIN_URL = 'https://pja.mykhi.org/'
SEMESTERS = ['0sem/', 'mgr/1sem/', 'mgr/2sem/', 'mgr/3sem/', 'mgr/blokowe/']
SUBJECT_ARGS = [x.upper() for x in sys.argv] 
SUBJECT_ARGS.pop(0)
SUBJECT_PATHS = {}

# Validation of program arguemnts
if len(SUBJECT_ARGS) == 0:
    print('No subjects provided')
    exit()

# Gather links to subjects
for semester in SEMESTERS:
    page = requests.get(MAIN_URL + semester)
    tree = html.fromstring(page.content)
    semesterSubjects = tree.xpath('//td/a/text()')
    try:
        semesterSubjects.remove('Parent Directory')
    except:
        pass

    for subject in SUBJECT_ARGS:
        for i in range(len(semesterSubjects)):
            if subject + '/' == semesterSubjects[i].upper():
                SUBJECT_PATHS[semesterSubjects[i].strip("/")] = MAIN_URL + semester + semesterSubjects[i]
                continue
print('Found: ' + str(SUBJECT_PATHS))

# Validation of links to subjects
if len(SUBJECT_PATHS) == 0:
    print('No subjects found')
    exit()

# Remove workspace directory
try:
    path = 'dump/'
    if os.path.exists(path) and os.path.isdir(path):
        print ('Deleting directory: ' + path)
        shutil.rmtree(path)
except OSError:
    print ("Deletion of the directory %s failed" % path)
else:
    print ("Successfully deleted the directory %s" % path)

# Create directories and files for found subjects
def getFiles(dir_path, url_path):
    try:
        print ('Creating directory: ' + dir_path)
        os.makedirs(dir_path)
    except OSError:
        print ("Creation of the directory %s failed" % dir_path)
    else:
        print ("Successfully created the directory %s " % dir_path)
        
    page = requests.get(url_path)
    tree = html.fromstring(page.content)
    subject_items = tree.xpath('//td/a/text()')
    try:
        subject_items.remove('Parent Directory')
    except:
        pass
    # directories
    subject_directories = list(filter(lambda x: x.endswith('/'), subject_items))
    for subject_directory in subject_directories:
        getFiles(dir_path + subject_directory, url_path + subject_directory)
    # files
    subject_files = list(filter(lambda x: not x.endswith('/'), subject_items))
    for subject_file in subject_files:
        file_path = dir_path + subject_file
        print ('Creating file: ' + file_path)
        r = requests.get(url_path + subject_file)
        with open(file_path, 'wb') as f:
            f.write(r.content)
    return

for subject in SUBJECT_PATHS.keys():
    getFiles('dump/' + subject + '/', SUBJECT_PATHS[subject])