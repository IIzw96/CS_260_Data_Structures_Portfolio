# Course:       CS261 - Data Structures
# Author:       Derek Hand
# Assignment:   Portfolio Project Part 2: Directed Graph via Adjacency Matrix
# Description:  An implementation of a directed graph via an adjacency matrix

class DirectedGraph:
    """
    Class to implement directed weighted graph
    - duplicate edges not allowed
    - loops not allowed
    - only positive edge weights
    - vertex names are integers
    """

    def __init__(self, start_edges=None):
        """
        Store graph info as adjacency matrix
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.v_count = 0
        self.adj_matrix = []

        # populate graph with initial vertices and edges (if provided)
        # before using, implement add_vertex() and add_edge() methods
        if start_edges is not None:
            v_count = 0
            for u, v, _ in start_edges:
                v_count = max(v_count, u, v)
            for _ in range(v_count + 1):
                self.add_vertex()
            for u, v, weight in start_edges:
                self.add_edge(u, v, weight)

    def __str__(self):
        """
        Return content of the graph in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if self.v_count == 0:
            return 'EMPTY GRAPH\n'
        out = '   |'
        out += ' '.join(['{:2}'.format(i) for i in range(self.v_count)]) + '\n'
        out += '-' * (self.v_count * 3 + 3) + '\n'
        for i in range(self.v_count):
            row = self.adj_matrix[i]
            out += '{:2} |'.format(i)
            out += ' '.join(['{:2}'.format(w) for w in row]) + '\n'
        out = f"GRAPH ({self.v_count} vertices):\n{out}"
        return out

    # ------------------------------------------------------------------ #

    def add_vertex(self) -> int:
        """
        Description:    Adds a vertex into the adjacency matrix
        Input(s):       None
        Output(s):      num:    the number of vertices in the graph after the vertex was added
        """

        if not self.adj_matrix:
            self.adj_matrix.append([0])

        else:
            self.adj_matrix[0].append(0)
            self.adj_matrix.append([0])
            for i in range(1, len(self.adj_matrix[0])):
                self.adj_matrix[i] = [0] * len(self.adj_matrix[0])

        self.v_count += 1

        return self.v_count

    def add_edge(self, src: int, dst: int, weight=1) -> None:
        """
        Description:    Adds an edge and a weight
        Input(s):       src:    The source
                        dst:    The destination
        Output(s):      None
        """

        if src == dst or weight < 0:
            return

        if src >= self.v_count or dst >= self.v_count:
            return

        self.adj_matrix[src][dst] = weight

    def remove_edge(self, src: int, dst: int) -> None:
        """
        Description:    Removes the edge at the given location
        Input(s):       src:    The source
                        dst:    The destination
        Output(s):      None
        """

        if src == dst or src >= self.v_count or dst >= self.v_count or src < 0 or dst < 0:
            return

        self.adj_matrix[src][dst] = 0


    def get_vertices(self) -> []:
        """
        Description:    Returns a list of the vertices in the graph
        Input(s):       None
        Output(s):      a list of all vertices
        """

        if not self.adj_matrix:
            return []

        vertices = []
        for i in range(self.v_count):
            vertices.append(i)
        return vertices

    def get_edges(self) -> []:
        """
        Description:    Returns a list of edges in the graph. Each edge is returned as a tuple with the src, dst, and
                        weight
        Input(s):       None
        Output(s):      edges:  [(src, dst, weight)]
        """

        if not self.adj_matrix:
            return []

        edges = []

        for i in range(self.v_count):
            for j in range(self.v_count):
                if self.adj_matrix[i][j] != 0:
                    edges.append((i, j, self.adj_matrix[i][j]))

        return edges

    def is_valid_path(self, path: []) -> bool:
        """
        Description:    Determines if the sequence of given vertices represent a valid path in the graph
        Input(s):       path:   a list of vertices to follow
        Output(s):      True:   if the given path is valid
                        False:  if the given path is invalid
        """

        if not self.adj_matrix:
            return False

        if len(path) == 1:
            if path[0] >= 0 and path[0] < self.v_count:
                return True
            else:
                return False

        for i in range(len(path) - 1):
            if self.adj_matrix[path[i]][path[i+1]] == 0:
                return False

        return True

    def dfs(self, v_start, v_end=None) -> []:
        """
        Description:    Performs a depth first search in the graph and returns a list of the vertices visited, in the
                        order that they were visited
        Input(s):       v_start:    Where to start the search
                        v_end:      Where to end the search if it is provided and is a valid vertex
        Output(s):      visited:    a list of the vertices that were visited
        """

        visited = []

        if not self.adj_matrix:
            return visited

        if v_start >= self.v_count or v_start < 0:
            return visited

        if v_end != None:
            if v_end >= self.v_count or v_end < 0:
                v_end = None

        self.dfs_helper(visited, v_start, v_end)

        return visited

    def dfs_helper(self, visited, vertex, v_end):
        """
        Description:    A helper function to traverse the graph recursively
        Input(s):       visited:    to keep track of what we have visited
                        vertex:     to keep track of what vertex to check for
                        v_end:      where do we end
        Output(s):      None
        """

        if vertex not in visited:
            visited.append(vertex)
            if v_end != None and vertex == v_end:
                return True
            if len(visited) == self.v_count:
                return True

            for i in range(self.v_count):
                if self.adj_matrix[vertex][i] != 0:
                    exit = self.dfs_helper(visited, i, v_end)
                    if exit:
                        return True

    def bfs(self, v_start, v_end=None) -> []:
        """
        Description:    Performs a breadth first search in the graph and returns a list of indices visited, in the
                        order that they were visited
        Input(s):       v_start:    where to start the breadth first search
                        v_end:      if provide and valid, where to end the search
        Output(s):      visited:    the vertices visited, in the order that they were visited
        """

        visited = []
        queue = []

        if v_start < 0 or v_start >= self.v_count:
            return visited

        if v_end != None:
            if v_end >= self.v_count or v_end < 0:
                v_end = None

        visited.append(v_start)
        queue.append(v_start)

        while queue:
            next = queue.pop(0)

            for i in range(self.v_count):
                if i not in visited and self.adj_matrix[next][i] != 0:
                    visited.append(i)
                    queue.append(i)

                if i == v_end:
                    break

            if i == v_end:
                break

        return visited

    def has_cycle(self):
        """
        Description:    Determines if the graph has a cycle
        Input(s):       None
        Output(s):      True:   if the graph has a cycle
                        False:  if the graph does not have a cycle
        """

        if not self.adj_matrix:
            return False

        visited = [False] * self.v_count
        recursion = [False] * self.v_count

        for i in range(self.v_count):
            if visited[i] is False:
                if self.cycle_helper(i, visited, recursion):
                    return True

        return False

    def cycle_helper(self, vertex, visited, recursion):
        """
        Description:    Does a depth first search to determine if the given vertex has a cycle
        Input(s):       vertex:     the current node to study
                        visited:    a list of the visited vertices
                        recursion:  a list of the values visited in the recursion function
        Output(s):      True:       if cycle was found
                        False:      if cycle was not found
        """

        visited[vertex] = True
        recursion[vertex] = True

        for j in range(self.v_count):
            if visited[j] is False and self.adj_matrix[vertex][j] != 0:
                if self.cycle_helper(j, visited, recursion):
                    return True
            elif recursion[j] is True and self.adj_matrix[vertex][j] != 0:
               return True

        recursion[vertex] = False
        return False



    def dijkstra(self, src: int) -> []:
        """
        Description:    Uses Dijkstra's algorithm to determine the shortest path from the given vertex to all other
                        vertices
        Input(s):       src:    the given vertex
        Output(s):      dist:   a list of distances from the given vertex to all other vertices
        """

        distances = [float('inf') for _ in range(self.v_count)]     # initialize all distances to inf
        visited = [False for _ in range(self.v_count)]          # we have not visited any node

        distances[src] = 0  # distance from start to itself is 0

        while True: # go through all nodes

            shortest = float('inf') # we have not traversed anything yet, set to default
            shortest_id = -666      # the number of the beast, i.e a flag

            for i in range(self.v_count):   # go through and all indices in visited/distances and update shortest path
                if distances[i] < shortest and not visited[i]:
                    shortest = distances[i]
                    shortest_id = i

            if shortest_id == -666: # all node have been visited
                return distances

            for i in range(self.v_count):
                if self.adj_matrix[shortest_id][i] != 0 and distances[i] > distances[shortest_id] \
                        + self.adj_matrix[shortest_id][i]:
                    distances[i] = distances[shortest_id] + self.adj_matrix[shortest_id][i]

            visited[shortest_id] = True


