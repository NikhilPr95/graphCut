import pickle
import matplotlib.image as mpimg
import matplotlib.pyplot as plt

img_name = 'woman.jpg'

img = mpimg.imread(img_name)
	
def initialize_image():
	ax = plt.gca()
	fig = plt.gcf()
	implot = ax.imshow(img)
	cid = fig.canvas.mpl_connect('button_press_event', onclick)

def onclick(event):
	x, y = round(event.xdata), round(event.ydata)
	if x != None and y != None:
		coords.append((x,y))

def set_and_delete(ground, coords):
	ground[:] = coords[:]
	del coords[:]

def assign(ground, coords, char, type):
	print("You wil be shown the image. Press " + char + " to start marking " + type + " and x when you're done")	
	ch = raw_input()
	if (ch == char):
		initialize_image()
		plt.show()
		set_and_delete(ground, coords)
	
coords = []
foreground = []
background = []
	
assign(foreground, coords, 'a', 'foreground')
assign(background, coords, 'b', 'background')

print("fg", foreground)
print("bg", background)

with open('foreground_assigned.pkl', 'wb') as fp:
	pickle.dump(foreground, fp, pickle.HIGHEST_PROTOCOL)
	
with open('background_assigned.pkl', 'wb') as fp:
	pickle.dump(background, fp, pickle.HIGHEST_PROTOCOL)
	
with open('img.pkl', 'wb') as fp:
	pickle.dump(img, fp, pickle.HIGHEST_PROTOCOL)