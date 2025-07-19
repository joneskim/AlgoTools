from graph import Graph, TraversalVisitor, TraversalFactory
from collections import deque


class BFSTraversalTemplate:
    WHITE = 0
    GRAY = 1
    BLACK = 2

    def __init__(self, graph: "Graph"):
        self.graph = graph
        self.COLORS = {}
        self.discovery = {}
        self.finish = {}
        self.parents = {}
        self.dist = {}
        self.time = 0
        self.visitor = TraversalVisitor()

    def initialize(self):
        self.COLORS = {node: self.WHITE for node in self.graph.nodes}
        self.discovery = {node: None for node in self.graph.nodes}
        self.finish = {node: None for node in self.graph.nodes}
        self.parents = {node: None for node in self.graph.nodes}
        self.dist = {node: None for node in self.graph.nodes}
        self.time = 0
    
    def run(self, start_node = None):
        self.initialize()
        self.bfs(start_node)
        return self.discovery, self.finish, self.parents, self.dist
        

    def bfs(self, node):
        queue = deque([node])
        self.COLORS[node] = self.GRAY
        self.discovery[node] = self.time
        self.time += 1
        self.dist[node] = 0

        self.visitor.pre_process(node)
        
        while queue:
            curr = queue.popleft()
            self.COLORS[curr] = self.GRAY
            self.discovery[curr] = self.time
            self.time += 1
            
            for neighbor in self.graph.nodes[curr]:
                if self.COLORS[neighbor] == self.WHITE:
                    self.parents[neighbor] = curr
                    self.dist[neighbor] = self.dist[curr] + 1
                    queue.append(neighbor)

            self.COLORS[curr] = self.BLACK
            self.finish[curr] = self.time
            self.time += 1
            self.visitor.post_process(curr)

    def set_visitor(self, visitor: "TraversalVisitor"):
        self.visitor = visitor

            
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
    
    # traversal = BFSTraversalTemplate(graph)
    # traversal.run('A')
    # print("parents: ", traversal.parents)
    # print("dist: ", traversal.dist)
    # print("discovery: ", traversal.discovery)
    # print("finish: ", traversal.finish)

    traversals = {
        "bfs": BFSTraversalTemplate,
    }
    traversal = TraversalFactory(traversals, graph)
    traversal.set_traversal("bfs")
    bfs_result = traversal("A")
    print(bfs_result.discovery)
    print(bfs_result.finish)
    print(bfs_result.parents)
    
    
        
        
