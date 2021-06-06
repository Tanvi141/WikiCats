import json
import requests
import time

S = requests.Session()
URL = "https://en.wikipedia.org/w/api.php"
fail_kg_ids = 0

def get_wikidata_id(cat_name):
    PARAMS = {
        "action" : "query",
        "titles" : cat_name,
        "prop" : "pageprops", 
        "ppprop": "wikibase_item",
		"redirects":"1",
        "format":"json",
        # "cmlimit": 500,
        #"continue":{"cmcontinue":"subcat|2a44503a36522a042a4430042c2a4c2c52302a04483246484032042c5a044c32403a363a464401250901dcbbdc1d|15974431","continue":"-||"},
        #"cmcontinue":"subcat|2a44503a36522a042a4430042c2a4c2c52302a04483246484032042c5a044c32403a363a464401250901dcbbdc1d|15974431",
    }
    
    try:
        R = S.get(url=URL, params=PARAMS)
        data = R.json()
    except:
        time.sleep(600)
        R = S.get(url=URL, params=PARAMS)
        data = R.json()

    kg_id = ""
    
    for page, value in data["query"]["pages"].items():
        try:
            kg_id = value["pageprops"]["wikibase_item"]
        except:
            #print(value)
            global fail_kg_ids
            fail_kg_ids += 1
            kg_id = -1

    return kg_id


cat2kgid = {}

with open("../../data/category2id.json", 'r') as f:
    data = json.load(f)
    print(len(data))
    st_time = time.time()
    
    for i, cat in (enumerate(data.keys())):
        
        if (i+1)%1000 == 0:
            print("At cat", i+1, "in time", time.time()-st_time)
            st_time = time.time()
            time.sleep(600)
        kg_id = get_wikidata_id(cat)
        cat2kgid[cat] = kg_id

print("KG IDs couldn't be extracted for ", fail_kg_ids, "categories")

with open("../../data/cat2kg_id.json", 'w') as f:
    json.dump(cat2kgid, f)
    

        
