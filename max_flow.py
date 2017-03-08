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

#print G.nodes()[0]
mincostFlow = nx.max_flow_min_cost(G, 'S', 'T')
print mincostFlow