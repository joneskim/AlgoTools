# this is pretty much the same as main.py but with a different implementation
# in this version i try to implement the algorithms in a more object-oriented way
# and applying the gang of four design patterns
# specifically the strategy pattern, template method pattern(with hooks)

class Graph:
    def __init__(self):
        self.nodes = {}

    def add_node(self, node):
        self.nodes[node] = []

    def add_edge(self, node1, node2):
        self.nodes[node1].append(node2)

class DFSTraversalTemplate:
    WHITE = 0
    GRAY = 1
    BLACK = 2

    def __init__(self, graph: "Graph"):
        self.graph = graph
        self.COLORS = {}
        self.discovery = {}
        self.finish = {}
        self.parents = {}
        self.time = 0

    def initialize(self):
        self.COLORS = {node: self.WHITE for node in self.graph.nodes}
        self.discovery = {node: None for node in self.graph.nodes}
        self.finish = {node: None for node in self.graph.nodes}
        self.parents = {node: None for node in self.graph.nodes}
        self.time = 0
    
    def run(self, start_node = None):
        self.initialize()
        self.dfs(start_node)

    def dfs(self, node):
        self.COLORS[node] = self.GRAY
        self.discovery[node] = self.time
        self.time += 1

        self.pre_process(node)
        
        for neighbor in self.graph.nodes[node]:
            if self.COLORS[neighbor] == self.WHITE:
                self.parents[neighbor] = node
                self.dfs(neighbor)
            elif self.COLORS[neighbor] == self.GRAY:
                self.back_edge(node, neighbor)
            elif self.COLORS[neighbor] == self.BLACK:
                if self.discovery[node] < self.discovery[neighbor]:
                    self.forward_edge(node, neighbor)
                else:
                    self.cross_edge(node, neighbor)
        
        self.COLORS[node] = self.BLACK
        self.finish[node] = self.time
        self.time += 1
        self.post_process(node)

    def pre_process(self, node):
        pass
    
    def post_process(self, node):
        pass
    
    def back_edge(self, node, neighbor):
        pass
        
    def forward_edge(self, node, neighbor):
        pass
        
    def cross_edge(self, node, neighbor):
        pass
        

class DFSTraversal(DFSTraversalTemplate):
    def __init__(self, graph: "Graph"):
        super().__init__(graph)
    
    def run(self, start_node = None):
        self.initialize()
        self.dfs(start_node)
        return self.discovery, self.finish, self.parents



class TopoSort(DFSTraversalTemplate):
    def __init__(self, graph: "Graph"):
        super().__init__(graph)
        self.topo_order = []
    
    def post_process(self, node):
        self.topo_order.append(node)

    def run(self, start_node = None):
        self.initialize()
        self.dfs(start_node)
        return self.topo_order
        

if __name__ == "__main__":
    graph = Graph()


    graph.nodes = {
        'A': ['B', 'C'],
        'B': ['A', 'D', 'E'],
        'C': ['A', 'F'],
        'D': ['B'],
        'E': ['B', 'F'],
        'F': ['C', 'E']
    }

    # traversal = DFSTraversal(graph)
    # traversal.run('A')
    
    
    
    # print("Discovery Times:")
    # for k, v in traversal.discovery.items():
    #     print(f"{k}: {v}")
    
    # print("Finish Times:")
    # for k, v in traversal.finish.items():
    #     print(f"{k}: {v}")
    
    # print("Parents:")
    # for k, v in traversal.parents.items():
    #     print(f"{k}: {v}")

    
    topo_sort = TopoSort(graph)
    topo_sort.run('A')
    print("Topo Sort:")
    for k in topo_sort.topo_order[::-1]:
        print(f"{k}")
    