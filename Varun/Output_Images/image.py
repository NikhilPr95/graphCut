import cv2
import sys
import numpy as np

input_img = cv2.imread(sys.argv[1])
mask_img = cv2.imread(sys.argv[2])
output_img = cv2.imread(sys.argv[3])

bar = np.zeros((input_img.shape[0],5,3),np.uint8)
res = np.hstack((input_img,bar,mask_img,bar,output_img))

cv2.imwrite('graphcut_output_'+sys.argv[1][0:sys.argv[1].find('.')]+'.png',res)




