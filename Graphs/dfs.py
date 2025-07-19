# this is pretty much the same as main.py but with a different implementation
# in this version i try to implement the algorithms in a more object-oriented way
# and applying the gang of four design patterns
# specifically the strategy pattern, template method pattern(with hooks)

from graph import Graph, TraversalVisitor, TraversalFactory, CompositeVisitor

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
        self.visitor = TraversalVisitor()

    def set_visitor(self, visitor: "TraversalVisitor"):
        self.visitor = visitor

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

        self.visitor.pre_process(node)
        
        for neighbor in self.graph.nodes[node]:
            if self.COLORS[neighbor] == self.WHITE:
                self.parents[neighbor] = node
                self.dfs(neighbor)
            elif self.COLORS[neighbor] == self.GRAY:
                self.visitor.back_edge(node, neighbor)
            elif self.COLORS[neighbor] == self.BLACK:
                if self.discovery[node] < self.discovery[neighbor]:
                    self.visitor.forward_edge(node, neighbor)
                else:
                    self.visitor.cross_edge(node, neighbor)
        
        self.COLORS[node] = self.BLACK
        self.finish[node] = self.time
        self.time += 1
        self.visitor.post_process(node)



class TopoSortVisitor(TraversalVisitor):
    def __init__(self, topo_order: list):
        super().__init__()
        self.topo_order = topo_order
    
    def post_process(self, node):
        self.topo_order.append(node)

class CyclicGraphVisitor(TraversalVisitor):
    def __init__(self):
        super().__init__()
    
    def back_edge(self, node, neighbor):
        print("Cyclic Graph")
        raise CyclicGraphException("Cyclic Graph")

class CyclicGraphException(Exception):
    pass

class TopoSort(DFSTraversalTemplate):
    def __init__(self, graph: "Graph"):
        super().__init__(graph)
        self.topo_order = []
        self.set_visitor(CompositeVisitor([CyclicGraphVisitor(), TopoSortVisitor(self.topo_order)]))

    def run(self, start_node = None):
        self.initialize()
        self.dfs(start_node)
        return list(reversed(self.topo_order))


    

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

    traversals = {
        "dfs": DFSTraversalTemplate,
        "topo_sort": TopoSort,
    }
    graph = Graph()
    graph.nodes = {
        'A': ['B', 'C'],
        'B': ['A', 'D', 'E'],
        'C': ['A', 'F'],
        'D': ['B'],
        'E': ['B', 'F'],
        'F': ['C', 'E']
    }

    traversal = TraversalFactory(traversals, graph)
    traversal.set_traversal("dfs")
    dfs_result = traversal("A")
    print(dfs_result.discovery)
    print(dfs_result.finish)
    print(dfs_result.parents)

    dag = Graph()
    dag.nodes = {
        'A': ['B', 'C'],
        'B': ['D', 'E'],
        'C': ['F'],
        'D': [],
        'E': ['F'],
        'F': []
    }

    acyclic_graph_traversal = TraversalFactory(traversals, dag)
    acyclic_graph_traversal.set_traversal("topo_sort")
    topo_result = acyclic_graph_traversal("A")
    print(topo_result.topo_order)
    
    
    

    