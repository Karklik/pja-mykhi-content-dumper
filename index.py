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
SIZE_ONLY = '-S' in SUBJECT_ARGS
if SIZE_ONLY:
    SUBJECT_ARGS.remove('-S')
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

# Convert display size of files to bytes
def to_bytes(value):
    value = value.strip()
    last_character = value[-1:]
    exit_value = 0.0
    if last_character.isnumeric():
        exit_value = float(value)
    elif last_character == 'K':
        exit_value = float(value[:-1]) * 1024
    elif last_character == 'M':
        exit_value = float(value[:-1]) * 1024 * 1024
    elif last_character == 'G':
        exit_value = float(value[:-1]) * 1024 * 1024 * 1024
    return exit_value

# Converts bytes number to more readable form
def format_bytes(size):
    # 2**10 = 1024
    power = 2**10
    n = 0
    power_labels = {0 : '', 1: 'kilo', 2: 'mega', 3: 'giga', 4: 'tera'}
    while size > power:
        size /= power
        n += 1
    return size, power_labels[n] + 'bytes'

# Calculated estiamted total sized for found files
def getFilesEstimatedSize(url_path):
    total_size = 0.0
    page = requests.get(url_path)
    tree = html.fromstring(page.content)
    subject_items = tree.xpath('//td/a/text()')
    try:
        subject_items.remove('Parent Directory')
    except:
        pass
    # directories
    subject_directories = list(filter(lambda x: x.endswith('/'), subject_items))
    try:
        subject_directories.remove('0sem/')
    except:
        pass
    try:
        subject_directories.remove('rec/')
    except:
        pass
    for subject_directory in subject_directories:
        total_size += getFilesEstimatedSize(url_path + subject_directory)
    # files
    subject_files = list(filter(lambda x: not x.endswith('/'), subject_items))
    for subject_file in subject_files:
        subject_file_size = tree.xpath('//td/a[normalize-space(text())="' + subject_file + '"]/../../td[contains(concat(" ", normalize-space(@class), " "), "indexcolsize")]/text()')
        total_size += to_bytes(subject_file_size[0])
    # print(url_path + ' estimated total size: ' + str(format_bytes(total_size)))
    return total_size

if SIZE_ONLY:
    for subject in SUBJECT_PATHS.keys():
        print(subject + ' estimated total size: ' + str(format_bytes(getFilesEstimatedSize(SUBJECT_PATHS[subject]))))
    exit()

# Remove workspace directory
try:
    path = 'dump/'
    if os.path.exists(path) and os.path.isdir(path):
        shutil.rmtree(path)
except OSError:
    pass

# Create directories and files for found subjects
def getFiles(dir_path, url_path):
    total_size = 0.0
    try:
        os.makedirs(dir_path)
    except OSError:
        pass
        
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
        total_size += getFiles(dir_path + subject_directory, url_path + subject_directory)
    # files
    subject_files = list(filter(lambda x: not x.endswith('/'), subject_items))
    for subject_file in subject_files:
        file_path = dir_path + subject_file
        r = requests.get(url_path + subject_file)
        total_size += len(r.content)
        with open(file_path, 'wb') as f:
            f.write(r.content)
    return total_size

for subject in SUBJECT_PATHS.keys():
    print(subject + ' dumped total size: ' + str(format_bytes(getFiles('dump/' + subject + '/', SUBJECT_PATHS[subject]))))
