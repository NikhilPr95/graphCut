import cv2
import sys
import os


name = os.path.splitext(os.path.basename(sys.argv[1]))[0]
ext = os.path.splitext(os.path.basename(sys.argv[1]))[1]

img = cv2.imread(name+ext)


cv2.imwrite(name+'_new'+ext,cv2.resize(img,(220,220)))

