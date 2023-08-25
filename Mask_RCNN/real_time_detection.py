
import cv2
import os
import sys
#============================================================
import numpy as np
import argparse
#============================================================
def rotate(image, angle, center=None, scale=1.0):
    # 取得影像尺寸
    (h, w) = image.shape[:2]
 
    # 若未指定旋轉中心，則將影像中心設為旋轉中心
    if center is None:
        center = (w / 2, h / 2)
 
    # 執行旋轉
    M = cv2.getRotationMatrix2D(center, angle, scale)
    rotated = cv2.warpAffine(image, M, (w, h))
 
    # 返回旋轉後的影像
    return rotated
#============================================================

# Root directory of the project
ROOT_DIR = os.path.abspath("./")
# Import Mask RCNN
sys.path.append(ROOT_DIR)  # To find local version of the library
from mrcnn.config import Config
from mrcnn import model as modellib, utils
from mrcnn import visualize
#import samples.pupil.pupil
import samples.pupil.new_mask
# Directory to save logs and model checkpoints, if not provided
# through the command line argument --logs
PRETRAINED_MODEL_PATH = "./logs/new_mask20200505T1814/mask_rcnn_new_mask_0200.h5"

class InferenceConfig(samples.pupil.new_mask.new_maskConfig):
    # Set batch size to 1 since we'll be running inference on
    # one image at a time. Batch size = GPU_COUNT * IMAGES_PER_GPU
    GPU_COUNT = 1
    IMAGES_PER_GPU = 1

if __name__ == '__main__':
     class_names = ['BG','full_med_bad','full_med_good','full_normal','half_med_bad','half_med_good','half_normal']
     #載入模型
     config = InferenceConfig()
     config.display()

     model = modellib.MaskRCNN(mode="inference", config=config, model_dir='./logs/new_mask20200505T1814/mask_rcnn_new_mask_0200.h5')
     model_path = PRETRAINED_MODEL_PATH
     # or if you want to use the latest trained model, you can use :
     # model_path = model.find_last()[1]
     model.load_weights(model_path, by_name=True)
     colors = visualize.random_colors(len(class_names))

     #cap = cv2.VideoCapture(0)
     #cap = cv2.VideoCapture("./full_med_good1.mp4")
     #cap = cv2.VideoCapture("D:\\MSI\Pictures\\Camera Roll\\new\\WIN_20200428_21_42_02_Pro.mp4")
     cap = cv2.VideoCapture("C:\\Users\MSI\\Desktop\\影片\\有污漬 沒戴好的 醫療.mp4")
     
     while True:

         _, frame = cap.read()
         predictions = model.detect([frame],
                                    verbose=1)  # We are replicating the same image to fill up the batch_size
         p = predictions[0]

         output = visualize.display_instances2(frame, p['rois'], p['masks'], p['class_ids'],
                                     class_names, p['scores'], colors=colors, real_time=True)
         #==============================================
         #向左旋轉270度
         rotated = rotate(output, 270)
         cv2.imshow("Rotated by 45 Degrees", rotated)
         #cv2.imshow("Mask RCNN", output)
         #==============================================
         k = cv2.waitKey(1)
         if k & 0xFF == ord('q'):
             break
     cap.release()
     cv2.destroyAllWindows()