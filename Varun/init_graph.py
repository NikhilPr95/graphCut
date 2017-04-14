#python 2.7
from __future__ import division

import pickle
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import networkx as nx
import math
from classes import *

with open('foreground_assigned.pkl', 'rb') as fp:
		foreground = pickle.load(fp)

with open('background_assigned.pkl', 'rb') as fp:
		background = pickle.load(fp)

with open('img.pkl', 'rb') as fp:
		img = pickle.load(fp)
		

def get_intensities(ndarray_of_pixels, intensity):
	return [intensity[pixel] for pixel in ndarray_of_pixels]	

def get_neigbours((i, j), length, breadth):
	min_x, min_y, max_x, max_y = 0, 0, length, breadth
	neigbours = []
	for x in range(i-1, i+2):
		for y in range(j-1, j+2):
			if not(x == i and y == j) and x > min_x and x < max_x and y > min_x and y < max_x:
				neigbours.append((x,y))
	
	return neigbours

def square(x):
	return x*x

def squared_diff(li, val):
	return [(x - val) ** 2 for x in li]
	
def gaussian_function(li, intensity):
	intensities =  get_intensities(li, intensity)	
	mean = np.sum(intensities, axis=0)/len(intensities)
	variance = np.sum(squared_diff(intensities, mean))/len(intensities)
	return mean, variance

def pixel_nodes(G):
	return [node for node in sorted(G.nodes()) if node not in ['S', 'T']]

def squared_intensity_difference(node1, node2, intensity):
	return square(intensity[node1] - intensity[node2])

def distance(node1, node2):
	return math.sqrt(square(node1[0] - node2[0]) + square(node1[1] - node2[1]))

def z_score(val, mean, variance):
	return (val - mean)/variance
	
def get_boundary_cost(node1, node2, intensity, gamma_val, sigma):		
	return gamma_val*(math.exp(-1*(np.mean(squared_intensity_difference(node1, node2, intensity))/2*square(sigma)))/distance(node1, node2))

def probability_of_background(node, intensity): #needs to be betterized
	count = [b for b in background if np.all(intensity[node] == intensity[b])] 
	return len(count)/len(background)
			
def probability_of_foreground(node, intensity): #needs to be betterized
	count = [f for f in foreground if np.all(intensity[node] == intensity[f])] 
	return len(count)/len(foreground)		

			
def get_regional_foreground_cost(node, intensity, fg_mean, fg_variance): #needs to be betterized
	prob = abs(np.mean(z_score(intensity[node], fg_mean, fg_variance))) #prob = probability_of_foreground(node, intensity)
	#if prob == 0:
	#	prob = 1e-320
	return -1*(math.log(prob))

def get_regional_background_cost(node, intensity, bg_mean, bg_variance):
	prob = abs(np.mean(z_score(intensity[node], bg_mean, bg_variance))) #prob = probability_of_background(node, intensity)
	#if prob == 0:
	#	prob = 1e-320
	return -1*(math.log(prob))

def add_neigbour_edges(G, max_neighbours_capacity, intensity, gamma_val, sigma, length, breadth):
	max_neighbours_capacity = 0
	for node in pixel_nodes(G):
		contender = 0
		for neigbour in get_neigbours(node, length, breadth):
			boundary_cost = get_boundary_cost(node, neigbour, intensity, gamma_val, sigma)
			G.add_edge(node, neigbour, capacity = boundary_cost)
			contender += boundary_cost
		if contender > max_neighbours_capacity:
			max_neighbours_capacity = contender
	return max_neighbours_capacity
	
def add_source_edges(G, intensity, ground_capacity, lambda_val, fg_mean, fg_variance):
	for node in pixel_nodes(G):
		if node in foreground:
			G.add_edge('S', node, capacity = ground_capacity)
		elif node in background:
			G.add_edge('S', node, capacity = 0)
		else:
			G.add_edge('S', node, capacity = lambda_val*get_regional_foreground_cost(node, intensity, fg_mean, fg_variance))

def add_sink_edges(G, intensity, ground_capacity, lambda_val, bg_mean, bg_variance):
	for node in pixel_nodes(G):
		if node in background:
			G.add_edge('T', node, capacity = ground_capacity)
		elif node in foreground:
			G.add_edge('T', node, capacity = 0)
		else:
			G.add_edge('T', node, capacity = lambda_val*get_regional_background_cost(node, intensity, bg_mean, bg_variance))
			
def add_edges(G, ground_capacity, max_neighbours_capacity, intensity, gamma_val, sigma, lambda_val, fg_mean, fg_variance, bg_mean, bg_variance, length, breadth):
	max_neighbours_capacity = add_neigbour_edges(G, max_neighbours_capacity, intensity, gamma_val, sigma, length, breadth)
	ground_capacity = max_neighbours_capacity + 1
	add_source_edges(G, intensity, ground_capacity, lambda_val, fg_mean, fg_variance)
	add_sink_edges(G, intensity, ground_capacity, lambda_val, bg_mean, bg_variance)

def add_nodes(G, img, length, breadth):
	G.add_node('S')
	G.add_node('T')
	print "l b", length, breadth
	#i = 614
	#j = 460
	#print "addnode", i, j, img[i][j]
	#print "addnode", j, i, img[j][i]
	for i in range(0, length):
		for j in range(0, breadth):
			try:
				G.add_node((i,j), val = img[i][j])
			except:
				print "error", i, j
def print_edges(G):
	for edge in G.edges(data=True):
		print edge, intensity[edge[0]]
	
def init(img):	
	length, breadth = img.shape[0:2]
	print (img.shape[0:2])
	ground_capacity, max_neighbours_capacity = 0,0
	gamma_val, sigma, lambda_val = 35, 0.5, 2
	G = nx.Graph()
	add_nodes(G, img, length, breadth)
	intensity = nx.get_node_attributes(G,'val')
	fg_mean, fg_variance = gaussian_function(foreground, intensity)
	bg_mean, bg_variance = gaussian_function(background, intensity)
	add_edges(G, ground_capacity, max_neighbours_capacity, intensity, gamma_val, sigma, lambda_val, fg_mean, fg_variance, bg_mean, bg_variance, length, breadth)	
	
	return G, img

	
G, img = init(img)

with open('graph.pkl', 'wb') as fp:
	pickle.dump(G, fp, pickle.HIGHEST_PROTOCOL)