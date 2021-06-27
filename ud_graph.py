# Course:       CS 261 - Data Structures
# Author:       Derek Hand
# Assignment:   Portfolio Project Part 1: Undirected Graph via Adjacency List
# Description:  An implementation of an undirected class by using an adjacency list


class UndirectedGraph:
    """
    Class to implement undirected graph
    - duplicate edges not allowed
    - loops not allowed
    - no edge weights
    - vertex names are strings
    """

    def __init__(self, start_edges=None):
        """
        Store graph info as adjacency list
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.adj_list = dict()

        # populate graph with initial vertices and edges (if provided)
        # before using, implement add_vertex() and add_edge() methods
        if start_edges is not None:
            for u, v in start_edges:
                self.add_edge(u, v)

    def __str__(self):
        """
        Return content of the graph in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = [f'{v}: {self.adj_list[v]}' for v in self.adj_list]
        out = '\n  '.join(out)
        if len(out) < 70:
            out = out.replace('\n  ', ', ')
            return f'GRAPH: {{{out}}}'
        return f'GRAPH: {{\n  {out}}}'

    # ------------------------------------------------------------------ #

    def add_vertex(self, v: str) -> None:
        """
        Description:    Adds a new vertex to the graph. If the vertex name already exists, the method does nothing
        Input(s):       v:  the vertex to add, it will be any sort of string
        Output(s):      None
        """

        if v not in self.adj_list:
            self.adj_list[v] = []
        
    def add_edge(self, u: str, v: str) -> None:
        """
        Description:    Adds a new edge to the graph. If either, or both of the vertices do not exist, adds a new
                        vertex.
        Input(s):       u:  a vertex to connect/add
                        v:  a vertex to connect/add
        Output(s):      None
        """

        if u == v:
            return

        if u not in self.adj_list:
            self.add_vertex(u)
        if v not in self.adj_list:
            self.add_vertex(v)

        if v in self.adj_list[u] and u in self.adj_list[v]:
            return

        else:
            self.adj_list[u].append(v)
            self.adj_list[v].append(u)

    def remove_edge(self, v: str, u: str) -> None:
        """
        Description:    Removes the edge between V and U. If either or both do not exist, or if there is not edge,
                        this does nothing.
        Input(s):       v:  an edge between this vertex and u to remove
                        u:  an edge between this vertex and v to remove
        Output(s):      None
        """

        if v not in self.adj_list or u not in self.adj_list:
            return

        if u in self.adj_list[v]:
            self.adj_list[v].remove(u)
        if v in self.adj_list[u]:
            self.adj_list[u].remove(v)

    def remove_vertex(self, v: str) -> None:
        """
        Description:    Removes the given vertex and all edges incident to it
        Input(s):       v:  the vertex to remove
        Output(s):      None
        """

        if v not in self.adj_list:
            return

        del self.adj_list[v]

        for i in self.adj_list:
            if v in self.adj_list[i]:
                self.adj_list[i].remove(v)

    def get_vertices(self) -> []:
        """
        Description:    Returns a list of vertices in the graph
        Input(s):       None
        Output(s):      vertices:   the list of vertices
        """

        vertices = []
        for i in self.adj_list:
            vertices.append(i)

        return vertices

    def get_edges(self) -> []:
        """
        Description:    Returns a list of edges in the graph. Each edge is returned as a tuple of two incident vertex
                        names
        Input(s):       None
        Output(s):      edges:  a list of edge tuples
        """

        edges = []

        keys = list(self.adj_list)

        for i in range(len(self.adj_list)):
            key_i = keys[i]
            for j in range(i + 1, len(self.adj_list)):
                key_j = keys[j]
                if key_i in self.adj_list[key_j]:
                    edges.append( (key_i, key_j))
        return edges

    def is_valid_path(self, path: []) -> bool:
        """
        Description:    Determines if the sequence of given vertices represent a valid path in the graph
        Input(s):       path:   a list of vertices to follow
        Output(s):      True:   if the given path is valid
                        False:  if the given path is invalid
        """

        if len(self.adj_list) == 0:
            return False

        if len(path) == 1:
            if path[0] not in self.adj_list:
                return False
            else:
                return True

        for i in range(len(path) - 1):
            if path[i] not in self.adj_list:
                return False
            if path[i+1] not in self.adj_list[path[i]]:
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

        visited= []

        if v_start not in self.adj_list:
            return visited

        if v_end != None and v_end not in self.adj_list:
            v_end = None

        for item in self.adj_list:
            self.adj_list[item].sort()

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

            for edge in self.adj_list[vertex]:
                exit = self.dfs_helper(visited, edge, v_end)
                if exit:
                    return True # need to exit recursion

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

        if v_start not in self.adj_list:
            return visited

        if v_end != None and v_end not in self.adj_list:
            v_end = None

        for item in self.adj_list:
            self.adj_list[item].sort()

        visited.append(v_start)
        queue.append(v_start)

        if v_end == v_start:
            return visited

        while queue:
            next = queue.pop(0)

            for vertex in self.adj_list[next]:
                if vertex not in visited:
                    visited.append(vertex)
                    queue.append(vertex)
                if vertex == v_end:
                    break

            if vertex == v_end:
                break

        return visited

    def count_connected_components(self):
        """
        Description:    Returns the number of connected components in the graph
        Input(s):       None
        Output(s):      connected:  the number of connected components
        """

        visited = []
        count = 0

        keys = list(self.adj_list)

        count_dict = dict()
        for i in range(len(keys)):
            count_dict[keys[i]] = False

        for i in range(len(keys)):
            if count_dict[keys[i]] is False:
                count += 1
                visited = self.dfs(keys[i])
                for j in visited:
                    if count_dict[j] is False:
                        count_dict[j] = True
        return count

    def has_cycle(self):
        """
        Description:    Determines if the graph has a cycle
        Input(s):       None
        Output(s):      True:   if the graph has a cycle
                        False:  if the graph does not have a cycle
        """

        keys = list(self.adj_list)

        for i in keys:
            if self.cycle_helper(i):
                return True

        return False

    def cycle_helper(self, vertex):
        """
        Description:    Does a breadth first search to determine if the given vertex has a cycle
        Input(s):       vertex: the current node to study
        Output(s):      True:   if cycle was found
                        False:  if cycle was not found
        """
        colors = {node: "red" for node in self.adj_list}    # mark unvisited nodes as red
        colors[vertex] = "black"        # visited

        visited = [(None, vertex)]      # we will store the edge as a list of tuples

        while visited:
            (prev, next) = visited.pop()
            for neighbor in self.adj_list[next]:
                if neighbor == prev:
                    pass    # don't go back the way we just came
                elif colors[neighbor] == "black":
                    return True     # found a cycle
                else:   # haven't visited, keep going
                    colors[neighbor] = "black"
                    visited.append( (next, neighbor) )

        return False    # no cycles here
        # this took forever to determine how to track the parent and not go from neighbor back to parent vertex

