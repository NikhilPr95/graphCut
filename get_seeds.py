import pickle
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import numpy as np
import cv2
import sys

BLACK = [0,0,0]         # sure BG
WHITE = [255,255,255]   # sure FG

DRAW_BG = {'color' : BLACK, 'val' : 0}
DRAW_FG = {'color' : WHITE, 'val' : 1}
thickness = 1           # brush thickness
value = DRAW_FG 
drawing = False
fg = list()
bg = list()

# registers user input
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

#marking the image
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

#values exceeding bounds
exf = [f for f in fg if (f[0] >= img.shape[0] or f[1] >= img.shape[1] or f[0] < 0 or f[1] < 0)]
exb = [b for b in bg if (b[0] >= img.shape[0] or b[1] >= img.shape[1] or b[0] < 0 or b[1] < 0)]
print "exceed", exf
print "exceed", exb

fg = [f for f in fg if f not in exf]
bg = [b for b in bg if b not in exb]

#saving original image
img = mpimg.imread(sys.argv[1])

with open('foreground_assigned.pkl', 'wb') as fp:
	pickle.dump(fg, fp, pickle.HIGHEST_PROTOCOL)
	
with open('background_assigned.pkl', 'wb') as fp:
	pickle.dump(bg, fp, pickle.HIGHEST_PROTOCOL)
	
with open('img.pkl', 'wb') as fp:
	pickle.dump(img, fp, pickle.HIGHEST_PROTOCOL)
