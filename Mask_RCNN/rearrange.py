'''
activate tf1
cd C:\pythonwork\chia_shin\Mask_RCNN_master2
python rearrange.py
'''


import cv2
import os
import numpy as np
bc = "cancerous" #benign #cancerous #--------------------------------------------------------------------------改
tt = "test" #train #test #--------------------------------------------------------------------------改
fileDir = "./dataset_test/seg/"+bc+"_"+tt
global crop_img
crop_img = []

def draw_min_rect(img1, cnts):  # conts = contours
    global crop_img
    img = np.copy(img1)
    #img2 = np.copy(img1)
    img2 = cv2.cvtColor(img1.copy(), cv2.COLOR_BGR2GRAY)
    #new = np.zeros((128, 128,3), dtype=np.int)
    new = np.zeros((128, 128))
    print("new=",new)
    print("img2=",img2)
    #N = 0
    max_h = 0
    w_last = 0
    h_last = 0
    for cnt in cnts:
        #N = N + 1
        x, y, w, h = cv2.boundingRect(cnt)
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 1)
        #crop = img2[y:y + h, x:x + w]
        '''
        if N == 1:
            new[max_h:max_h+h , w_last:x+w] = img2[y:y+h , x:x+w]
            max_h = h
            w_last = w
            h_last = h
        else:
        '''   
        print("new=",new.shape)
        print("img2=",img2.shape)
        if w_last+w <= 128:
            new[h_last:h_last+h , w_last:w_last+w] = img2[y:y+h , x:x+w]
            w_last = w_last + w
            if h>max_h:
                max_h = h
        else:
            w_last = 0
            new[max_h:max_h+h , w_last:w_last+w] = img2[y:y+h , x:x+w]
            w_last = w_last + w
            if h>max_h:
                max_h = h
    #cv2.imshow("new",new)
    #cv2.waitKey(0)
    
        #crop_img.append(crop)
        #print(new)
        #print("crop_img=",crop_img)
        
    return img, new #, angle


for file in os.listdir(fileDir):
   image = cv2.imread(os.path.join(fileDir,file))
   thresh = cv2.Canny(image, 128, 256)
   contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
   img, new = draw_min_rect(image, contours) #img, angle 
   #cv2.imshow("image",img)
   cv2.imwrite('./dataset_test/rect/'+bc+'_'+tt+'_min_rect/'+file, img)
   cv2.imwrite('./dataset_test/rect/'+bc+'_'+tt+'_rearrange/'+file, new)
   #print(angle)

   ############################################################
   #  Merge
   ############################################################
   file_dir = "./dataset_test/cal/"+tt+"_merge"
   merge_img = cv2.imread(os.path.join(file_dir,file))
   img = cv2.resize(img, (1000,1000))
   merge = np.hstack((merge_img,img))
   #new = cv2.resize(new, (1000,1000))
   new = cv2.imread('./dataset_test/rect/'+bc+'_'+tt+'_rearrange/'+file)
   new = cv2.resize(new, (1000,1000))
   merge = np.hstack((merge,new))
       
   if len(merge)!=0:
      cv2.imwrite("./dataset_test/cal/"+bc+"_"+tt+"_merge/"+file,merge)
   	