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
        for node1 in dict1.keys():
            for node2 in dict2.keys():

                for node1_adjac in self.cattree.adjlist[node1]: 
                    if node2 == node1_adjac[0]:
                        if dict1[node1][0][0] == to_remove_start or dict2[node2][0][0] == to_remove_end:
                            continue
                        for occur_1 in dict1[node1]:
                            for occur_2 in dict2[node2]:
                                if dirn == 12:
                                    to_ret.append((dirn, node1, node2, occur_1[ht], occur_2[ht])) #dirn of edge, node in s1, node in s2
                                else:
                                    to_ret.append((dirn, node2, node1, occur_2[ht], occur_1[ht])) 

                # for node2_adjac in self.cattree.adjlist[node2]:
                #     if node1 == node2_adjac[0]:
                #         if dict1[node1][0] == to_remove_end or dict2[node2][0] == to_remove_start:
                #             continue
                #         to_ret.append((-1, node1, node2)) #can change to 0 or 1            
                
        return to_ret

    def compare_two_cats(self, cat1, cat2): 
        
        #subtree 1
        cat1_parents = self.cattree.get_neighbours(cat1, 2, "parents")
        cat1_children = self.cattree.get_neighbours(cat1, 2, "children")
        #subtree 2
        cat2_parents = self.cattree.get_neighbours(cat2, 2, "parents")
        cat2_children = self.cattree.get_neighbours(cat2, 2, "children")

        # n1, n2 are siblings, start is CA
        p_pn = self.compare_dicts(cat1_parents, cat2_parents, 0, None, 12)
        p_pn += self.compare_dicts(cat2_parents, cat1_parents, 0, None, 21)

        # labelless relations
        np_c = self.compare_dicts(cat1_parents, cat2_children, None, 0, 12)
        np_c += self.compare_dicts(cat2_parents, cat1_children, None, 0, 21)

        c_c = self.compare_dicts(cat1_children, cat2_children, 0, 0, 12)
        c_c += self.compare_dicts(cat2_children, cat1_children, 0, 0, 21)

        # parent-child
        nc_pn = self.compare_dicts(cat1_children, cat2_parents, None, None, 12)
        nc_pn += self.compare_dicts(cat2_children, cat1_parents, None, None, 21)

        print(p_pn,"\n\n")
        print(np_c,"\n\n")
        print(c_c,"\n\n")
        print(nc_pn,"\n\n")


wikiparser = WikiParser(cattree, articletree, articlemap)
wikiparser.compare_two_cats(50624508, 38398308)