#python 2.7
from __future__ import division

import pickle
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import networkx as nx
import math
from classes import *
from networkx.algorithms.flow import maximum_flow

with open('graph.pkl', 'rb') as fp:
		G = pickle.load(fp)

"""
#print G.nodes()[0]
#mincostFlow = nx.max_flow_min_cost(G, 'S', 'T', capacity = 'capacity')
#Equivalent to above line
#Not guaranteed to work if edge weights are floats 
#made it work by casting demand to int


maxFlow = nx.maximum_flow_value(G, 'S', 'T', capacity = 'capacity')
H = nx.DiGraph(G)
H.add_node('S', demand = -int(maxFlow))
H.add_node('T', demand = int(maxFlow))
flow_cost, flow_dict = nx.network_simplex(H, capacity = 'capacity')

print("maxflow =", maxFlow)		
with open('flow_dict.pkl', 'wb') as fp:
	pickle.dump(flow_dict, fp, pickle.HIGHEST_PROTOCOL)
"""

cut_value, partition = nx.minimum_cut(G, 'S', 'T')
foreground, background = partition