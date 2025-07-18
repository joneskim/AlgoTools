from abc import ABC, abstractmethod

class GraphTraversalStrategy(ABC):
    @abstractmethod
    def traverse(self, graph, start_node = None):
        pass

class Graph:
    def __init__(self, strategy: GraphTraversalStrategy):
        self.strategy = strategy
        self.nodes = {}

    def traverse(self, start_node = None):
        return self.strategy.traverse(self, start_node)

    def set_strategy(self, strategy: GraphTraversalStrategy):
        self.strategy = strategy




class BFS(GraphTraversalStrategy):
    def traverse(self, graph, start_node = None):

        if start_node is None:
            start_node = list(graph.nodes.keys())[0]
        
        time = 0
        queue = [start_node]
        visited = set()
        dist = {start_node: 0}
        discovery = {start_node: time}
        finish = {start_node: time}
        parents = {start_node: None}
        
        
        while queue:
            curr = queue.pop(0)

            
            if curr in visited:
                continue

            time += 1

            visited.add(curr)
            dist[curr] = time
            discovery[curr] = time
            
            for neighbor in graph.nodes[curr]:
                queue.append(neighbor)
                parents[neighbor] = curr

            time += 1
            finish[curr] = time

        return dist, discovery, finish, parents

        

class DFS(GraphTraversalStrategy):
    def traverse(self, graph, start_node = None):
        if start_node is None:
            start_node = list(graph.nodes.keys())[0]

        time = 0
        stack = [start_node]
        visited = set()
        dist = {start_node: 0}
        discovery = {start_node: time}
        finish = {start_node: time}
        parents = {start_node: None}

        while stack:
            curr = stack.pop()


            if curr in visited:
                continue

            time += 1

            visited.add(curr)
            dist[curr] = time
            discovery[curr] = time
            
            for neighbor in graph.nodes[curr]:
                parents[neighbor] = curr
                stack.append(neighbor)

            time += 1
            finish[curr] = time

        return dist, discovery, finish, parents
        


class TopoSort(GraphTraversalStrategy):
    def traverse(self, graph, start_node = None):
        pass

class Dijkstra(GraphTraversalStrategy):
    def traverse(self, graph, start_node = None):
        pass

class BellmanFord(GraphTraversalStrategy):
    def traverse(self, graph, start_node = None):
        pass

class Prim(GraphTraversalStrategy):
    def traverse(self, graph, start_node = None):
        pass
    
class Kruskal(GraphTraversalStrategy):
    def traverse(self, graph, start_node = None):
        pass
    

if __name__ == "__main__":
    graph = Graph(BFS())
    graph.nodes = {
        'A': ['B', 'C'],
        'B': ['A', 'D', 'E'],
        'C': ['A', 'F'],
        'D': ['B'],
        'E': ['B', 'F'],
        'F': ['C', 'E']
    }
    
    dist, discovery, finish, parents = graph.traverse('A')
    print(parents)
