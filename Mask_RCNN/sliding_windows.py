import time
import cv2
import os
import sys
from keras.preprocessing.image import img_to_array
from keras.models import load_model
import numpy as np
import imutils
import math
from itertools import product

winW=40
winH=40
v_stepSize=22
h_stepSize=22

#********************************************************************************************************
#*********** 原本在image_classification_keras/sliding_window/pyimagesearch/helpers.py檔內的 *************
#********************************************************************************************************
def sliding_window(image, v_stepSize, h_stepSize, windowSize):
	# slide a window across the image
	#for y in range(0, image.shape[0], stepSize):
	for y in range(0, image.shape[0], v_stepSize):
		#for x in range(0, image.shape[1], stepSize):
		for x in range(0, image.shape[1], h_stepSize):
			#sw = image[y:y + windowSize[1], x:x + windowSize[0]]
			#sum = np.sum(sw)
			#print("sum of pixel intensity in sliding window=",sum)
			# yield the current window
			yield (x, y, image[y:y + windowSize[1], x:x + windowSize[0]]) #将 return 换成了 yield

#********************************************************************************************************
#******************************************** 主程式 **************************************
#********************************************************************************************************
# load the image and define the window width and height
bc = "cancerous" #benign #cancerous #--------------------------------------------------------------------------改
tt = "train" #train #test #--------------------------------------------------------------------------改
fileDir = "./dataset_test/seg/"+bc+"_"+tt
pathDir = os.listdir(fileDir)
for file in pathDir:
   num = 0
   #print(file)
   image = cv2.imread(fileDir+'/'+file)
   clone = image.copy()
   img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
   for (x, y, window) in sliding_window(img, v_stepSize=int(v_stepSize), h_stepSize=int(h_stepSize), windowSize=(winW, winH)):
        # if the window does not meet our desired window size, ignore it
        if window.shape[0] != winH or window.shape[1] != winW:
            continue
        
        count_black=0
        
        for i in range(len(window)):
            for j in range(len(window[i])):
                #print(window[i][j])
                if window[i][j] == 0:
                    count_black = count_black + 1
        #print(count_black)
        
        if count_black != (winW*winH):
            num = num + 1
            cv2.imwrite("./dataset_test/seg/"+bc+"_"+tt+"_cut/"+file[:-4]+"_cut"+str(num)+".jpg",window)

