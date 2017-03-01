import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import networkx as nx	
img = mpimg.imread('stinkbug.png')
imgplot = plt.imshow(img)
lum_img = img[:,:,0]
plt.imshow(lum_img)

length, breadth = lum_img.shape[0], img.shape[1]

class Node:
	def __init__(self, x, y, val):
		self.x = x
		self.y = y
		self.val = val

	def coordinates(self):
		return (self.x, self.y)
		
	def val(self):
		return val
	  
nodes = np.array([[Node(-1, -1,-1) for x in range(breadth)] for y in range(length)])

arr = [[-1 for x in range(breadth)] for y in range(length)]

G = nx.Graph()
		
for i in range(0, length):
	for j in range(0, breadth):
		nodes[i,j] = Node(i, j, lum_img[i][j])
		G.add_node((i,j), val = lum_img[i][j])#obj = nodes[i,j])
		#print(nodes[i,j].coordinates(), nodes[i,j].val)
		
xs = nx.get_node_attributes(G, 'val')
print xs

'red'
#for node in G.nodes():
#	print node.coordinates()