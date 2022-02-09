data_path = "data/"

# -*- coding: utf-8 -*-
"""Copy of stippling.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1NfkjBcOh10wbMMkMfESTztWjwZkc9vX2

# Stippling Application

The PyTSPArt repo is cloned in order to access the adapted code for the stippling algorithm.
"""

#!git clone https://github.com/RoboTums/PyTSPArt.git
#!mv PyTSPArt/code/voronoi.py 

"""The base image is asked for to the user."""

#from google.colab import files
#uploaded = files.upload()

"""The following snippet of code shows the image uploaded."""

#from IPython.display import Image
#Image(filename=list(uploaded.keys())[0])

"""Stippling algorithm, recieves a base image and parameters such as, number of points and number of iterations, in order to process the image given."""

# This code was adapted from: https://github.com/RoboTums/PyTSPArt/blob/master/code/stippler.py
#! /usr/bin/env python3
# -----------------------------------------------------------------------------
# Weighted Voronoi Stippler
# Copyright (2017) Nicolas P. Rougier - BSD license
#
# Implementation of:
#   Weighted Voronoi Stippling, Adrian Secord
#   Symposium on Non-Photorealistic Animation and Rendering (NPAR), 2002
# -----------------------------------------------------------------------------
# Some usage examples
#
# stippler.py boots.jpg --save --force --n_point 20000 --n_iter 50
#                       --pointsize 0.5 2.5 --figsize 8 --interactive
# stippler.py plant.png --save --force --n_point 20000 --n_iter 50
#                       --pointsize 0.5 1.5 --figsize 8
# stippler.py gradient.png --save --force --n_point 5000 --n_iter 50
#                          --pointsize 1.0 1.0 --figsize 6
# -----------------------------------------------------------------------------
# usage: stippler.py [-h] [--n_iter n] [--n_point n] [--epsilon n]
#                    [--pointsize min,max) (min,max] [--figsize w,h] [--force]
#                    [--save] [--display] [--interactive]
#                    image filename
#
# Weighted Vororonoi Stippler
#
# positional arguments:
#   image filename        Density image filename
#
# optional arguments:
#   -h, --help            show this help message and exit
#   --n_iter n            Maximum number of iterations
#   --n_point n           Number of points
#   --epsilon n           Early stop criterion
#   --pointsize (min,max) (min,max)
#                         Point mix/max size for final display
#   --figsize w,h         Figure size
#   --force               Force recomputation
#   --save                Save computed points
#   --display             Display final result
#   --interactive         Display intermediate results (slower)
# -----------------------------------------------------------------------------
import tqdm
from repo.PyTSPArt.code import voronoi
import os.path
import scipy.misc
import scipy.ndimage
import numpy as np
import imageio
import matplotlib.pyplot as plt

def normalize(D):
    Vmin, Vmax = D.min(), D.max()
    if Vmax - Vmin > 1e-5:
        D = (D-Vmin)/(Vmax-Vmin)
    else:
        D = np.zeros_like(D)
    return D


def initialization(n, D):
    """
    Return n points distributed over [xmin, xmax] x [ymin, ymax]
    according to (normalized) density distribution.
    with xmin, xmax = 0, density.shape[1]
         ymin, ymax = 0, density.shape[0]
    The algorithm here is a simple rejection sampling.
    """

    samples = []
    while len(samples) < n:
        # X = np.random.randint(0, D.shape[1], 10*n)
        # Y = np.random.randint(0, D.shape[0], 10*n)
        X = np.random.uniform(0, D.shape[1], 10*n)
        Y = np.random.uniform(0, D.shape[0], 10*n)
        P = np.random.uniform(0, 1, 10*n)
        index = 0
        while index < len(X) and len(samples) < n:
            x, y = X[index], Y[index]
            x_, y_ = int(np.floor(x)), int(np.floor(y))
            if P[index] < D[y_, x_]:
                samples.append([x, y])
            index += 1
    return np.array(samples)

