#python 2.7
from __future__ import division

import pickle
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import networkx as nx
import math
from classes import *


with open('foreground.pkl', 'rb') as fp:
		foreground = pickle.load(fp)

with open('background.pkl', 'rb') as fp:
		background = pickle.load(fp)

lambda_val = 1 # what should lambda_val be ?
gamma_val = 1
sigma = 5

def get_intensities(ndarray_of_pixels):
	return [intensity[pixel] for pixel in ndarray_of_pixels]	

def add_nodes(G):
	G.add_node('S')
	G.add_node('T')
	for i in range(0, length):
		for j in range(0, breadth):
			nodes[i,j] = Node(i, j, img[i][j])
			G.add_node((i,j), val = img[i][j])

def get_neigbours((i, j)):
	neigbours = []
	for x in range(i-1, i+2):
		for y in range(j-1, j+2):
			if not(x == i and y == j) and x > min_x and x < max_x and y > min_x and y < max_x:
				neigbours.append((x,y))
	
	return neigbours

def square(x):
	return x*x

def squared_intensity_difference(node1, node2):
	return square(intensity[node1] - intensity[node2])

def distance(node1, node2):
	return math.sqrt(square(node1[0] - node2[0]) + square(node1[1] - node2[1]))

def get_boundary_cost(node1, node2):		
	return gamma_val*(math.exp(-1*(np.mean(squared_intensity_difference(node1, node2))/2*square(sigma)))/distance(node1, node2))

def pixel_nodes(G):
	return [node for node in sorted(G.nodes()) if node not in ['S', 'T']]
	
def add_neigbour_edges(G, max_neighbours_weight):
	max_neighbours_weight = 0
	for node in pixel_nodes(G):
		contender = 0
		for neigbour in get_neigbours(node):
			boundary_cost = get_boundary_cost(node, neigbour)
			G.add_edge(node, neigbour, weight = boundary_cost)
			contender += boundary_cost
		if contender > max_neighbours_weight:
			max_neighbours_weight = contender

def probability_of_background(node): #needs to be betterized
	return background.count(node)/len(background)
			
def probability_of_foreground(node): #needs to be betterized
	return foreground.count(node)/len(foreground)
			
def get_regional_foreground_cost(node): #needs to be betterized
	prob = probability_of_foreground(node)
	if prob == 0:
		prob = 1e-320
	return -1*(math.log(prob))

def get_regional_background_cost(node):
	prob = probability_of_background(node)
	if prob == 0:
		prob = 1e-320
	return -1*(math.log(prob))
	
def add_source_edges(G):
	for node in pixel_nodes(G):
		if node in foreground:
			G.add_edge('S', node, weight = ground_weight)
		elif node in background:
			G.add_edge('S', node, weight = 0)
		else:
			G.add_edge('S', node, weight = get_regional_foreground_cost(node))

def add_sink_edges(G):
	for node in pixel_nodes(G):
		if node in background:
			G.add_edge('T', node, weight = ground_weight)
		elif node in foreground:
			G.add_edge('T', node, weight = 0)
		else:
			G.add_edge('T', node, weight = get_regional_background_cost(node))
			
def add_edges(G, ground_weight, max_neighbours_weight):
	add_neigbour_edges(G, max_neighbours_weight)
	ground_weight = max_neighbours_weight + 1 #K
	add_source_edges(G)
	add_sink_edges(G)

def print_edges(G):
	for edge in G.edges(data=True):
		print edge, intensity[edge[0]]#, intensity[edge[1]], distance(edge[0],edge[1])
	
	
img = mpimg.imread('woman.jpg')
length, breadth = img.shape[0:2]
min_x = 0
min_y = 0
max_x = length
max_y = breadth
ground_weight = 0
max_neighbours_weight = 0
nodes = np.array([[Node(-1, -1,-1) for x in range(breadth)] for y in range(length)])

G = nx.Graph()

add_nodes(G)

intensity = nx.get_node_attributes(G,'val')
foreground_intensities = get_intensities(foreground)
background_intensities = get_intensities(background)

add_edges(G, ground_weight, max_neighbours_weight)	
print np.mean(intensity[sorted(G.nodes())[3]])


#print("fg and prob")
#for node in foreground:
#	print node, probability_of_foreground(node), foreground.count(node)