import statistics
import json
import numpy as np
from Tree import cattree, articletree
from ArticleMap import articlemap

class WikiParser():

    def __init__(self, cattree, articletree, articlemap):
        self.cattree = cattree
        self.articletree = articletree
        self.articlemap = articlemap
    
   
    def compare_dicts(self, dict1, dict2,  search_tree, dirn,ht=0): 
        #pass to_remove_* as 0 if you want to remove, else pass as none
        to_ret = []
        score_components = []

        for node1 in dict1.keys():
            for node2 in dict2.keys():
                try: #TODO: some articles missing in files
                    for node1_adjac in search_tree.adjlist[node1]: 
                        if node2 == node1_adjac[0]:
                            for occur_1 in dict1[node1]:
                                for occur_2 in dict2[node2]:
                                    eles = []
                                    if dirn == 12:
                                        to_ret.append((dirn, node1, node2, occur_1[ht], occur_2[ht])) #dirn of edge, node in s1, node in s2
                                    else:
                                        to_ret.append((dirn, node2, node1, occur_2[ht], occur_1[ht])) 
                                    eles.append(\
                                        abs(occur_1[ht]) + abs(occur_2[ht]) \
                                    )
                            try:
                                score_components.append(statistics.mean(eles))
                            except:
                                pass
                except:
                    # print("error:", node1)
                    pass
        try:
            return [to_ret, 1/statistics.mean(score_components)]
        except:
            return [to_ret, 1/1000000] #TODO
    
    def get_score_components(self, cat1, cat2, subtrees, search_tree): 
        subscores = []
        entities = []
        for from_node in range(3):  #0:p, 1:n, 2:c
            for to_node in range(3): #["p","n","c"]
                val = self.compare_dicts(subtrees[from_node], subtrees[3+to_node], search_tree, 12)
                temp = self.compare_dicts(subtrees[3+from_node], subtrees[to_node], search_tree, 21)
                val[0] += temp[0]  
                val[1] += temp[1]  

                subscores.append(val[1])
                entities.append(val[0])

        #subscores is
        #0:p->p
        #1:p->n
        #2:p->c
        #3:n->p
        #4:n->n
        #5:n->c
        #6:c->p
        #7:c->n
        #8:c->c
        return np.array(subscores), entities

    def get_cat_score(self, cat1, cat2, subtrees):
        components, _ = self.get_score_components(cat1, cat2, subtrees, self.cattree)
        weights = np.array([1, 1, 10, 5, 5, 10, 5, 5, 20])
        # print(components)
        return np.dot(components, weights)

    def get_art_score(self, cat1, cat2, subtrees):
        article_mapped_subtrees = [self.articlemap.get_articles_in_cats(tree) for tree in subtrees]
        components, _ = self.get_score_components(cat1, cat2, article_mapped_subtrees, self.articletree)
        weights = np.array([5, 8, 3, 8, 12, 3, 3, 5, 1])
        return np.dot(components, weights)

    def compare_two_cats(self, cat1, cat2):

         #subtree 1
        cat1_parents = self.cattree.get_neighbours(cat1, 2, "parents")
        cat1_children = self.cattree.get_neighbours(cat1, 2, "children")
        cat1_self = {cat1:[(0,0)]}
        #subtree 2
        cat2_parents = self.cattree.get_neighbours(cat2, 2, "parents")
        cat2_children = self.cattree.get_neighbours(cat2, 2, "children")
        cat2_self = {cat2:[(0,0)]}
        subtrees = (cat1_parents, cat1_self, cat1_children, cat2_parents, cat2_self, cat2_children)


        cat_score = self.get_cat_score(cat1, cat2, subtrees)
        art_score = self.get_art_score(cat1, cat2, subtrees)
        # art_score = 0

        sk_score = 0*cat_score + art_score
        print(sk_score) #TODO: depth of the article
        return sk_score

    def get_best_match(self, catname, search_space):
        f = open("../../Union_Territories/Union Territories of India_cat_keys.txt","rb")
        label_map = json.load(f)
        f.close()
        inv_map = {v: k for k, v in label_map.items()}
        sk_scores = []
        for cat2 in search_space:
            score = self.compare_two_cats(catname, cat2)
            try:
                sk_scores.append((score, inv_map[cat2]))
            except:
                sk_scores.append((score, "Original"))
        sk_scores = sorted(sk_scores, reverse=True)
        print(sk_scores)

wikiparser = WikiParser(cattree, articletree, articlemap)
# wikiparser.compare_two_cats(6969241, 9746199)
wikiparser.get_best_match(52499719, wikiparser.cattree.adjlist.keys())