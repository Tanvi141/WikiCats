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

uids = {}
already_writ = set()

S = requests.Session()
URL = "https://en.wikipedia.org/w/api.php"

def get_cats(cat_name):
    global already_writ
    global uids

    already_writ.add(cat_name)

    if cat_name not in uids.keys():
        print("Something is wrong")

    PARAMS = {
        "action" : "query",
        "list" : "categorymembers",
        "cmtitle" : "Category:"+cat_name,
        "cmtype": "subcat",
        "format":"json",
        "cmlimit": 100,
        #"continue":{"cmcontinue":"subcat|2a44503a36522a042a4430042c2a4c2c52302a04483246484032042c5a044c32403a363a464401250901dcbbdc1d|15974431","continue":"-||"},
        #"cmcontinue":"subcat|2a44503a36522a042a4430042c2a4c2c52302a04483246484032042c5a044c32403a363a464401250901dcbbdc1d|15974431",
    }

   

    with open("%s_outfile.txt"%(sys.argv[1]),"a") as f:
        
        f.write(str(uids[cat_name])+":")
        while True:

            R = S.get(url=URL, params=PARAMS)
            data = R.json()
            lol = data["query"]["categorymembers"]
            #print(lol)
            for cat in lol:
                if cat["title"] not in uids.keys():
                    uids[cat["title"]] = cat["pageid"]
                f.write(str(cat["pageid"])+",")

            try:
                PARAMS["cmcontinue"] = data["continue"]["cmcontinue"]
            except:
                break
        f.write("\n") 

    return lol

def cats_galore(cat_name):
    global already_writ
    lee = get_cats(cat_name)
    for next_cat in lee:
        if next_cat["title"] in already_writ:    
            continue
        cats_galore(next_cat["title"])


uids[sys.argv[1]]=sys.argv[2]
cats_galore(sys.argv[1])
#get_cats(sys.argv[1])

s_uids = {k: v for k, v in sorted(uids.items(), key=lambda item: item[0])}

with open('%s_cat_keys.txt'%(sys.argv[1]), 'w') as outfile:
    json.dump(s_uids, outfile)
