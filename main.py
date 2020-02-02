from pja_mykhi_service import PjaMykhiService
from custom_utils import to_bytes
from custom_utils import format_bytes
from lxml import html
import os
import shutil
import sys

base_url = 'https://pja.mykhi.org/'
semesters = ['0sem/', 'mgr/1sem/', 'mgr/2sem/', 'mgr/3sem/', 'mgr/blokowe/']
subject_args = [x.upper() for x in sys.argv] 
subject_args.pop(0)
size_only = '-S' in subject_args
all_subjects = '-A' in subject_args
if size_only:
    subject_args.remove('-S')
pm_service = PjaMykhiService()

# Validation of program arguemnts
if not all_subjects and len(subject_args) == 0:
    print('No subjects provided')
    exit()

# Gather links to subjects
subject_paths = {}
if all_subjects:
    subject_paths = pm_service.get_subject_paths()
else:
    subject_paths = pm_service.get_subject_paths(subject_args)
    
# Validation of links to subjects
if len(subject_paths) == 0:
    print('No subjects found')
    exit()
elif all_subjects:
    print(f'Found {len(subject_paths)} subjects')
else:
    print(f'Found {len(subject_paths)} of {len(subject_args)} subjects')

# Calculating estimated total size
if size_only:
    total_size = 0.0
    for key in subject_paths:
        subject_total_size = pm_service.count_estimated_bytes(subject_paths[key])
        total_size += subject_total_size
        print(f'{key} estimated total size {str(format_bytes(subject_total_size))} of files') 
    print(f'Estimated total size: {str(format_bytes(total_size))}')
    exit()

# Remove relative workspace directory
try:
    path = 'dump/'
    if os.path.exists(path) and os.path.isdir(path):
        shutil.rmtree(path)
except OSError:
    pass

# Dumping subjects
total_size = 0.0
for key in subject_paths:
    dir_path = 'dump/' + key + '/'
    subject_total_size = pm_service.get_files(dir_path, subject_paths[key])
    print(f'{key} dumped total size {str(format_bytes(subject_total_size))} of files to {dir_path}') 
    total_size += subject_total_size
print(f'Dumped total size: {str(format_bytes(total_size))}')