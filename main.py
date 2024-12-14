#!/usr/bin/env python

import os
import time
from pathlib import Path
from babelfish import Language
from subliminal import download_best_subtitles, region, save_subtitles, scan_videos, Subtitle

def getSetFromString(languagesString):
    languagesArray = languagesString.split(",")
    languages = set()
    for lang in languagesArray:
        languages.add(Language(lang)) 
    return languages

def setPermissions(languages, videoName):
    for lang in languages:
        try:
            os.chmod(Path(videoName).with_suffix('.'+ lang.alpha2+'.srt'), 0o0666)
        except:
            print("Could not find the subtitle " 
                    + str(Path(videoName).with_suffix('.' + lang.alpha2 + '.srt'))) 

def downloadSub(v,languages):
    # Download_best_subtitles need a string in release group
    if isinstance(v.release_group, list):
        v.release_group = v.release_group[0]
    try:
        # download best subtitles
        subtitles = download_best_subtitles([v], languages)
        # save them to disk, next to the video
        if(len(subtitles[v]) > 0):
            save_subtitles(v, subtitles[v])
            return True
        else:
            print("Could not found subtitle for " + str(v.name))
            return False
    except:
        print("Was a error saving the subtitle for: " + str(v.name))
    # give rigth permissions

def areSub(subList):
    subsExists = True
    for path in subList:
        subsExists = subsExists and os.path.exists(os.path.expanduser(path))
    return subsExists


def downloadSubsFromFolder(folder, languages):
    # scan for videos newer than 2 weeks and their existing subtitles in a folder
    #age=timedelta(weeks=2)
    videos = scan_videos(folder, age=None)
    for v in videos:
        subList = []
        for lang in languages:
            subList.append(Path(v.name).with_suffix('.'+ lang.alpha2+'.srt'))
        # Check if subs alredy exists    
        subsExists = areSub(subList)
        if not subsExists:
            print("Downloading subtitles for: " + v.name)
            donwloaded = downloadSub(v,languages)
            # give rigth permissions
            if donwloaded:
                setPermissions(languages, v.name)


FOLDERS = ['movies','tvshows']
minsToSleep = int(os.getenv('MINS'))

# configure the cache
region.configure('dogpile.cache.dbm', arguments={'filename': 'cachefile.dbm'})

# get languages to download
languagesString = os.getenv("LANGUAGES")
languages = getSetFromString(languagesString)

while True:
    for folder in FOLDERS:
        downloadSubsFromFolder(folder, languages)
    time.sleep(60*minsToSleep)
    