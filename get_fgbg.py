import pickle
import matplotlib.image as mpimg
import matplotlib.pyplot as plt

im = mpimg.imread('woman.jpg')

def initialize_image():
	ax = plt.gca()
	fig = plt.gcf()
	implot = ax.imshow(im)
	cid = fig.canvas.mpl_connect('button_press_event', onclick)
	#line, = ax.plot([], [], linestyle="none", marker="o", color="r")
	#linebuilder = LineBuilder(line)

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

with open('foreground.pkl', 'wb') as fp:
	pickle.dump(foreground, fp, pickle.HIGHEST_PROTOCOL)
	
with open('background.pkl', 'wb') as fp:
	pickle.dump(background, fp, pickle.HIGHEST_PROTOCOL)	