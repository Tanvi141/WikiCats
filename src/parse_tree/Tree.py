import json
blacklist  = [60159159, 59055138, 62028269, 63588168, 59055138, 59055145, 63587964, 63588072, 63588010, 63588075, 60159153, 60159163]
class Tree():

    def __init__(self, adj_list_filename, id_map_filename, extend_rev_adjlist = False):

        self.adjlist = {}
        self.rev_adjlist = {}
        self.id2name = {}
        self.name2id = {}

        f = open(adj_list_filename, "r")
        line = f.readline().strip("\n")
        while(line):
            node, nodelist = line.split(":")
            node = int(node)
            nodelist = nodelist.split(",")

            if node in blacklist:
                continue

            if node not in self.adjlist:    
                self.adjlist[node] = [] 

            for item in nodelist:
                
                try:
                    next_node, wt = item.split("-")
                    next_node = int(next_node)
                    wt = int(wt)
                except:
                    try:
                        next_node = int(item)
                        wt = 1
                    except:
                        continue
                
                if next_node in blacklist:
                    continue

                self.adjlist[node].append((next_node,wt))

                if next_node not in self.rev_adjlist:
                    self.rev_adjlist[next_node] = []

                self.rev_adjlist[next_node].append((node, wt))

            line = f.readline().strip("\n")

        if len(self.adjlist) == len(self.rev_adjlist)+1:
            # raise Exception("Incorrectly parsed", len(self.adjlist), len(self.rev_adjlist))
            self.rev_adjlist[3970272] = []
        self.num_nodes = len(self.adjlist)
        
          #populating the ID2map and map2id dictionaries for categories and articles
        try:
            with open(id_map_filename) as json_file: 
                self.name2id.update(json.load(json_file))
                self.id2name.update({int(value) : key for (key, value) in self.name2id.items()})
                self.name2id= {value : int(key) for (key, value) in self.id2name.items()}

        except:
            with open(id_map_filename, 'r') as f:
                line = f.readline().strip('\n')

                while(line):
                    id, title = line.split(':',1)
                    id = int(id)
                    self.name2id[title] = id
                    self.id2name[id] = title
                    line = f.readline().strip('\n')

        if extend_rev_adjlist:
            with open('../../data/categories_parent_ids.txt','r') as f1, open('../../data/categories_parents.txt') as f2:
                line1 = f1.readline().strip("\n")
                line2 = f2.readline().strip("\n")
                while(line1):
                    cat, parents = line1.split(':',1)
                    catname, parentsnames = line2.split(':',1)

                    parent_cats = parents.split('\t')[:-1]
                    cat = int(cat)

                    if cat in blacklist:
                        line1 = f1.readline().strip("\n")
                        line2 = f2.readline().strip("\n")
                        continue

                    parent_cats = [int(p) for p in parent_cats]
                    if cat not in self.rev_adjlist:
                        self.rev_adjlist[cat] = []

                    for parent in parent_cats:
                        if parent not in blacklist:
                            self.rev_adjlist[cat].append((parent,1))
                        
                    line1 = f1.readline().strip("\n")
                    line2 = f2.readline().strip("\n")

                    self.rev_adjlist[cat] = list(set(self.rev_adjlist[cat]))

                    self.name2id[catname] = cat
                    self.id2name[cat] = catname
                    parentsnames = parentsnames.split('\t')[:-1]
                    for pid, pname in zip(parent_cats, parentsnames):
                        if pid not in blacklist:
                            self.name2id[pname] = pid
                            self.id2name[pid] = pname

    def get_neighbours_recurse(self, node, hops, dirn, track = 1, w = 0): #do we also want to trace the path?
        if hops < 0:
            raise Warning("Negative hops")
        elif hops == 0:
            return []
        else:
            to_return = []
            # further_children = []
            try:
                if dirn == "children":
                    for node_info in self.adjlist[node]:
                        node_next, wt = node_info
                        to_return.append((node_next, w + wt, track))
                        to_return += self.get_neighbours_recurse(node_next, hops-1, dirn, track+1, w+wt) 


                elif dirn == "parents":
                    for node_info in self.rev_adjlist[node]:
                        node_next, wt = node_info
                        to_return.append((node_next, w - wt, -1*track))
                        to_return += self.get_neighbours_recurse(node_next, hops-1, dirn, track+1, w-wt) 

                else:
                    raise Exception("Invalid dirn")

            except:
                # passable = [66401928, 66332501,  66323714, 66286062, 66294548, 66340636, 66402743, 66284249, 66296944, 66341416, 66393006]
                # print("Article too new to be in adjlist", node)
                pass
                
        return to_return

    def get_neighbours(self, node, hops, dirn):
        as_list = self.get_neighbours_recurse(node, hops, dirn)
        ret_dict = {}

        for item in as_list:
            catname, wt_dist, hop_dist = item
            if catname not in ret_dict:
                ret_dict[catname] = []
            
            ret_dict[catname].append((wt_dist, hop_dist))
        
        #the node itself
        # ret_dict[node] = [(0,0)]
        
        return ret_dict

cattree = Tree("../../data/al_subcat_tree.txt", '../../Union_Territories/Union Territories of India_cat_keys.txt', True)
articletree = Tree("../../data/al_inlinks_tree.txt", "../../data/article_id_name.txt")