'''
Get all the categories for each article that
falls under the Union Territories subdomain.
'''

import requests
import json
import time
import platform    # For getting the operating system name
import subprocess  # For executing a shell command

from utils import Utils

category2id = {}
id2article = {}

S = requests.Session()
URL = "https://en.wikipedia.org/w/api.php"

util = Utils()
category2id = {}
id2article = {}


'''
Function to return the set of categories associated
with a given input article
'''
def get_all_categories(article_id):

    PARAMS = {
        "action" : "query",
        "prop" : "categories", 
        "format":"json",
        "cllimit": 500,
        "clshow":"!hidden",
        "pageids" : article_id,
    }

    try:
        R = S.get(url=URL, params=PARAMS)
        data = R.json()
    except:
        time.sleep(600)
        R = S.get(url=URL, params=PARAMS)
        data = R.json()

    category_set = set()
    try:
        category_info = data["query"]["pages"][article_id]["categories"]
    except:
        return []

    for category in category_info:
        
        title = category["title"]
        id = util.get_id_from_title(title)

        if title not in category2id:
            category2id[title] = id
        category_set.add(id)
    
    return list(category_set)
       
'''
Use the subpages under each category in the subdomain
to get all the articles that are present. Get the
categories corresponding to each article using the wiki API
'''
article_cat_map = {}
count = 1

with open("../../Union_Territories/consolidated_subpages.txt",'r') as f:
    
    line = f.readline().strip()

    while(line):
        
        if count % 10 == 0:
            with open("log.txt", "w") as wr:
                wr.write("C =" + str(count))
            time.sleep(600)
        count += 1

        _, article_ids = line.split(':')
        article_ids = article_ids.split(",")[:-1]
        
        if len(article_ids) < 1:
            line = f.readline().strip()
            continue
   
        '''
        For each article corresponding to the list of subpages
        obtain the categories for that article using the API
        '''
        for a_id in article_ids:
            
            id2article[a_id] = util.get_title_from_id(a_id)
            article_cat_map[a_id] = get_all_categories(a_id)
            #break
        
        line = f.readline().strip()
        #break


print("ID to article ...")
#print(id2article)
with open("../../data/id2article.json", 'w') as f:
    json.dump(id2article, f)


print("\n\ncategory 2 id ...")
#print(category2id)
with open("../../data/category2id.json", 'w') as f:
    json.dump(category2id, f)


print("\n\narticle cat map ...")
#print(article_cat_map)
with open("../../data/article_cat_map.json", 'w') as f:
    json.dump(article_cat_map, f)

print("All Done!")
        

