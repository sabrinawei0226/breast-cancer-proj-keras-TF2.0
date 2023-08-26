import os
import sys
import random
import math
import numpy as np
import skimage.io
import matplotlib
import matplotlib.pyplot as plt
import tkinter as tk
import tkinter.messagebox 
import subprocess

# Root directory of the project
ROOT_DIR = os.path.abspath("./")
print("ROOT_DIR",ROOT_DIR)

# Import Mask RCNN
sys.path.append(ROOT_DIR)  # To find local version of the library
from mrcnn import utils
import mrcnn.model as modellib
from mrcnn import visualize
# Import COCO config
sys.path.append(os.path.join(ROOT_DIR, "/home/lab/chia_shin/pythonwork/Mask_RCNN_master2/samples/pupil/"))  # To find local version
import samples.pupil.pupil

#% matplotlib inline 

# Directory to save logs and trained model
MODEL_DIR = os.path.join(ROOT_DIR, "logs")

# Local path to trained weights file
COCO_MODEL_PATH = os.path.join(ROOT_DIR, "C:/pythonwork/chia_shin/Mask_RCNN_master2/logs/calcification20200630_class=cal_128th/mask_rcnn_calcification_0128.h5")
# Download COCO trained weights from Releases if needed
if not os.path.exists(COCO_MODEL_PATH):
    utils.download_trained_weights(COCO_MODEL_PATH)

# Directory of images to run detection on
IMAGE_DIR = os.path.join(ROOT_DIR, "./dataset_test/test")#--------------------------------改#train/test
#IMAGE_DIR = os.path.join(ROOT_DIR, "/home/lab/chia_shin/pythonwork/Mask_RCNN_master/cut_img")
print("IMAGE_DIR",IMAGE_DIR)


class InferenceConfig(samples.pupil.pupil.BalloonConfig):
    # Set batch size to 1 since we'll be running inference on
    # one image at a time. Batch size = GPU_COUNT * IMAGES_PER_GPU
    GPU_COUNT = 1
    IMAGES_PER_GPU = 1

config = InferenceConfig()
config.display()

# Create model object in inference mode.
model = modellib.MaskRCNN(mode="inference", model_dir=MODEL_DIR, config=config)

# Load weights trained on MS-COCO
model.load_weights(COCO_MODEL_PATH, by_name=True)

# COCO Class names
# Index of the class in the list is its ID. For example, to get ID of
# the teddy bear class, use: class_names.index('teddy bear')
class_names = ['BG','cal']
#class_names = ['BG','benign','cancerous']

# Load a random image from the images folder
#file_names = next(os.walk(IMAGE_DIR))[2]
count = os.listdir(IMAGE_DIR)
#print("count=",count) #[檔名1, 檔名2, ...]
for i in range(0,len(count)):
    if count[i]!='via_region_data.json' and count[i]!='desktop.ini' :
        print("i=",i) #第幾張影像
        print("count[i]=",count[i]) #檔名
        path = os.path.join(IMAGE_DIR, count[i])
        if os.path.isfile(path):
            file_names = next(os.walk(IMAGE_DIR))[2]
            image = skimage.io.imread(os.path.join(IMAGE_DIR, count[i]))
            # Run detection
            results = model.detect([image], verbose=1)
            # Visualize results
            r = results[0]
            visualize2.display_instances(count[i],image, r['rois'], r['masks'], r['class_ids'], 
                             class_names, r['scores'])
            print("#==============================")
            
'''
tk.messagebox.showinfo(title='information',message='分析完成!')

os.chdir('/home/lab/chia_shin/pythonwork/breast_ui')
cmd =str("python benign_evil_analysis.py")
subprocess.call(cmd, shell=True)
'''
#plt.savefig("D:/Users/user/Desktop/maskRCNN/sav.jpg")

							
							
							
							
