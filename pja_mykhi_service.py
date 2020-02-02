from custom_utils import to_bytes
from custom_utils import format_bytes
from lxml import html
import os
import requests
class PjaMykhiService:
    __BASE_URL__ = 'https://pja.mykhi.org/'
    __SEMESTERS__ = ['0sem/', 'mgr/1sem/', 'mgr/2sem/', 'mgr/3sem/', 'mgr/blokowe/']
    __RESTRICTED_DIRS__ = ['Parent Directory', '0sem/']
    __FORBIDDEN_FILE_CHARS__ = ['\\', '/', ':', '*', '?', '"', '<', '>', '|']


    def get_subject_paths(self, subjects = None):
        subject_paths = {}
        for semester in PjaMykhiService.__SEMESTERS__:
            page = requests.get(PjaMykhiService.__BASE_URL__ + semester)
            tree = html.fromstring(page.content)
            semesterSubjects = tree.xpath('//td/a/text()')
            
            for rd in PjaMykhiService.__RESTRICTED_DIRS__:
                try:
                    semesterSubjects.remove(rd)
                    if rd != 'Parent Directory':
                        print(f'WARN : get_subject_paths : skipped directory {rd} in {PjaMykhiService.__BASE_URL__}{semester}{rd}')
                except:
                    pass

            if subjects is not None:
                for subject in subjects:
                    for i in range(len(semesterSubjects)):
                        if subject + '/' == semesterSubjects[i].upper():
                            url = PjaMykhiService.__BASE_URL__ + semester + semesterSubjects[i]
                            subject_paths[semesterSubjects[i].strip("/")] = url
                            continue
            else:
                for i in range(len(semesterSubjects)):
                    url = PjaMykhiService.__BASE_URL__ + semester + semesterSubjects[i]
                    subject_paths[semesterSubjects[i].strip("/")] = url
        return subject_paths

    def count_estimated_bytes(self, url_path):
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

        if '0sem/' in subject_directories:
            print(f'WARN : count_estimated_bytes : Leaving directory {url_path} due possible infinite recursion')
            return total_size

        for rd in PjaMykhiService.__RESTRICTED_DIRS__:
            try:
                subject_directories.remove(rd)
                if rd != 'Parent Directory':
                    print(f'WARN : count_estimated_bytes : skipped directory {rd} in {url_path}{rd}')
            except:
                pass

        for subject_directory in subject_directories:
            total_size += self.count_estimated_bytes(url_path + subject_directory)
        # files
        subject_files = list(filter(lambda x: not x.endswith('/'), subject_items))
        for subject_file in subject_files:
            subject_file_size = tree.xpath('//td/a[text()="' + subject_file.strip() + '"]/../../td[contains(concat(" ", normalize-space(@class), " "), "indexcolsize")]/text()')
            total_size += to_bytes(subject_file_size[0])
        return total_size

    def get_files(self, dir_path, url_path):
        total_size = 0.0
        try:
            os.makedirs(dir_path)
        except OSError:
            pass
            
        page = requests.get(url_path)
        tree = html.fromstring(page.content)
        subject_items = tree.xpath('//td/a/text()')

        if '0sem/' in subject_items:
            print(f'WARN : get_files : Leaving directory {url_path} due possible infinite recursion')
            return total_size

        for rd in PjaMykhiService.__RESTRICTED_DIRS__:
            try:
                subject_items.remove(rd)
                if rd != 'Parent Directory':
                    print(f'WARN : get_files : skipped directory {rd} in {url_path}{rd}')
            except:
                pass

        # directories
        subject_directories = list(filter(lambda x: x.endswith('/'), subject_items))
        for subject_directory in subject_directories:
            total_size += self.get_files(dir_path + subject_directory, url_path + subject_directory)

        # files
        subject_files = list(filter(lambda x: not x.endswith('/'), subject_items))
        for subject_file in subject_files:
            r = requests.get(url_path + subject_file)

            # Replacing illegal chars before safe 
            for c in PjaMykhiService.__FORBIDDEN_FILE_CHARS__:
                if c in subject_file:
                    subject_file = subject_file.replace(c, '%%')

            file_path = dir_path + subject_file
            with open(file_path, 'wb') as f:
                f.write(r.content)
            total_size += len(r.content)

        return total_size