if __name__ == '__main__':

    print("\nPDF - method add_vertex() / add_edge example 1")
    print("----------------------------------------------")
    g = DirectedGraph()
    print(g)
    for _ in range(5):
        g.add_vertex()
    print(g)

    edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
             (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    for src, dst, weight in edges:
        g.add_edge(src, dst, weight)
    print(g)


    print("\nPDF - method get_edges() example 1")
    print("----------------------------------")
    g = DirectedGraph()
    print(g.get_edges(), g.get_vertices(), sep='\n')
    edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
             (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    g = DirectedGraph(edges)
    print(g.get_edges(), g.get_vertices(), sep='\n')


    print("\nPDF - method is_valid_path() example 1")
    print("--------------------------------------")
    edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
             (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    g = DirectedGraph(edges)
    test_cases = [[0, 1, 4, 3], [1, 3, 2, 1], [0, 4], [4, 0], [], [2]]
    for path in test_cases:
        print(path, g.is_valid_path(path))


    print("\nPDF - method dfs() and bfs() example 1")
    print("--------------------------------------")
    edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
             (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    g = DirectedGraph(edges)
    for start in range(5):
        print(f'{start} DFS:{g.dfs(start)} BFS:{g.bfs(start)}')


    print("\nPDF - method has_cycle() example 1")
    print("----------------------------------")
    edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
             (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    g = DirectedGraph(edges)

    edges_to_remove = [(3, 1), (4, 0), (3, 2)]
    for src, dst in edges_to_remove:
        g.remove_edge(src, dst)
        print(g.get_edges(), g.has_cycle(), sep='\n')

    edges_to_add = [(4, 3), (2, 3), (1, 3), (4, 0)]
    for src, dst in edges_to_add:
        g.add_edge(src, dst)
        print(g.get_edges(), g.has_cycle(), sep='\n')
    print('\n', g)

    print("\nPDF - dijkstra() example 1")
    print("--------------------------")
    edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
             (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    g = DirectedGraph(edges)
    for i in range(5):
        print(f'DIJKSTRA {i} {g.dijkstra(i)}')
    g.remove_edge(4, 3)
    print('\n', g)
    for i in range(5):
        print(f'DIJKSTRA {i} {g.dijkstra(i)}')