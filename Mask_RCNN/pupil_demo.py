import os
import sys
import random
import math
import numpy as np
import skimage.io
import matplotlib
import matplotlib.pyplot as plt

# Root directory of the project
ROOT_DIR = os.path.abspath("./")
print("ROOT_DIR",ROOT_DIR)

# Import Mask RCNN
sys.path.append(ROOT_DIR)  # To find local version of the library
from mrcnn import utils
import mrcnn.model as modellib
from mrcnn import visualize
# Import COCO config
sys.path.append(os.path.join(ROOT_DIR, "./samples/pupil/"))  # To find local version
import samples.pupil.pupil_n

#% matplotlib inline 

# Directory to save logs and trained model
MODEL_DIR = os.path.join(ROOT_DIR, "logs")

# Local path to trained weights file
COCO_MODEL_PATH = os.path.join(ROOT_DIR, "./logs/point20200408T0107/mask_rcnn_point_0100.h5")
# Download COCO trained weights from Releases if needed
if not os.path.exists(COCO_MODEL_PATH):
    utils.download_trained_weights(COCO_MODEL_PATH)

# Directory of images to run detection on
IMAGE_DIR = os.path.join(ROOT_DIR, "./pupil_test_im2/val")
print("IMAGE_DIR",IMAGE_DIR)

class InferenceConfig(samples.pupil.pupil_n.PointConfig):
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
class_names = ['BG','point']

# Load a random image from the images folder
#file_names = next(os.walk(IMAGE_DIR))[2]
count = os.listdir(IMAGE_DIR)
for i in range(0,len(count)):
    if count[i]!='via_region_data.json':
        print(i)
        print(count[i])
        path = os.path.join(IMAGE_DIR, count[i])
        if os.path.isfile(path):
            file_names = next(os.walk(IMAGE_DIR))[2]
            image = skimage.io.imread(os.path.join(IMAGE_DIR, count[i]))
            # Run detection
            results = model.detect([image], verbose=1)
            # Visualize results
            r = results[0]
            visualize.display_instances(count[i],image, r['rois'], r['masks'], r['class_ids'], 
                                class_names, r['scores'])


#plt.savefig("D:/Users/user/Desktop/maskRCNN/sav.jpg")

							
							
							
							