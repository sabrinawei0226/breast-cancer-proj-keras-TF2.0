import PIL
import os
import os.path
from PIL import Image
import cv2

#f = r'E:\new_vocal_cord_dataset\latest_images\480x270'
f = r'E:\wavelet_remove_stripe\Wavelet-Deep-Neural-Network-for-Stripe-Noise-Removal-master\test'
for file in os.listdir(f):
    f_img = f+"/"+file
    img = Image.open(f_img)
    '''
    imgCV = cv2.imread(f_img)
    size = imgCV.shape
    print (size)
    '''
    img = img.resize((256,256))
    img.save(f_img)