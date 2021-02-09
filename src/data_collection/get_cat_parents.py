#!/usr/bin/python3

"""
    get_allcategories.py

    MediaWiki API Demos
    Demo of `Allcategories` module: Get all categories, starting from a
    certain point, as ordered by category title.

    MIT License
"""

import requests
import re
import sys
import json
import threading 

uids = {}
already_writ = set()

S = requests.Session()
URL = "https://en.wikipedia.org/w/api.php"

def get_parents(cat_name, main_cat, lock):
    global already_writ
    global uids

    lock.acquire()
    already_writ.add(cat_name)
    lock.release()

    PARAMS = {
        "action" : "query",
        "titles" : cat_name,
        "prop" : "categories", 
        "format":"json",
        "cmlimit": 500,
        #"continue":{"cmcontinue":"subcat|2a44503a36522a042a4430042c2a4c2c52302a04483246484032042c5a044c32403a363a464401250901dcbbdc1d|15974431","continue":"-||"},
        #"cmcontinue":"subcat|2a44503a36522a042a4430042c2a4c2c52302a04483246484032042c5a044c32403a363a464401250901dcbbdc1d|15974431",
    }

    R = S.get(url=URL, params=PARAMS)
    data = R.json()
    print(data)


def cats_galore(cat_name, main_cat, lock):
    global already_writ
    lee = get_cats(cat_name, main_cat, lock)
    for next_cat in lee:
        if next_cat["title"] in already_writ:    
            continue
        cats_galore(next_cat["title"], main_cat, lock)

def parallel_cats_galore(cat_name):
    global already_writ
    lock = threading.Lock()
    lee = get_cats(cat_name, cat_name, lock)
    thrds = []
    for next_cat in lee:
        thrds.append(threading.Thread(target=cats_galore, args=(next_cat["title"],next_cat["title"],lock,)))
        
    print("now start")
    for i in range(len(thrds)):
        thrds[i].start()

    for i in range(len(thrds)):
        thrds[i].join()

lock = threading.Lock()
get_parents("Buildings and structures in Chandigarh", "Buildings and structures in Chandigarh", lock)
# uids["Category:"+sys.argv[1]]=sys.argv[2]
# parallel_cats_galore("Category:"+sys.argv[1])
# #get_cats(sys.argv[1])

# s_uids = {k: v for k, v in sorted(uids.items(), key=lambda item: item[0])}

# print(s_uids)
# with open('%s_cat_keys.txt'%(sys.argv[1]), 'w') as outfile:
#     json.dump(s_uids, outfile)
