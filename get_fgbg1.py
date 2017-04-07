import pickle
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import numpy as np
import cv2
import sys

img_name = 'blacktoucan.jpg'

img1 = mpimg.imread(img_name)
'''	
def initialize_image():
	ax = plt.gca()
	fig = plt.gcf()
	implot = ax.imshow(img)
	cid = fig.canvas.mpl_connect('button_press_event', onclick)

def onclick(event):
	x, y = round(event.xdata), round(event.ydata)
	if x != None and y != None:
		coords.append((y,x))

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
'''
BLACK = [0,0,0]         # sure BG
WHITE = [255,255,255]   # sure FG

DRAW_BG = {'color' : BLACK, 'val' : 0}
DRAW_FG = {'color' : WHITE, 'val' : 1}
thickness = 1           # brush thickness
value = DRAW_FG 
drawing = False
fg = list()
bg = list()

def onmouse(event,x,y,flags,param):
	global img,value,drawing    
	if event == cv2.EVENT_LBUTTONDOWN:
			drawing = True
			cv2.circle(img,(x,y),thickness,value['color'],-1)
			if(value['color']==BLACK):
				bg.append((y,x));
			if(value['color']==WHITE):
				fg.append((y,x));
            

	elif event == cv2.EVENT_MOUSEMOVE:
		if drawing == True:
			cv2.circle(img,(x,y),thickness,value['color'],-1)
			if(value['color']==BLACK):
				bg.append((y,x));
			if(value['color']==WHITE):
				fg.append((y,x));

	elif event == cv2.EVENT_LBUTTONUP:
		if drawing == True:
			drawing = False
			cv2.circle(img,(x,y),thickness,value['color'],-1)
			if(value['color']==BLACK):
				bg.append((y,x));
			if(value['color']==WHITE):
				fg.append((y,x));
           
img = cv2.imread(sys.argv[1])
img2 = img.copy()
cv2.namedWindow('input')
cv2.setMouseCallback('input',onmouse)

while(1):	
	cv2.imshow('input',img)
	
	k = 0xFF & cv2.waitKey(1)
	if k == 27:         # esc to exit
		break
	elif k == ord('0'): # BG drawing
		print(" mark background regions with left mouse button \n")
		value = DRAW_BG
	elif k == ord('1'): # FG drawing
		print(" mark foreground regions with left mouse button \n")
		value = DRAW_FG
cv2.destroyAllWindows()

fg = list(set(fg))
bg = list(set(bg))
#print fg
#print bg
	
#assign(fg, coords, 'a', 'foreground')
#assign(bg, coords, 'b', 'background')

#print("fg", foreground)
#print("bg", background)

#print foreground
#print background
with open('foreground_assigned.pkl', 'wb') as fp:
	pickle.dump(fg, fp, pickle.HIGHEST_PROTOCOL)
	
with open('background_assigned.pkl', 'wb') as fp:
	pickle.dump(bg, fp, pickle.HIGHEST_PROTOCOL)
	
with open('img.pkl', 'wb') as fp:
	pickle.dump(img1, fp, pickle.HIGHEST_PROTOCOL)
