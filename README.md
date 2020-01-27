# pja-mykhi-content-dumper
This short python script helps with content dumping of https://pja.mykhi.org/ for specific subjects

## Requirments
- `python --version`
  > Python 3.8.1
- `pip install lxml --user`
- `pip install requests --user`

## Usage
All school subjects should be given as argument list with space seperator. Subject name must be same as display name of directory in pja.mykhi.org 

```
py index.py SUBJECT1 SUBJECT2 ...
```

For example:
```
py index.py TAK "PJC_2018 zaoczne" BSI
```
