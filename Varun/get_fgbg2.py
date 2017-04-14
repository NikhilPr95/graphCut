import pickle
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import numpy as np
import cv2
import sys

rectangle = False
rect_over = False
BLUE = [255,0,0]        # rectangle color

rect_coord = list()

BLACK = [0,0,0]         # sure BG
WHITE = [255,255,255]   # sure FG

DRAW_BG = {'color' : BLACK, 'val' : 0}
DRAW_FG = {'color' : WHITE, 'val' : 1}
thickness = 3           # brush thickness
value = DRAW_FG 
drawing = False
fg = list()
bg = list()

def onmouse(event,x,y,flags,param):
	global img,value,drawing    
	global rectangle, ix, iy, img2, rect_over
	
	#drawing rectangle
	
	if event == cv2.EVENT_RBUTTONDOWN:
		rectangle = True
		ix,iy = x,y
		

	elif event == cv2.EVENT_MOUSEMOVE:
		if rectangle == True: 
			img = img2.copy()           
			cv2.rectangle(img,(ix,iy),(x,y),BLUE,2) 
			           

	elif event == cv2.EVENT_RBUTTONUP:
		rectangle = False  
		rect_over = True      
		cv2.rectangle(img,(ix,iy),(x,y),BLUE,2)
		rect_coord.append((ix,iy,x,y))		
		populate()
	
	#drawing touch up curves	
	if event == cv2.EVENT_LBUTTONDOWN:
			if rect_over == True:
				drawing = True
				cv2.circle(img,(x,y),thickness,value['color'],-1)
				if(value['color']==BLACK):
					bg.append((y,x));
				if(value['color']==WHITE):
					fg.append((y,x));
			else:
				print "Draw rectangle first"
            

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

def populate():
	for i in range(img.shape[0]):
		for j in range(img.shape[1]):
			if( (i < rect_coord[0][0] or i > rect_coord[0][2]) or ( j<rect_coord[0][1] or j>rect_coord[0][3])):
				bg.append( (j,i))
           
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

exf = [f for f in fg if (f[0] >= img.shape[0] or f[1] >= img.shape[1] or f[0] < 0 or f[1] < 0)]
exb = [b for b in bg if (b[0] >= img.shape[0] or b[1] >= img.shape[1] or b[0] < 0 or b[1] < 0)]
print "exceed", exf
print "exceed", exb

fg = [f for f in fg if f not in exf]
bg = [b for b in bg if b not in exb]

#print "fg", fg
#print "bg", bg

img = mpimg.imread(sys.argv[1])
with open('foreground_assigned.pkl', 'wb') as fp:
	pickle.dump(fg, fp, pickle.HIGHEST_PROTOCOL)
	
with open('background_assigned.pkl', 'wb') as fp:
	pickle.dump(bg, fp, pickle.HIGHEST_PROTOCOL)
	
with open('img.pkl', 'wb') as fp:
	pickle.dump(img, fp, pickle.HIGHEST_PROTOCOL)
