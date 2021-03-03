from collections import Counter
import statistics
import json
import numpy as np
from Tree import cattree, articletree
from ArticleMap import articlemap

class LabelMatcher():

    def __init__(self, cattree, articletree, articlemap):
        self.cattree = cattree
        self.articletree = articletree
        self.articlemap = articlemap
    
    def identify_articles_in_subtree(self, catname): #finding S1 from p1
        subcats = self.cattree.get_neighbours(catname, 1000, "children") #getting the entire subtree
        subcats[catname] = [(0,0)]

        subarts = self.articlemap.get_articles_in_cats(subcats)

        return subarts

    def get_inlink_neighbours(self, subarts):#get S2 from S1
        neighbours = {}

        for article in subarts.keys():
            neighbours.update(self.articletree.get_neighbours(article, 1, "children")) #getting the 1-hop neighbours

        return neighbours
    
    def identify_all_parents_single_article(self, artname, hop_height):
        
        all_cats = set()
        one_hop = set(self.articlemap.get_cats_of_articles([artname]))
        #do i want n-hops of all of these, or just the top ones?
        all_cats = all_cats.union(one_hop)

        for cat in one_hop:
            all_cats = all_cats.union(set(self.cattree.get_neighbours(cat, hop_height-1, "parents").keys()))

        return list(all_cats)

    def identify_labels(self, articles, hop_height):#get [p2] from S2

        all_parents = []
        for article in articles:
            all_parents += self.identify_all_parents_single_article(article, hop_height)
        
        parent_counts = Counter(all_parents)

        parent_counts = {k: v for k, v in sorted(parent_counts.items(), key=lambda item: item[1], reverse=True)} #sorting by value

        return parent_counts

    def get_matching_articles(self, article):
        cats = self.articlemap.get_cats_of_articles([article])
        
        for p1 in cats:
            S1 = self.identify_articles_in_subtree(p1)
            S2 = self.get_inlink_neighbours(S1)
            potential_p2 = self.identify_labels(S2, 2)
            print(potential_p2)
            break

labelmatcher = LabelMatcher(cattree, articletree, articlemap)
labelmatcher.get_matching_articles(28712618)