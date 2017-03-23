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

def onmouse(event,x,y,flags,param):
	global img,value,drawing    
	if event == cv2.EVENT_LBUTTONDOWN:
			drawing = True
			cv2.circle(img,(x,y),thickness,value['color'],-1)
			if(value['color']==BLACK):
				bg.append((x,y));
			if(value['color']==WHITE):
				fg.append((x,y));
            

	elif event == cv2.EVENT_MOUSEMOVE:
		if drawing == True:
			cv2.circle(img,(x,y),thickness,value['color'],-1)
			if(value['color']==BLACK):
				bg.append((x,y));
			if(value['color']==WHITE):
				fg.append((x,y));

	elif event == cv2.EVENT_LBUTTONUP:
		if drawing == True:
			drawing = False
			cv2.circle(img,(x,y),thickness,value['color'],-1)
			if(value['color']==BLACK):
				bg.append((x,y));
			if(value['color']==WHITE):
				fg.append((x,y));
           
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
print fg
print bg
