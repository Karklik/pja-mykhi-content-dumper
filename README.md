# pja-mykhi-content-dumper
This short python script helps with content dumping of https://pja.mykhi.org/ for specific subjects

## Requirments
- `python --version`
  > Python 3.8.1
- `pip install lxml --user`
- `pip install requests --user`

## Usage
All school subjects should be given as argument list with space seperator. Subject name must be same as display name of directory in pja.mykhi.org 

### Dump mode (Defaul)
All sbuject subdirectories and files will be dumped to relative directory `dump/`

```
py index.py SUBJECT1 SUBJECT2 ...
```

For example:
```
$ py index.py TAK "PJC_2018 zaoczne" BSI
Found: {'TAK': 'https://pja.mykhi.org/0sem/TAK/', 'PJC_2018 zaoczne': 'https://pja.mykhi.org/0sem/PJC_2018 zaoczne/', 'BSI': 'https://pja.mykhi.org/0sem/BSI/'}
TAK dumped total size: (28.810507774353027, 'megabytes')
PJC_2018 zaoczne dumped total size: (137.560546875, 'kilobytes')
BSI dumped total size: (241.01168251037598, 'megabytes')
```

### Estimate total size only
To calculate estimated total size of subject just add `-s` argument
```
py index.py SUBJECT1 SUBJECT2 ... -s
```

For example:
```
$ py index.py TAK "PJC_2018 zaoczne" BSI -s
Found: {'TAK': 'https://pja.mykhi.org/0sem/TAK/', 'PJC_2018 zaoczne': 'https://pja.mykhi.org/0sem/PJC_2018 zaoczne/', 'BSI': 'https://pja.mykhi.org/0sem/BSI/'}
TAK estimated total size: (28.9505859375, 'megabytes')
PJC_2018 zaoczne estimated total size: (138.0, 'kilobytes')
BSI estimated total size: (240.81152114868163, 'megabytes')
```