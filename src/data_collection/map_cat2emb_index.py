import json
import numpy as np

cat2index = {}
cat_embs = None

#read the embedding file:
with open("../../data/cat2emb.txt", 'r') as f:

    line = f.readline().strip()
    cat_id_idx = 0

    while(line):

        if cat_id_idx %1000 == 0:
            print(cat_id_idx)
        cat_id, emb = line.split(":")
        emb = np.array(emb.split("\t")).astype(float)
        cat2index[cat_id] = cat_id_idx
        cat_id_idx += 1

        if cat_embs is None:
            cat_embs = emb
        else:
            cat_embs = np.vstack((cat_embs, emb))

        line = f.readline().strip()


print("Total cats = ", cat_id_idx+1)
print("Emb shape = ", cat_embs.shape)

np.save("../../data/cat_embeddings.npy", cat_embs)
with open("../../data/cat2idx.json", 'w') as f:
    json.dump(cat2index, f)
