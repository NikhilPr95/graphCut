import matplotlib.image as mpimg
import matplotlib.pyplot as plt

im = mpimg.imread('woman.jpg')

ax = plt.gca()
fig = plt.gcf()
implot = ax.imshow(im)

coords = []
foreground = []
background = []

def onclick(event):
	x, y = event.xdata, event.ydata
	if event.xdata != None and event.ydata != None:
		#print(x, y)
		coords.append((x,y))
		
def onKeyPress(event):
	print("you just did a ", event.char)
	
cid = fig.canvas.mpl_connect('button_press_event', onclick)

print("You wil be shown the image. Press a to start marking foreground, and x when you're done")

stopitnow = False

ch = raw_input()
if (ch == 'a'):
	plt.show()

"""
while (not stopitnow):
	ch = raw_input()
	if (ch == 'a'):
		plt.show()
	if (ch == 'x'):
		plt.close()
		stopitnow = True
"""
print(coords)		
foreground = coords[:]
del coords[:]

print("You wil be shown the image. Press b to start marking foreground, and x when you're done")
plt.close()

stopitnow = False

"""
while (not stopitnow):
	ch = raw_input()
	if (ch == 'b'):
		plt.show()
	if (ch == 'x'):
		plt.close()
		stopitnow = True
"""

ch = raw_input()
if (ch == 'b'):
	plt.close()
	im = mpimg.imread('woman.jpg')
	ax = plt.gca()
	fig = plt.gcf()
	cid = fig.canvas.mpl_connect('button_press_event', onclick)
	implot = ax.imshow(im)
	plt.show()
		
background = coords[:]
del coords[:]

print("fg", foreground)
print("bg", background)