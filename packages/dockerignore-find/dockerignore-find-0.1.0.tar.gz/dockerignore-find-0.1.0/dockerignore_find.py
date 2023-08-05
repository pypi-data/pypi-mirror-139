#!/bin/env python
import os
import re
import fnmatch

def read_dockerignore(path):
    """ returns a regex to exclude and a regex to include """
    excludes = []
    includes = []
    try:
        with open(os.path.join(path,'.dockerignore'),'r') as dockerignore:
            for line in dockerignore:
                if line.startswith('#'): # ignore
                    continue
                elif line.startswith('!'): # is an exception from an exclude
                    pattern = fnmatch.translate(line[1:].strip())
                    includes.append(f'({pattern})')
                else:
                    pattern = fnmatch.translate(line.strip())
                    excludes.append(f'({pattern})')
    except FileNotFoundError:
        pass
    
    if excludes:
        exclude = re.compile('|'.join(excludes))
    else:
        exclude = re.compile('$^') # shouldn't match anything
    if includes:
        include = re.compile('|'.join(includes))
    else:
        include = re.compile('$^') # shouldn't match anything
    return exclude, include 

def main():
    exclude, include = read_dockerignore('.')
    for path in find_with_dockerignore('.',exclude,include):
        print(path)

def find_with_dockerignore(path,exclude,include):
    for entry in os.scandir(path):
        if exclude.match(entry.path) and not include.match(entry.path):
            continue
        elif entry.is_dir():
            yield from find_with_dockerignore(entry.path,exclude,include)
        else:
            yield entry.path

if '__main__' == __name__:
    main()
