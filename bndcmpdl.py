#!/usr/bin/python3

'''
TODO:
- ajouter l'année au dossier
- ajouter les idtags mp3
- gros cleanup
'''

from urllib.request import urlopen
from typing import List


import sys
import os
import re
import json
import urllib.request

class Album:
    artist = ""
    title = ""
    track_nb = 0
    tracks_title = []
    tracks_url = []
    trackinfo = []

def get_htmlsrc(url: str) -> List[str]:
    with urlopen(url) as fp:
        url_bytes = fp.read()
        return url_bytes.decode("utf8").splitlines()
    
def get_albuminfo_from_json(htmlsrc):
    for l in htmlsrc:
        if re.search("^\s+artist:", l):
            Album.artist = json.loads(l[12:-1])
        if re.search("^\s+album_title:", l):
            Album.title = json.loads(l[17:-1])
        if re.search("^\s+trackinfo:", l):
            Album.trackinfo = json.loads(l[15:-1])
        Album.track_nb = len(Album.trackinfo)
        for t in Album.trackinfo:
            t['title'] = get_sane_filename(t['title'])
            Album.tracks_title.append(t['title'])
            Album.tracks_url.append(t['file']['mp3-128'])
    
def get_sane_filename(s): # get rid of forbidden characters
    s = s.replace("/", "-")
    s = s.replace("*", "-")
    s = s.replace("?", "")
    s = s.replace("!", "")
    return s

if __name__ == "__main__":
    src = get_htmlsrc(sys.argv[1])
    get_albuminfo_from_json(src)

    dirname = Album.artist + " - " + Album.title
    dirname = get_sane_filename(dirname)
    os.mkdir(dirname)

    for i in range(Album.track_nb):
        with urlopen(Album.tracks_url[i]) as trk:
            nfname = dirname + "/" + str(i+1).zfill(2) + " - " + Album.tracks_title[i] + ".mp3"
            print(nfname)
            newfile = open(nfname, 'wb')
            newfile.write(trk.read())
            newfile.close()
