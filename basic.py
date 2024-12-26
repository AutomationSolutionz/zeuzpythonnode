class Graph:
    def __init__(self):
        self.graph = {}

    # Add edge to the graph
    def add_edge(self, node, neighbor):
        if node not in self.graph:
            self.graph[node] = []
        self.graph[node].append(neighbor)

    # Recursive DFS function
    def dfs_util(self, node, visited):
        # Mark the current node as visited and print it
        visited.add(node)
        print(node, end=' ')

        # Recur for all the neighbors of this node
        for neighbor in self.graph[node]:
            if neighbor not in visited:
                self.dfs_util(neighbor, visited)

    # DFS function
    def dfs(self, start_node):
        # Create a set to store visited nodes
        visited = set()
        # Call the recursive helper function to start DFS traversal
        self.dfs_util(start_node, visited)


# Create a graph and add edges
g = Graph()
g.add_edge('A', 'B')
g.add_edge('A', 'C')
g.add_edge('B', 'D')
g.add_edge('B', 'E')
g.add_edge('C', 'F')
g.add_edge('C', 'G')

# Perform DFS traversal
print("Depth-First Search starting from node A:")
g.dfs('A')
