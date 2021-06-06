import json
import random

with open("../../data/subset/article_cat_map.json",'r') as f:
    data = json.load(f)

all_keys = list(data.keys())
random.shuffle(all_keys)

train_split = int(0.8*len(all_keys))
val_split = int(0.1*len(all_keys))

train_list = all_keys[:train_split]
test_list = all_keys[train_split:train_split+val_split]
val_list = all_keys[train_split+val_split:]

with open("../../data/subset/train_articles.txt",'w') as f:
    for art in train_list:
        f.write(str(art)+"\n")

with open("../../data/subset/test_articles.txt",'w') as f:
    for art in test_list:
        f.write(str(art)+"\n")

with open("../../data/subset/val_articles.txt",'w') as f:
    for art in val_list:
        f.write(str(art)+"\n")