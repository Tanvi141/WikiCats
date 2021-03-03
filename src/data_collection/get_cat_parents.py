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
import tqdm

uids = {}
already_writ = set()
fail_cats = []

S = requests.Session()
URL = "https://en.wikipedia.org/w/api.php"

def get_parents(cat_name):
    global already_writ
    global uids

    already_writ.add(cat_name)

    PARAMS = {
        "action" : "query",
        "titles" : cat_name,
        "prop" : "categories", 
        "format":"json",
        # "cmlimit": 500,
        #"continue":{"cmcontinue":"subcat|2a44503a36522a042a4430042c2a4c2c52302a04483246484032042c5a044c32403a363a464401250901dcbbdc1d|15974431","continue":"-||"},
        #"cmcontinue":"subcat|2a44503a36522a042a4430042c2a4c2c52302a04483246484032042c5a044c32403a363a464401250901dcbbdc1d|15974431",
    }

    R = S.get(url=URL, params=PARAMS)
    data = R.json()
    all_parents = []

    try:
        for _, cat_data in data['query']['pages'].items():
            all_parents = [obj['title'] for obj in cat_data['categories']]
    except:
        global fail_cats
        fail_cats.append(cat_name)

    with open("../../data/categories_parents.txt", 'a') as f:
        f.write(cat_name[9:]+":")
        for parent in all_parents:
            f.write(parent.strip('\t')[9:]+"\t")
        f.write("\n")

    # print(all_parents)
    return all_parents

def parents_galore(cat_name, hops):

    if hops == 0:
        return

    global already_writ
    parents = get_parents(cat_name)
    for next_parent in parents:
        if next_parent in already_writ:    
            continue
        parents_galore(next_parent, hops-1)

with open('../../Union_Territories/Union Territories of India_cat_keys.txt','r') as f:
    cat_ids = json.load(f)

for key, _ in tqdm.tqdm(cat_ids.items()):
    parents_galore(key,3)

print("\nFail Categories:\n",len(fail_cats),"\n",fail_cats)
