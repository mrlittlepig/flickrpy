#!/usr/bin/env python

import os

def get_file_list(src_dir):
    file_list = []
    for filename in os.listdir(src_dir):
        if not filename.split('.')[-1] == 'txt':
            continue
        file_list.append(filename)
        # print(filename)
    return file_list

def readLines(file_path):
    with open(file_path, 'r') as T:
        lines = T.readlines()
    return lines

dir = "data/"

file_list = get_file_list(dir)
count = 0
tmp = []
for fe in file_list:
    lines = readLines(dir+fe)
    for line in lines:
        if len(line) <= 1:
            continue
        count += 1
        tmp.append(('%05d.jpg ' % count) + line.split(' ')[-1])
        #print tmp

file('filelist.txt', "w").writelines(tmp)