def stippler(filename,
            n_point = 5000,
            n_iter = 50,
            threshold = 255,
            force = False,
            save = False,
            display = False,
            interactive = False):

    density = imageio.imread(filename, as_gray=True, pilmode='L')

    # We want (approximately) 500 pixels per voronoi region
    zoom = (n_point * 500) / (density.shape[0]*density.shape[1])
    zoom = int(round(np.sqrt(zoom)))
    density = scipy.ndimage.zoom(density, zoom, order=0)
    # Apply threshold onto image
    # Any color > threshold will be white
    density = np.minimum(density, threshold)

    density = 1.0 - normalize(density)
    density = density[::-1, :]
    density_P = density.cumsum(axis=1)
    density_Q = density_P.cumsum(axis=1)

    dirname = os.path.dirname(filename)
    basename = (os.path.basename(filename).split('.'))[0]
    pdf_filename = os.path.join(dirname, basename + "_stipple.pdf")
    png_filename = os.path.join(dirname, basename + "_stipple.png")
    dat_filename = os.path.join(dirname, basename + "_stipple.npy")

    # Initialization
    points = initialization(n_point, density)
    print("Nb points:", n_point)
    print("Nb iterations:", n_iter)

    print("Density file: %s (resized to %dx%d)" % (
          filename, density.shape[1], density.shape[0]))

    for i in tqdm.trange(n_iter):
        regions, points = voronoi.centroids(points, density, density_P, density_Q)
       
    return points, density

    # Plot voronoi regions if you want
    # for region in vor.filtered_regions:
    #     vertices = vor.vertices[region, :]
    #     ax.plot(vertices[:, 0], vertices[:, 1], linewidth=.5, color='.5' )

#points, density = stippler(list(uploaded.keys())[0], n_point=1000)

"""Converts the result of the stippler algorithm to a list of points."""

#points1 = points.tolist()
#points1

class ImagePoints:
    def __init__(self, point_list):
        '''
        point_list: list of points returned by the stippler algorithm
        '''
        self.point_list = point_list

    def read_list(self):
        '''
        Returns:
        The complete list of points
        '''
        return self.point_list

    def read(self, i):
        '''
        i: index of the point to read
        Returns:
        The point in position i
        '''
        return self.point_list[i]
    
    def update(self, point, i):
        '''
        point: given point
        i: index of the point to read
        Returns:
        Updates the point in position i
        '''
        self.point_list[i] = point
    
    def insert(self, point):
        '''
        point: a given point
        Returns:
        Inserts a given point at the back of the list
        '''
        self.point_list.append(point)

    def num_points(self):
        '''
        Returns:
        The number of elements in the list
        '''
        return len(self.point_list)

    def delete(self, i):
        '''
        i: index of the point to read
        Returns:
        Deletes the point in position i
        '''
        self.point_list.pop(i)

    def visualize(self, density, pointsize = (1.0, 1.0), figsize = 6):
        '''
        Density: density of the points in the image
        Pointsize: size of the points that will conform the processed image
        Figsize: size of the processed image
        Returns:
        A visual representation of the processed base image
        '''
        # Visualize points
        xmin, xmax = 0, density.shape[1]
        ymin, ymax = 0, density.shape[0]
        bbox = np.array([xmin, xmax, ymin, ymax])
        ratio = (xmax-xmin)/(ymax-ymin)
        
        fig = plt.figure(figsize=(figsize, figsize/ratio),
                        facecolor="white")
        ax = fig.add_axes([0, 0, 1, 1], frameon=False)
        ax.set_xlim([xmin, xmax])
        ax.set_xticks([])
        ax.set_ylim([ymin, ymax])
        ax.set_yticks([])
        points = np.array(self.point_list)
        scatter = ax.scatter(points[:, 0], points[:, 1], s=1, 
                            facecolor="k", edgecolor="None")
        Pi = points.astype(int)
        X = np.maximum(np.minimum(Pi[:, 0], density.shape[1]-1), 0)
        Y = np.maximum(np.minimum(Pi[:, 1], density.shape[0]-1), 0)
        sizes = (pointsize[0] +
                (pointsize[1]-pointsize[0])*density[Y, X])
        scatter.set_offsets(points)
        scatter.set_sizes(sizes)

        plt.show()

