from collections import Counter
import statistics
import json
import numpy as np
from Tree import cattree, articletree
from ArticleMap import articlemap
import copy
import math

class LabelMatcher():

    def __init__(self, cattree, articletree, articlemap):
        self.cattree = cattree
        self.articletree = articletree
        self.articlemap = articlemap
    
    def identify_articles_in_subtree(self, catname): #finding S1 from p1
        subcats = self.cattree.get_neighbours(catname, 1000, "children") #getting the entire subtree
        subcats[catname] = [(0,0)]

        subarts = self.articlemap.get_articles_in_cats(subcats, True)

        return subarts

    def get_inlink_neighbours(self, subarts):#get S2 from S1
        neighbours = {}

        for article in subarts.keys(): 
            tmp = self.articletree.get_neighbours(article, 1, "children") #getting the 1-hop neighbours #CHECK PARENTS VS CHILDREN
            for t in tmp:
                if t not in neighbours:
                    neighbours[t] = []
                neighbours[t] += tmp[t]

        return neighbours
    
    def identify_all_parents_single_article(self, artname, hop_height):
        
        all_cats = set()
        one_hop = set(self.articlemap.get_cats_of_articles([artname], True))
        #do i want n-hops of all of these, or just the top ones?
        all_cats = all_cats.union(one_hop)

        depth_dict = {}

        for catname in all_cats:
            depth_dict[catname] = 0 #means direct parent 

        for cat in one_hop:
            #if multiple heights for the same article, take the minimum
            #we want to incorporate the hop_distance
            temp = self.cattree.get_neighbours(cat, hop_height-1, "parents") 
            for catname in temp:
                val = min([k[0] for k in temp[catname]])
                if catname not in depth_dict:
                    depth_dict[catname] = val 
                else: 
                    depth_dict[catname] = min(val, depth_dict[catname])

        return depth_dict #dict[cat] = minimum depth

    def identify_labels(self, articles, hop_height):#get [p2] from S2

        all_parents = []

        possible_p2_wts = {} #the hop distance weights in art tree (infobox etc)
        possible_p2_dpts = {} #the distance from the article
        for article in articles:
            wt = sum([k[0] for k in articles[article]]) #we take into account the weight of edges

            temp = self.identify_all_parents_single_article(article, hop_height)

            for catname in temp:
                if catname not in possible_p2_wts:
                    possible_p2_wts[catname] = 0
                # possible_p2_wts[catname] += wt #TODO: Figure out why this is not giving good results! Could be because it gives high wt to infobox
                possible_p2_wts[catname] += 1
                
                if catname not in possible_p2_dpts:
                    possible_p2_dpts[catname] = []
                possible_p2_dpts[catname].append(temp[catname])
        

        parent_counts = {k: v/(6+self.cattree.id2height[k] + statistics.mean(possible_p2_dpts[k])) #TODO: do something to ensure no div by 0
        for k, v in sorted(possible_p2_wts.items(), key=lambda item: item[1], 
        reverse=True)} #sorting by value
        
        parent_counts = {k: v for k, v in sorted(parent_counts.items(), key=lambda item: item[1], reverse=True)} #sorting by value

        return parent_counts

    def get_matching_cats(self, catname, hts1):
        S1 = self.identify_articles_in_subtree(catname)
        check_potential_p1 = self.identify_labels(S1, -hts1)

        # print(S1)
        S2 = self.get_inlink_neighbours(S1)
        potential_p2 = self.identify_labels(S2, 3)
        return potential_p2, check_potential_p1

    def get_tfidf_scores(self, p12):

        '''
        The term frequency (occurence of a p2 in a p1) is always =1
        since the identify labels function returns a dictionary of potential P2s

        IDF is computed by taking into account the number of p1s 
        that contain a particular p2
        '''

        p1p2 = copy.deepcopy(p12)
        p2_count = {}
        total_docs = len(p1p2)

        for p1 in p1p2.keys():
            for p2 in p1p2[p1].keys():

                if p2 not in p2_count:
                    p2_count[p2] = 1
                else:
                    p2_count[p2] += 1

        for p1 in p1p2.keys():

            for p2 in p1p2[p1].keys():
                p1p2[p1][p2] *= np.log(total_docs / (1+p2_count[p2]))

            p1p2[p1] = dict(sorted(p1p2[p1].items(), key=lambda item: item[1], reverse=True))
        

        return p1p2



    def get_matching_articles(self, article, up_height):
        
        cats = self.articlemap.get_cats_of_articles([article])
        
        potential_p1 = set()
        p1_depths = {}
        # print(cats)
        for cat in cats:
            # print("PARENTS OF CAT", cat)
            temp_dict = self.cattree.get_neighbours(cat, up_height, "parents")
            temp_dict2 = self.cattree.get_neighbours(cat, 100, "parents")
            
            for p1 in temp_dict.keys():
                potential_p1.add(p1)
                
            for p1 in temp_dict2.keys(): # a lot of misc garbage entries will also come in but we will not access them
                if p1 == 37327939:
                    print(temp_dict2[p1])
                if p1 not in p1_depths:  
                    p1_depths[p1] = temp_dict2[p1]
                else:
                    p1_depths[p1] += temp_dict2[p1]  
                # p1_depths[p1] = temp_dict[p1][0][0]
                # p1_depths[p1] = self.cattree.id2height[p1]
            
        # make sure that there are no ancestors if a->b->c, a and c in potential_p1, keep only c
        p1_map_p2 = {}
        p1_map_p1 = {} #checkign whether p1 is good or no
        for p1 in potential_p1:        
            #print("\n\nWith label as", self.cattree.id2name[p1])
            pot_p2, pot_p1 = self.get_matching_cats(p1, -3)
            p1_map_p2[p1] = pot_p2
            p1_map_p1[p1] = pot_p1
            #print([(p2, self.cattree.id2name[p2], pot_p2[p2]) for p2 in pot_p2][:20])
            # break

        p1_map_p2_tfidf = self.get_tfidf_scores(p1_map_p2)
        # p1_map_p1_tfidf = self.get_tfidf_scores(p1_map_p1)

        # p1_map_p1_tfidf = dict(sorted(p1_map_p1_tfidf.items(), key=lambda item: (len(item[1])*-1*p1_depths[item[0]])))
        
        p1_fitness = {}
        for p1 in potential_p1:
            p1_fitness[p1] = 0
            c = 0
            for p11_dict in p1_map_p1.values():
                if p1 in p11_dict:
                    p1_fitness[p1] += p11_dict[p1]
                    c+=1
            # if c!=0:
            #     p1_fitness[p1]/=c

            

        p1_fitness = dict(sorted(p1_fitness.items(), key=lambda item: item[1]))

        
        for p1 in p1_fitness.keys():
            
            pot_p2_dict = p1_map_p2_tfidf[p1]
            print("\n\nWith label as", self.cattree.id2name[p1], p1)
            # print("Len pot p2", len(pot_p2_dict))
            # print([(p2, self.cattree.id2name[p2], pot_p2_dict[p2]) for p2 in pot_p2_dict ][:20])
            # print([(p11, self.cattree.id2name[p11], p1_map_p1[p1][p11]) for p11 in p1_map_p1[p1]][:20])
            # print()
            print("Len of tfidf p1", len(p1_map_p1[p1]))
            print("Depth in tree", p1_depths[p1])
            # print("score", p1_depths[p1]*-1*len(p1_map_p1_tfidf[p1]))
            print("score", p1_fitness[p1])

            # print([(p11, self.cattree.id2name[p11], p1_map_p1_tfidf[p1][p11]) for p11 in p1_map_p1_tfidf[p1]][:20])
            # print()
        
labelmatcher = LabelMatcher(cattree, articletree, articlemap)
labelmatcher.get_matching_articles(47385064, 2)
# labelmatcher.get_matching_cats(2681730)
# print(labelmatcher.cattree.adjlist[2681730])
# for i in labelmatcher.articletree.adjlist[7016804]:
#     print(labelmatcher.articletree.id2name[i[0]])
# print("\\n\n")
# for i in labelmatcher.articletree.rev_adjlist[7016804]:
#     print(labelmatcher.articletree.id2name[i[0]])
# print("\\n\n")

# print("india : 37327939")
# print(labelmatcher.cattree.adjlist[37327939])
# print(labelmatcher.cattree.rev_adjlist[37327939])
# print()
# print("andaman : 35862280")
# print(labelmatcher.cattree.adjlist[35862280])
# print(labelmatcher.cattree.rev_adjlist[35862280])
