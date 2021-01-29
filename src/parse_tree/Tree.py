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
        
            self.adjlist[node] = []

            for item in nodelist:
                
                try:
                    next_node, wt = item.split("-")
                    next_node = int(next_node)
                    wt = int(wt)
                except:
                    next_node = int(item)
                    wt = 1

                self.adjlist[node].append((next_node,wt))

                if next_node not in self.rev_adjlist:
                    self.rev_adjlist[next_node] = []

                self.rev_adjlist[next_node].append((node, wt))

            line = f.readline().strip("\n")

        if len(self.adjlist) != len(self.rev_adjlist):
            raise Exception("Incorrectly parsed")

        self.num_nodes = len(self.adjlist)

    def get_neighbours(self, nodelist, hops, dirn, track = 1):
        if hops < 0:
            raise Warning("Negative hops")
        elif hops == 0:
            return []
        else:
            to_return = []
            if dirn == "children":
                for node in nodelist:               
                    for node_next in self.adjlist[node]:
                        to_return.append((node_next, track))


            elif dirn == "parents":
                for node in nodelist:               
                    for node_next in self.revadjlist[node]:
                        to_return.append((node_next, -1*track))

            to_return += get_neighbours(to_return, hops-1, dirn, track+1) 

            else:
                raise Exception("Invalid dirn")
    
    
    # Cycle detection code credits:
    # https://www.geeksforgeeks.org/python-program-for-detect-cycle-in-a-directed-graph/
    
    def isCyclicUtil(self, v, visited, recStack): 
  
        # Mark current node as visited and  
        # adds to recursion stack 
        visited[v] = True
        recStack[v] = True
  
        # Recur for all neighbours 
        # if any neighbour is visited and in  
        # recStack then graph is cyclic 
        for neighbour in self.adjlist[v]: 
            if visited[neighbour[0]] == False: 
                if self.isCyclicUtil(neighbour[0], visited, recStack) == True: 
                    return True
            elif recStack[neighbour[0]] == True: 
                return True
  
        # The node needs to be poped from  
        # recursion stack before function ends 
        recStack[v] = False
        return False
  
    # Returns true if graph is cyclic else false 
    def isCyclic(self): 

        visited = {}
        recStack = {}

        for node in self.adjlist.keys():
            visited[node] = False  
            recStack[node] = False

        for node in self.adjlist.keys(): 
            if visited[node] == False: 
                if self.isCyclicUtil(node, visited, recStack) == True: 
                    return True
        return False
