import json
import tqdm
import requests

id2vec = {}
cat_ids = set()
art_ids = set()
found_cat_ids = set()

#load the category IDs for all articles  under Union Territories
#with open("../../data/article_id_name.txt") as f:
    
#    line = f.readline().strip()

#    while(line):
#        id, _ = line.split(":", 1)
#        art_ids.add(int(id))

#        line = f.readline().strip()

with open("../../data/cat2kg_id.json") as f:
    data = json.load(f)
    cat_ids = set(data.values())
    print(len(cat_ids))
    for key, val in data.items():
        if val == "Q47038375":
            print(key) 

with open("/scratch/mallika/wikidata_translation_v1.tsv?fbclid=IwAR2_gVmlA8bhMqierg-iW6AnA_FuJ8ULdw6Zl-53pGcrzdszDwKGmjXo3C4") as f:

    line_count = 0
    vec_count = 0
    cat_vec_count = 0
    word_key_count = 0
    line = f.readline().strip() #ignoring the header line
    line = f.readline().strip()
    
    while(line):
        
        line_count += 1

        if line_count % 1000000 == 0:
            print("Read", line_count, "line | UT cats so far", cat_vec_count)

        vec_count += 1
        id, vec = line.split("\t", 1)
        id = id.rsplit('/',1)
        id = id[1][:-1]
        
        if id in cat_ids:
            if id not in id2vec:
                id2vec[id] = 2
                # id2vec[id] = [float(val) for val in (vec.split(" "))] 
                cat_vec_count += 1
                found_cat_ids.add(id)

        line = f.readline().strip()

print("\n---------------------------------------------")
print("Total vectors: ", vec_count)
print("Total Cat vecs: ", cat_vec_count)
print("Total Word Keys: ", word_key_count)

diff = cat_ids.difference(found_cat_ids)        
print(diff)


