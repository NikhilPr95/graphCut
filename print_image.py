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

with open('img.pkl', 'rb') as fp:
		img = pickle.load(fp)

with open('flow_dict.pkl', 'rb') as fp:
		flow_dict = pickle.load(fp)
		
length, breadth = img.shape[0:2]

for i in range(0, length):
	for j in range(0, breadth):
		if flow_dict[(i,j)]['S'] == 1:
			print img[i][j], flow_dict[(i,j)]['S']
