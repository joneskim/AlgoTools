


class Graph:
    def __init__(self):
        self.nodes = {}

    def add_node(self, node):
        self.nodes[node] = []

    def add_edge(self, node1, node2):
        self.nodes[node1].append(node2)

class TraversalVisitor:
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


class CompositeVisitor(TraversalVisitor):
    def __init__(self, visitors=None):
        self.visitors = visitors or []

    def add(self, visitor: TraversalVisitor):
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


class TraversalFactory:
    def __init__(self, traversals: dict, graph: "Graph"):
        self.traversals = traversals
        self.graph = graph
        self.traversal = None

    def set_traversal(self, traversal: str):
        self.traversal = traversal
    
    def __call__(self, start_node=None):
        traversal_cls = self.traversals[self.traversal]
        traversal_obj = traversal_cls(self.graph)
        traversal_obj.run(start_node)
        return traversal_obj