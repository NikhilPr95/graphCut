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

with open('foreground_partition.pkl', 'rb') as fp:
		foreground = pickle.load(fp)

with open('background_partition.pkl', 'rb') as fp:
		background = pickle.load(fp)
		
length, breadth = img.shape[0:2]

#marks the background
for node in background:
	try:
		i, j = node
		img[i][j] = [255,0,0]
	except:
		x=1
		
			
plt.imshow(img)
plt.show()