import json
import tqdm
import requests

cat_id2kg_vec = {}
cat_kg_ids = set()
art_ids = set()
found_cat_ids = set()
kg2cat = {}

#load the category IDs for all articles  under Union Territories
#with open("../../data/article_id_name.txt") as f:
    
#    line = f.readline().strip()

#    while(line):
#        id, _ = line.split(":", 1)
#        art_ids.add(int(id))

#        line = f.readline().strip()

with open("../../data/cat2kg_id.json") as f:
    data = json.load(f)
    cat_kg_ids = set(data.values())
    
    kg2cat = {value:key for key, value in data.items()}

    print(len(cat_kg_ids))

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

        print(id)
        print([float(val) for val in (vec.split(" "))])
        break
        
        if id in cat_kg_ids:
            if id not in cat_id2kg_vec:
                #cat_id2kg_vec[id] = 2
                cat_id2kg_vec[id] = [float(val) for val in (vec.split(" "))] 
                cat_vec_count += 1
                found_cat_ids.add(id)

        line = f.readline().strip()

print("\n---------------------------------------------")
print("Total vectors: ", vec_count)
print("Total Cat vecs: ", cat_vec_count)
print("Total Word Keys: ", word_key_count)

diff = cat_id2kg_vec.difference(found_cat_ids)        
print(diff)


