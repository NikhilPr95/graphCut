#python 2.7
from __future__ import division

import pickle
import cv2
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

def non_fgbg_pixel_nodes(G, foreground, background):
	return [node for node in sorted(G.nodes()) if node not in ['S', 'T'] and node not in foreground and node not in background]

def squared_intensity_difference(node1, node2, intensity):
	return square(intensity[node1] - intensity[node2])

def distance(node1, node2):
	return math.sqrt(square(node1[0] - node2[0]) + square(node1[1] - node2[1]))

def z_score(val, mean, variance):
	return (val - mean)/variance
	
def get_boundary_cost(node1, node2, intensity, gamma_val, sigma):		
	return gamma_val*(math.exp(-1*(np.mean(squared_intensity_difference(node1, node2, intensity))/2*square(sigma)))/distance(node1, node2))

def probability_of_background(node, background_set, bg_variance, intensity): #needs to be betterized
	max_prob = 0
	for b_node in background_set:
		prob = abs(np.mean(z_score(intensity[node], intensity[b_node], bg_variance)))
		if prob > max_prob:
			max_prob = prob
			
	return max_prob
			
def probability_of_foreground(node, foreground_set, fg_variance, intensity): #needs to be betterized
	max_prob = 0
	for f_node in foreground_set:
		prob = abs(np.mean(z_score(intensity[node], intensity[f_node], fg_variance)))
		if prob > max_prob:
			max_prob = prob
			
	return max_prob
	
			
def get_regional_foreground_cost(node, intensity, foreground_set, fg_mean, fg_variance): #needs to be betterized
	prob = probability_of_foreground(node, foreground_set, fg_variance, intensity)
	return -1*(math.log(prob))

def get_regional_background_cost(node, intensity, background_set, bg_mean, bg_variance):
	prob = probability_of_background(node, background_set, bg_variance, intensity)
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
	
def add_source_edges(G, intensity, ground_capacity, lambda_val, foreground, background, foreground_set, fg_mean, fg_variance):
	for node in foreground:
		G.add_edge('S', node, capacity = ground_capacity)
	for node in background:
		G.add_edge('S', node, capacity = 0)
	for node in non_fgbg_pixel_nodes(G, foreground, background):
		G.add_edge('S', node, capacity = lambda_val*get_regional_foreground_cost(node, intensity, foreground_set, fg_mean, fg_variance))

def add_sink_edges(G, intensity, ground_capacity, lambda_val, foreground, background, background_set, bg_mean, bg_variance):
	for node in foreground:
		G.add_edge('S', node, capacity = 0)
	for node in background:
		G.add_edge('S', node, capacity = ground_capacity)
	for node in non_fgbg_pixel_nodes(G, foreground, background):
		G.add_edge('T', node, capacity = lambda_val*get_regional_background_cost(node, intensity, background_set, bg_mean, bg_variance))
			
def add_edges(G, ground_capacity, max_neighbours_capacity, intensity, gamma_val, sigma, lambda_val, foreground, fg_mean, fg_variance, background, bg_mean, bg_variance, length, breadth, foreground_set, background_set):
	max_neighbours_capacity = add_neigbour_edges(G, max_neighbours_capacity, intensity, gamma_val, sigma, length, breadth)
	ground_capacity = max_neighbours_capacity + 1
	print ('adding source edges')
	add_source_edges(G, intensity, ground_capacity, lambda_val, foreground, background, foreground_set, fg_mean, fg_variance)
	print ('adding sink edges')
	add_sink_edges(G, intensity, ground_capacity, lambda_val, foreground, background, background_set, bg_mean, bg_variance)

def add_nodes(G, img, length, breadth):
	G.add_node('S')
	G.add_node('T')
	print "l b", length, breadth
	for i in range(0, length):
		for j in range(0, breadth):
			try:
				G.add_node((i,j), val = img[i][j])
			except:
				print "error", i, j
def print_edges(G):
	for edge in G.edges(data=True):
		print edge, intensity[edge[0]]

def smooth(img):
    kernel = np.ones((5,5),np.float32)/25
    dst = cv2.filter2D(img,-1,kernel)
    return dst

def smooth2(img):
	return cv2.blur(img, (5,5))

def smooth3(img):
	return cv2.GaussianBlur(img, (5,5), 0)

def getset(list, intensity):
	result = []
	for node in list:
		if len(result) == 0:
			result.append(node)
		else:
			if not any(np.array_equal(intensity[node], intensity[x]) for x in result):
					result.append(node)

	print("size", len(list), len(result))
	return result

def init(img, foreground, background):	
	length, breadth = img.shape[0:2]
	print (img.shape[0:2])
	ground_capacity, max_neighbours_capacity = 0,0
	gamma_val, sigma, lambda_val = 10000, 1.5, 0.01
	G = nx.Graph()
	add_nodes(G, smooth(img), length, breadth)
	intensity = nx.get_node_attributes(G,'val')
	foreground_set = getset(foreground, intensity)
	background_set = getset(background, intensity)

	fg_mean, fg_variance = gaussian_function(foreground, intensity)
	bg_mean, bg_variance = gaussian_function(background, intensity)
	print('adding edges')
	add_edges(G, ground_capacity, max_neighbours_capacity, intensity, gamma_val, sigma, lambda_val, foreground, fg_mean, fg_variance, background, bg_mean, bg_variance, length, breadth, foreground_set, background_set)	
	
	return G, img

	
G, img = init(img, foreground, background)

with open('graph.pkl', 'wb') as fp:
	pickle.dump(G, fp, pickle.HIGHEST_PROTOCOL)