# Image1 = ImagePoints(points1)
# print(Image1.read(2))
# Image1.delete(2)
# print(Image1.read(2))
# print(Image1.num_points())
# Image1.insert([0, 1])
# print(Image1.num_points())
# #Image1.delete(4998)
# print(Image1.num_points())

"""Visualization of the points returned by the algorithm within the density parameters givien."""

#Image1.visualize(density)

"""Function to create nodes and nearest neighbors"""

import math

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
#print(k_neighbors(3, points, 5))

class Graph():
    def __init__(self, points):
        self.V = []
        self.E = []
        self.points = points

    def add_vertex(self, info):
        self.V.append(info)
        self.E.append([])

    def add_edge(self, start, finish):
        self.E[start].append(finish)

    def get_vertex(self, i):
        return self.V[i]

    def get_neighbors(self, info, k):
        return k_neighbors(info, self.points, k)

    def num_vertices(self):
        return len(self.V)

    def num_edges(self):
        return len(self.E)

    def print(self):
        print(self.V)
        print(self.E)

def create_nn_graph(points, k):
    nn_graph = Graph(points)
    j = 0
    size = len(points)
    while j < size:
        nn_graph.add_vertex(points[j])
        neighbors = k_neighbors(j, points, k)
        for n in range(len(neighbors)):
            nn_graph.add_edge(j, neighbors[n])
        j += 1
    return nn_graph

#graph = create_nn_graph(points, 3)


def create_graph(edgelist):
    graph = {}
    for e1, e2 in edgelist:
        graph.setdefault(e1, []).append(e2)
        graph.setdefault(e2, []).append(e1)
    return graph

def mst(start, graph):
    closed = set()
    edges = []
    q = [(start, start)]
    while q:
        v1, v2 = q.pop()
        if v2 in closed:
            continue
        closed.add(v2)
        edges.append((v1, v2))
        for v in graph[v2]:
            if v in graph:
                q.append((v2, v))
    del edges[0]
    assert len(edges) == len(graph)-1
    return edges

#min_graph = create_graph(mst(0, {v: k for v, k in enumerate(graph.E)}))
#min_graph

import networkx as nx
import matplotlib.pyplot as plt

#graph = create_nn_graph(points1, 5)
#pos1 = {}
#print(graph.E)

#def nx_graph():

G = nx.Graph()

def add_edges_nx(graph):
    i = 0
    while i < graph.num_vertices():
        j = 0
        while j < len(graph.E[i]):
            G.add_edge(i, graph.E[i][j])
            j += 1
        i += 1

# explicitly set positions
def vertex_dictionary(graph):
    pos1 = {}
    i = 0
    while i < graph.num_vertices(): 
        pos1[i] = graph.get_vertex(i)
        i += 1
    return pos1

# vertex_dictionary(graph)
# add_edges_nx(graph)

# options = {
#     "font_size": 0,
#     "node_size": 15,
#     "node_color": "black",
#     "edgecolors": "black",
#     "linewidths": 1,
#     "width": 1,
# }
# nx.draw_networkx(G, pos1, **options)

# Set margins for the axes so that nodes aren't clipped
# ax = plt.gca()
# ax.margins(0.20)
# plt.axis("off")
# plt.show()

def main(file_name, points, iterations, k):
    points, density = stippler("data/" + file_name, n_point=points, n_iter=iterations) 
    points1 = points.tolist()
    graph = create_nn_graph(points1, k)
    vertex_dictionary(graph)
    add_edges_nx(graph)

    options = {
    "font_size": 0,
    "node_size": 15,
    "node_color": "black",
    "edgecolors": "black",
    "linewidths": 1,
    "width": 1,
    }
    nx.draw_networkx(G, vertex_dictionary(graph), **options)

    ax = plt.gca()
    ax.margins(0.20)
    plt.axis("off")
    # plt.show()

    plt.savefig("data/output-" + file_name)

# main("penguin.jpeg", 1000, 50, 3)