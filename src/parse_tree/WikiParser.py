import statistics
from Tree import cattree, articletree
from ArticleMap import articlemap

class WikiParser():

    def __init__(self, cattree, articletree, articlemap):
        self.cattree = cattree
        self.articletree = articletree
        self.articlemap = articlemap
    
   
    def compare_dicts(self, dict1, dict2, to_remove_start, to_remove_end, dirn, ht=0): 
        #pass to_remove_* as 0 if you want to remove, else pass as none
        to_ret = []
        score_components = []

        for node1 in dict1.keys():
            for node2 in dict2.keys():

                for node1_adjac in self.cattree.adjlist[node1]: 
                    if node2 == node1_adjac[0]:
                        if dict1[node1][0][0] == to_remove_start or dict2[node2][0][0] == to_remove_end:
                            continue
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
        
        try:
            return [to_ret, statistics.mean(score_components)]
        except:
            return [to_ret, 100000]

    def get_cat_score(self, cat1, cat2): 
        
        #subtree 1
        cat1_parents = self.cattree.get_neighbours(cat1, 2, "parents")
        cat1_children = self.cattree.get_neighbours(cat1, 2, "children")
        #subtree 2
        cat2_parents = self.cattree.get_neighbours(cat2, 2, "parents")
        cat2_children = self.cattree.get_neighbours(cat2, 2, "children")

        # n1, n2 are siblings, start is CA
        p_pn = self.compare_dicts(cat1_parents, cat2_parents, 0, None, 12)
        temp = self.compare_dicts(cat2_parents, cat1_parents, 0, None, 21)
        p_pn[0] += temp[0]
        p_pn[1] += temp[1]
 
        # labelless relations
        np_c = self.compare_dicts(cat1_parents, cat2_children, None, 0, 12)
        temp = self.compare_dicts(cat2_parents, cat1_children, None, 0, 21)
        np_c[0] += temp[0]
        np_c[1] += temp[1]

        c_c = self.compare_dicts(cat1_children, cat2_children, 0, 0, 12)
        temp = self.compare_dicts(cat2_children, cat1_children, 0, 0, 21)
        c_c[0] += temp[0]
        c_c[1] += temp[1]

        # parent-child
        nc_pn = self.compare_dicts(cat1_children, cat2_parents, None, None, 12)
        temp = self.compare_dicts(cat2_children, cat1_parents, None, None, 21)
        nc_pn[0] += temp[0]
        nc_pn[1] += temp[1]

        print(p_pn,"\n\n")
        print(np_c,"\n\n")
        print(c_c,"\n\n")
        print(nc_pn,"\n\n")

        cat_score = p_pn[1] + np_c[1] + c_c[1] + nc_pn[1]
        
        return cat_score

    def get_art_score(self, cat1, cat2):
        return 0

    def compare_two_cats(self, cat1, cat2):
        cat_score = self.get_cat_score(cat1, cat2)
        art_score = self.get_art_score(cat1, cat2)

        sk_score = cat_score + art_score
        print(sk_score)
        return sk_score

wikiparser = WikiParser(cattree, articletree, articlemap)
wikiparser.compare_two_cats(50624508, 38398308)