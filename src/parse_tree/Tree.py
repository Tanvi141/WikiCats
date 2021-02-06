class Tree():

    def __init__(self, filename):

        self.adjlist = {}
        self.rev_adjlist = {}

        f = open(filename, "r")
        line = f.readline().strip("\n")
        while(line):
            node, nodelist = line.split(":")
            node = int(node)
            nodelist = nodelist.split(",")

            if node not in self.adjlist:    
                self.adjlist[node] = [] 
            # if node not in self.rev_adjlist:    
            #     self.rev_adjlist[node] = []

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

                self.adjlist[node].append((next_node,wt))

                if next_node not in self.rev_adjlist:
                    self.rev_adjlist[next_node] = []

                self.rev_adjlist[next_node].append((node, wt))

            line = f.readline().strip("\n")

        # if len(self.adjlist) != len(self.rev_adjlist):
        #     raise Exception("Incorrectly parsed", len(self.adjlist), len(self.rev_adjlist))

        self.num_nodes = len(self.adjlist)

    def get_neighbours_recurse(self, node, hops, dirn, track = 1, w = 0): #do we also want to trace the path?
        if hops < 0:
            raise Warning("Negative hops")
        elif hops == 0:
            return []
        else:
            to_return = []
            further_children = []
            if dirn == "children":
                for node_info in self.adjlist[node]:
                    node_next, wt = node_info
                    to_return.append((node_next, w + wt, track))
                    further_children += self.get_neighbours_recurse(node_next, hops-1, dirn, track+1, w+wt) 


            elif dirn == "parents":
                for node_info in self.rev_adjlist[node]:
                    node_next, wt = node_info
                    to_return.append((node_next, w - wt, -1*track))
                    further_children += self.get_neighbours_recurse(node_next, hops-1, dirn, track+1, w-wt) 

            else:
                raise Exception("Invalid dirn")
        
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

cattree = Tree("../../data/al_subcat_tree.txt")
articletree = Tree("../../data/al_inlinks_tree.txt")