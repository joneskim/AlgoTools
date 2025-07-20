from graph import Graph

class Dijkstra:
    def __init__(self, graph: "Graph"):
        pass
    
class BellmanFord:
    def __init__(self, graph: "Graph"):
        self.graph = graph
        self.dist = {}
        self.parents = {}

    
    def relax(self, u, v, weight):
        if self.dist[v] > self.dist[u] + weight:
            self.dist[v] = self.dist[u] + weight
            self.parents[v] = u

    def initialize_single_source(self, start):
        for node in self.graph.nodes:
            self.dist[node] = float('inf')
            self.parents[node] = None
        self.dist[start] = 0

    def run(self, start):
        self.initialize_single_source(start)
        for _ in range(len(self.graph.nodes) - 1):
            for u in self.graph.nodes:
                for v, weight in self.graph.nodes[u].items():
                    self.relax(u, v, weight)
        
        for u in self.graph.nodes:
            for v, weight in self.graph.nodes[u].items():
                if self.dist[v] > self.dist[u] + weight:
                    return False
        return True

    def get_shortest_path(self, start, end):
        path = []
        curr = end
        while curr != start:
            path.append(curr)
            curr = self.parents[curr]
        path.append(start)
        return path[::-1]

                    
if __name__ == "__main__":
    graph = Graph()
    graph.nodes = {
        'A': {'B': 1, 'C': 4},
        'B': {'A': 1, 'D': 2, 'E': 5},
        'C': {'A': 4, 'F': 11},
        'D': {'B': 2},
        'E': {'B': 5, 'F': 1},
        'F': {'C': 11, 'E': 1}
    }
    bellman_ford = BellmanFord(graph)
    print(bellman_ford.run('A'))
    print(bellman_ford.dist)
    print(bellman_ford.parents)
    print(bellman_ford.get_shortest_path('A', 'F'))

        
        
        
            