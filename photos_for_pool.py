#!/usr/bin/python
"""Usage: python photos_for_pool.py [OPTIONS] group_id
group_id must the flickr NSID for a group

OPTIONS:
  -v or --verbose
  -e or --equal : width and height of photo must be the same
  -s size or --size size : size of photo Thumbnail, Small,
                           Medium, Large, Original
  -n number or --number number : the number of photos to retrieve

"""


__author__ = "James Clarke <james@jamesclarke.info>"
__version__ = "$Rev$"
__date__ = "$Date$"
__copyright__ = "Copyright 2004-5 James Clarke"

import sys
import urllib
import flickr
import os

verbose = False

def getURL(photo, size, equal=False):
    """Retrieves a url for the photo.  (flickr.photos.getSizes)
    
    photo - the photo
    size - what size 'Thumbnail, Small, Medium, Large, Original'
    equal - should width == height?
    """
    method = 'flickr.photos.getSizes'
    data = flickr._doget(method, photo_id=photo.id)
    for psize in data.rsp.sizes.size:
        if psize.label == size:
            if equal and psize.width == psize.height:
                return psize.source
            elif not equal:
                return psize.source
    raise flickr.FlickrError, "No URL found"

def getPhotoURLs(groupid, size, number, equal=False):
    group = flickr.Group(groupid)
    photos = group.getPhotos(per_page=number)
    urls = []
    for photo in photos:
        try:
            urls.append(getURL(photo, size, equal))
        except flickr.FlickrError:
            if verbose:
                print "%s has no URL for %s" % (photo, size)
    return urls
    

def main(group, max_num, save_path):
    from getopt import getopt, GetoptError

    size = 'Large'
    equal = False
    number = max_num


    if len(group) == 0:
        print "You must specify a group"
        print __doc__
        return 1
    
    groupid = group
    
    urls = getPhotoURLs(groupid, size, number, equal)

    count = 0
    tmp = []
    for url in urls:
        count += 1
        tmp.append(url + '\n')
    file(save_path, "w").writelines(tmp)
        
if __name__ == '__main__':
    if not os.path.exists('data'):
        os.mkdir('data')
    max_count = 600
    group_id = ["1089961@N20","722210@N24","13078277@N00","80263920@N00","1408220@N24"]
    for group in group_id:
        main(group, max_count, "data/"+group+".txt")
