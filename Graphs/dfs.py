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


class DFSVisitor:
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
        self.visitor = DFSVisitor()

    def set_visitor(self, visitor: "DFSVisitor"):
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

class CompositeVisitor(DFSVisitor):
    def __init__(self, visitors=None):
        self.visitors = visitors or []

    def add(self, visitor: DFSVisitor):
        self.visitors.append(visitor)

    def pre_process(self, node):
        for v in self.visitors:
            v.pre_process(node)

    def post_process(self, node):
        for v in self.visitors:
            v.post_process(node)

    def back_edge(self, node, neighbor):
        for v in self.visitors:
            v.back_edge(node, neighbor)

    def forward_edge(self, node, neighbor):
        for v in self.visitors:
            v.forward_edge(node, neighbor)

    def cross_edge(self, node, neighbor):
        for v in self.visitors:
            v.cross_edge(node, neighbor)


class TopoSortVisitor(DFSVisitor):
    def __init__(self, topo_order: list):
        super().__init__()
        self.topo_order = topo_order
    
    def post_process(self, node):
        self.topo_order.append(node)

class CyclicGraphVisitor(DFSVisitor):
    def __init__(self):
        super().__init__()
    
    def back_edge(self, node, neighbor):
        print("Cyclic Graph")
        # raise CyclicGraphException("Cyclic Graph")

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
        return self.topo_order

class TraversalFactory:
    def __init__(self, traversal: str, graph: "Graph"):
        self.traversals = {
            "dfs": DFSTraversalTemplate,
            "topo_sort": TopoSort
        }
        self.graph = graph
        self.traversal = traversal
    
    def __call__(self):
        return self.traversals[self.traversal](self.graph)
    


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

    traversal = TraversalFactory("dfs", graph)()


    topo_sort = TraversalFactory("topo_sort", graph)()
    try:
        topo_sort.run('A')
    except CyclicGraphException as e:
        print(e)
    except Exception as e:
        print(e)
    print(topo_sort.topo_order)

    