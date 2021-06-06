class ArticleMap():

    def __init__(self, filename, articles_to_include=[]):

        self.cat_to_article = {}
        self.article_to_cat = {}

        f = open(filename, "r")
        line = f.readline().strip("\n")
        while(line):
            node, nodelist = line.split(":")
            node = int(node)

            if node not in articles_to_include:
                line = f.readline().strip("\n")
                continue

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

    def get_articles_in_cats(self, catdict, ignorefaults = False):
        to_ret = {}
        for catname in catdict.keys():
            try:
                for article_id in self.cat_to_article[catname]:
                    if article_id not in to_ret.keys():
                        to_ret[article_id] = []
                    to_ret[article_id] += catdict[catname]  #adding two lists
            except:
                if ignorefaults:
                    pass
                else:
                    raise Exception("Category is not in the Union Territories catrgory")
        return to_ret


    def get_cats_of_articles(self, articlelist, ignorefaults = False):
        to_ret = []
        for article in articlelist:
            try:
                to_ret += self.article_to_cat[article]
            except:
                if ignorefaults:
                    pass
                else:
                    raise Exception("Article is not in the Union Territories catrgory")
        return to_ret
