class ArticleMap():

    def __init__(self, filename):

        self.cat_to_article = {}
        self.article_to_cat = {}

        f = open(filename, "r")
        line = f.readline().strip("\n")
        while(line):
            node, nodelist = line.split(":")
            node = int(node)
            nodelist = nodelist.split(",")
        
            self.cat_to_article[node] = []

            for item in nodelist:
                
                try:
                    next_node = int(item)
                except:
                    continue
                
                self.cat_to_article[node].append(next_node)

                if next_node not in self.article_to_cat:
                    self.article_to_cat[next_node] = []

                self.article_to_cat[next_node].append(node)

            line = f.readline().strip("\n")

    def get_articles_in_cats(self, catdict):
        to_ret = {}
        for catname in catdict.keys():
            for article_id in self.cat_to_article[catname]:
                if article_id not in to_ret.keys():
                    to_ret[article_id] = []
                to_ret[article_id] += catdict[catname]  #adding two lists

        return to_ret


    def get_cats_of_articles(self, articlelist):
        to_ret = []
        for article in articlelist:
            to_ret += self.article_to_cat[article]
        return to_ret

articlemap = ArticleMap("../../data/consolidated_subpages.txt")