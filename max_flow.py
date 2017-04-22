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

print("computing max flow")

#computes the minimum cut and performs partition
cut_value, partition = nx.minimum_cut(G, 'S', 'T')
foreground, background = partition

with open('foreground_partition.pkl', 'wb') as fp:
	pickle.dump(foreground, fp, pickle.HIGHEST_PROTOCOL)
	
with open('background_partition.pkl', 'wb') as fp:
	pickle.dump(background, fp, pickle.HIGHEST_PROTOCOL)