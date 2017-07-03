#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import urllib
from PIL import Image


def load_photo(url):
    file, mime = urllib.urlretrieve(url)
    photo = Image.open(file)
    return photo

def readLines(file_path):
    with open(file_path, 'r') as T:
        lines = T.readlines()
    return lines

def download(filelist, save_path):
    if not os.path.exists(save_path):
        os.mkdir(save_path)
    lines = readLines(filelist)
    index = 0
    for line in lines:
        index += 1
        photo = load_photo(line)
        photo.save(save_path+"%5d.png"%index)
        print "processed %d"%index
    print "down!"


if __name__ == '__main__':
    download("1.txt", "tmp/")
