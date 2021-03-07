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
import urllib

uids = {}
already_writ = set()
fail_cats = []

S = requests.Session()
URL = "https://en.wikipedia.org/w/api.php"


with open("../../data/categories_parents.txt", 'r') as f1, open('../../data/categories_parent_ids.txt','a') as f2 :

    line = f1.readline().strip('\n')
    i = 0
    while(line):
        print(i)
        cat, parents = line.split(':',1)
        parent_cats = parents.split('\t')

        if "Category:"+cat in already_writ:
            f2.write(str(uids["Category:"+cat])+":")

        else:
            urlencoded = urllib.parse.quote_plus(cat)
            url = (
                'https://en.wikipedia.org/w/api.php'
                '?action=query'
                '&prop=info'
                '&inprop=subjectid'
                '&titles=Category:' + urlencoded +
                '&format=json')
            json_response = requests.get(url).json()

            title_to_page_id  = {
                page_info['title']: page_id
                for page_id, page_info in json_response['query']['pages'].items()}

            f2.write(str(title_to_page_id["Category:"+cat])+":")
            uids["Category:"+cat] = title_to_page_id["Category:"+cat]
            already_writ.add("Category:"+cat)

        for parent in parent_cats:
            
            if len(parent) < 1:
                continue

            parent = "Category:"+parent

            if parent in already_writ:
                f2.write(str(uids[parent])+"\t")

            else:
                urlencoded = urllib.parse.quote_plus(parent) 
                url = (
                    'https://en.wikipedia.org/w/api.php'
                    '?action=query'
                    '&prop=info'
                    '&inprop=subjectid'
                    '&titles=' + urlencoded +
                    '&format=json')
                json_response = requests.get(url).json()

                title_to_page_id  = {
                    page_info['title']: page_id
                    for page_id, page_info in json_response['query']['pages'].items()}


                f2.write(title_to_page_id[parent]+"\t")
                uids[parent] = title_to_page_id[parent]
                already_writ.add(parent)


        f2.write("\n")
        line = f1.readline().strip('\n')
        i+=1


