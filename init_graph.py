#python 2.7
import pickle
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import networkx as nx
from classes import *

with open('foreground.pkl', 'rb') as fp:
		foreground = pickle.load(fp)

with open('background.pkl', 'rb') as fp:
		background = pickle.load(fp)

img = mpimg.imread('woman.jpg')
imgplot = plt.imshow(img)
plt.imshow(img)
#plt.show()
length, breadth = img.shape[0], img.shape[1]

nodes = np.array([[Node(-1, -1,-1) for x in range(breadth)] for y in range(length)])

arr = [[-1 for x in range(breadth)] for y in range(length)]

G = nx.Graph()
G.add_node('S')
G.add_node('T')

for i in range(0, length):
	for j in range(0, breadth):
		nodes[i,j] = Node(i, j, img[i][j])
		G.add_node((i,j), val = img[i][j])#obj = nodes[i,j])
		#print(nodes[i,j].coordinates(), nodes[i,j].val)
		
		
#print sorted(G.nodes(data=True))[0]

value = nx.get_node_attributes(G,'val')
print value[(0,0)]

print "faorfawf"
for pixel in foreground:
	print value[pixel]
	
print "barbaof"
for pixel in background:
	print value[pixel]
	
xx = [value[pixel] for pixel in background]	
print xx
print any(np.array_equal(x, np.array([89,89,89]) for x in xx))

x = value[(0,0)]
print x
print type(x)