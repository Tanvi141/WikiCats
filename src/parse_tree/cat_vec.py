import json
import tqdm

id2vec = {}
cat_ids = set()

#load the category IDs for all cat under Union Territories
with open("../../data/article_id_name.txt") as f:
    
    line = f.readline().strip()

    while(line):
        id, _ = line.split(":", 1)
        cat_ids.add(int(id))

        line = f.readline().strip()

with open("../../../WikipediaClean5Negative300Skip10/WikipediaClean5Negative300Skip10.txt") as f:

    line_count = 0
    vec_count = 0
    cat_vec_count = 0
    word_key_count = 0
    line = f.readline().strip() #ignoring the header line
    line = f.readline().strip()
    
    while(line):
        
        line_count += 1

        if line_count % 10000 == 0:
            print("Read", line_count, "line | UT cats so far", cat_vec_count)

        vec_count += 1
        id, vec = line.split(" ", 1)

        #check if the Key is an ID or a word
        try:
            id = int(id)
        except:
            word_key_count += 1
            line = f.readline().strip()
            continue
        
        if id in cat_ids:
            if id not in id2vec:
                # id2vec[id] = [float(val) for val in (vec.split(" "))] 
                cat_vec_count += 1

        line = f.readline().strip()

print("\n---------------------------------------------")
print("Total vectors: ", vec_count)
print("Total Cat vecs: ", cat_vec_count)
print("Total Word Keys: ", word_key_count)
        


