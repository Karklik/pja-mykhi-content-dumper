# pja-mykhi-content-dumper
This short python script helps with content dumping of https://pja.mykhi.org/ for specific subjects

## Requirments
- `python --version`
  > Python 3.8.1
- `pip install lxml --user`
- `pip install requests --user`

## Usage
If you want to use program for all subjects in args add `-a`, otherwise in args add subject names as list with space seperator. Subject name must be same as display name of directory in pja.mykhi.org 

### Dump mode (Default)
All sbuject subdirectories and files will be dumped to relative directory `dump/`

For all subjects:
```
py main.py -a
```

For selected subjects:
```
py main.py SUBJECT1 SUBJECT2 ...
```

For example:
```
$ py main.py TAK "PJC_2018 zaoczne" BSI
Found: 3 of 3 subjects
TAK dumped total size: (28.810507774353027, 'megabytes')
PJC_2018 zaoczne dumped total size: (137.560546875, 'kilobytes')
BSI dumped total size: (241.01168251037598, 'megabytes')
```

### Estimate total size mode
To calculate estimated total size of subject just add `-s` argument

For all subjects:
```
py main.py -a -s
```

For selected subjects:
```
py main.py SUBJECT1 SUBJECT2 ... -s
```

For example:
```
$ py main.py TAK "PJC_2018 zaoczne" BSI -s
Found: 3 of 3 subjects
TAK estimated total size: (28.9505859375, 'megabytes')
PJC_2018 zaoczne estimated total size: (138.0, 'kilobytes')
BSI estimated total size: (240.81152114868163, 'megabytes')
```
