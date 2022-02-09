import math

points = [[4,1], [4,2], [4,3], 
          [3,1], [3,2], [3,3], 
          [2,1], [2,2], [2,3], 
          [1,1], [1,2], [1,3]]

def distance(point1, point2):
    return math.sqrt(((point2[0] - point1[0])**2) + ((point2[1] - point1[1])**2))

def k_neighbors(i, points, k):
    """
    i: index of a point
    points: list of points
    k: number of neighbors
    """
    distancias_point_i = []
    point_i = points[i]
    size = len(points)
    j = 0
    while j < size:
        point_j = points[j]
        distancias_point_i.append([distance(point_i, point_j), j])
        j += 1
    distancias_point_i.sort()
    #print(distancias_point_i)
    result = []
    for m in range(len(distancias_point_i)):
        result.append(distancias_point_i[m][1])
    return result[1:k+1]

#print(distance([1,2], [3,4]))
print(k_neighbors(3, points, 5))

class Graph():
    def __init__(self):
        self.V = []
        self.E = []

    def add_vertex(self, info):
        self.V.append(info)
        self.E.append([])

    def add_edge(self, start, finish):
        self.E[start].append(finish)

    def get_vertex(self, i):
        return self.V[i]

    def get_neighbors(self, info, k):
        return k_neighbors(info, points, k)

    def print(self):
        print(self.V)
        print(self.E)


""" graph1 = Graph()
graph1.add_vertex(0)
graph1.add_vertex(1)
graph1.add_vertex(2)
graph1.add_vertex(3)
graph1.add_vertex(4)
graph1.add_vertex(5)
graph1.add_vertex(6)
graph1.add_vertex(7)
graph1.add_edge(1, 2)
graph1.add_edge(2, 4)
graph1.add_edge(3, 1)
graph1.add_edge(3, 4)
graph1.add_edge(4, 5)
graph1.add_edge(4, 7)
graph1.add_edge(6, 7)
graph1.add_edge(5, 6)
graph1.print() """

def create_nn_graph(points, k):
    nn_graph = Graph()
    j = 0
    size = len(points)
    while j < size:
        nn_graph.add_vertex(points[j])
        neighbors = k_neighbors(j, points, k)
        for n in range(len(neighbors)):
            nn_graph.add_edge(j, neighbors[n])
        j += 1
    return nn_graph

graph = create_nn_graph(points, 3)
graph.print()