if __name__ == '__main__':

    print("\nPDF - method add_vertex() / add_edge example 1")
    print("----------------------------------------------")
    g = UndirectedGraph()
    print(g)

    for v in 'ABCDE':
        g.add_vertex(v)
    print(g)

    g.add_vertex('A')
    print(g)

    for u, v in ['AB', 'AC', 'BC', 'BD', 'CD', 'CE', 'DE', ('B', 'C')]:
        g.add_edge(u, v)
    print(g)

    print("\nPDF - method remove_edge() / remove_vertex example 1")
    print("----------------------------------------------------")
    g = UndirectedGraph(['AB', 'AC', 'BC', 'BD', 'CD', 'CE', 'DE'])
    g.remove_vertex('DOES NOT EXIST')
    g.remove_edge('A', 'B')
    g.remove_edge('X', 'B')
    print(g)
    g.remove_vertex('D')
    print(g)

    print("\nPDF - method get_vertices() / get_edges() example 1")
    print("---------------------------------------------------")
    g = UndirectedGraph()
    print(g.get_edges(), g.get_vertices(), sep='\n')
    g = UndirectedGraph(['AB', 'AC', 'BC', 'BD', 'CD', 'CE'])
    print(g.get_edges(), g.get_vertices(), sep='\n')

    print("\nPDF - method is_valid_path() example 1")
    print("--------------------------------------")
    g = UndirectedGraph(['AB', 'AC', 'BC', 'BD', 'CD', 'CE', 'DE'])
    test_cases = ['ABC', 'ADE', 'ECABDCBE', 'ACDECB', '', 'D', 'Z']
    for path in test_cases:
        print(list(path), g.is_valid_path(list(path)))

    print("\nPDF - method dfs() and bfs() example 1")
    print("--------------------------------------")
    edges = ['AE', 'AC', 'BE', 'CE', 'CD', 'CB', 'BD', 'ED', 'BH', 'QG', 'FG']
    g = UndirectedGraph(edges)
    test_cases = 'ABCDEGH'
    for case in test_cases:
        print(f'{case} DFS:{g.dfs(case)} BFS:{g.bfs(case)}')
    print('-----')
    for i in range(1, len(test_cases)):
        v1, v2 = test_cases[i], test_cases[-1 - i]
        print(f'{v1}-{v2} DFS:{g.dfs(v1, v2)} BFS:{g.bfs(v1, v2)}')

    print("\nPDF - method count_connected_components() example 1")
    print("---------------------------------------------------")
    edges = ['AE', 'AC', 'BE', 'CE', 'CD', 'CB', 'BD', 'ED', 'BH', 'QG', 'FG']
    g = UndirectedGraph(edges)
    test_cases = (
        'add QH', 'remove FG', 'remove GQ', 'remove HQ',
        'remove AE', 'remove CA', 'remove EB', 'remove CE', 'remove DE',
        'remove BC', 'add EA', 'add EF', 'add GQ', 'add AC', 'add DQ',
        'add EG', 'add QH', 'remove CD', 'remove BD', 'remove QG')
    for case in test_cases:
        command, edge = case.split()
        u, v = edge
        g.add_edge(u, v) if command == 'add' else g.remove_edge(u, v)
        print(g.count_connected_components(), end=' ')
    print()

    print("\nPDF - method has_cycle() example 1")
    print("----------------------------------")
    edges = ['AE', 'AC', 'BE', 'CE', 'CD', 'CB', 'BD', 'ED', 'BH', 'QG', 'FG']
    g = UndirectedGraph(edges)
    test_cases = (
        'add QH', 'remove FG', 'remove GQ', 'remove HQ',
        'remove AE', 'remove CA', 'remove EB', 'remove CE', 'remove DE',
        'remove BC', 'add EA', 'add EF', 'add GQ', 'add AC', 'add DQ',
        'add EG', 'add QH', 'remove CD', 'remove BD', 'remove QG',
        'add FG', 'remove GE')
    for case in test_cases:
        command, edge = case.split()
        u, v = edge
        g.add_edge(u, v) if command == 'add' else g.remove_edge(u, v)
        print('{:<10}'.format(case), g.has_cycle())
