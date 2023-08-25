import os
import sys
import random
import math
import numpy as np
import skimage.io
import cv2
from PIL import Image
import scipy
from scipy import misc
import matplotlib
import matplotlib.pyplot as plt
from skimage.measure import find_contours
from matplotlib import patches,  lines
from matplotlib.patches import Polygon
import IPython.display
import colorsys
# Root directory of the project
ROOT_DIR = os.path.abspath("../")

# Import Mask RCNN
sys.path.append(ROOT_DIR)  # To find local version of the library
from mrcnn import utils
import mrcnn.model as modellib
from mrcnn import visualize
################################################################   放入train.py的路徑 並import
# Import COCO config
sys.path.append(os.path.join(ROOT_DIR, "D:/Users/user/Desktop/maskRCNN/"))  # To find local version
import catvsdog2

#% matplotlib inline 

# Directory to save logs and trained model
MODEL_DIR = os.path.join(ROOT_DIR, "logs")

################################################################  放入訓練好的權重
# Local path to trained weights file
COCO_MODEL_PATH = os.path.join(ROOT_DIR, "D:/Users/user/Desktop/maskRCNN/mask_rcnn_catvsdog_0050.h5")
# Download COCO trained weights from Releases if needed
if not os.path.exists(COCO_MODEL_PATH):
    utils.download_trained_weights(COCO_MODEL_PATH)

# Directory of images to run detection on
IMAGE_DIR = os.path.join(ROOT_DIR, "images")

class InferenceConfig(catvsdog2.CatVSDogConfig):
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
################################################################ 增加模型辨識類別種類
class_names = ['BG','ca','tumor']

# Load a random image from the images folder     ##原始程式為隨機從資料集中抽取影像出來implement，修改為讀取固定影像((乳房影像批次crop出的四張影像))
#file_names = next(os.walk(IMAGE_DIR))[2]
#image = skimage.io.imread(os.path.join(IMAGE_DIR, random.choice(file_names)))
image1 = skimage.io.imread('D:/Users/user/Desktop/maskRCNN/breast_ui/run/crop/breast_crop1.bmp')
image2 = skimage.io.imread('D:/Users/user/Desktop/maskRCNN/breast_ui/run/crop/breast_crop2.bmp')
image3 = skimage.io.imread('D:/Users/user/Desktop/maskRCNN/breast_ui/run/crop/breast_crop3.bmp')
image4 = skimage.io.imread('D:/Users/user/Desktop/maskRCNN/breast_ui/run/crop/breast_crop4.bmp')
 
# Run detection  將影像輸入MaskRCNN model進行辨識
results1 = model.detect([image1], verbose=1)         
results2 = model.detect([image2], verbose=1)
results3 = model.detect([image3], verbose=1)
results4 = model.detect([image4], verbose=1)
#results 辨識結果輸出資訊
#{'rois': array([[897, 228, 903, 233]]), 'class_ids': array([1]), 'scores': array([0.9804196], dtype=float32), 'masks': array([[[False],....

# Visualize results
r1 = results1[0]
r2 = results2[0]
r3 = results3[0]
r4 = results4[0]
#r1 辨識結果輸出資訊，與model.detect相同
#{'rois': array([[897, 228, 903, 233]]), 'class_ids': array([1]), 'scores': array([0.9804196], dtype=float32), 'masks': array([[[False],....
################################################################ 因此可將之轉換為roi、mask、classid

# initial parameters
# 擷取各個參數之數值
boxes1 = r1['rois']                   #[[897 228 903 233]]
masks1 = r1['masks']                  #array([[[False],....
class_ids1 = r1['class_ids']          #[1]

boxes2 = r2['rois']
masks2 = r2['masks']
class_ids2 = r2['class_ids']

boxes3 = r3['rois']
masks3 = r3['masks']
class_ids3 = r3['class_ids']

boxes4 = r4['rois']
masks4 = r4['masks']
class_ids4 = r4['class_ids']

#初始化視覺化工具之參數
ax=None
scores=None
title=""
figsize=(16, 16)
show_mask=True
show_bbox=True
colors=None
captions=None
colors1=0
colors2=0
colors3=0
colors4=0

################################################################ 預設輸出object results 是套上隨機顏色的mask  ((因為改成全部為紅色  這段沒用到
def random_colors(N, bright=True):
    """
    Generate random colors.
    To get visually distinct colors, generate them in HSV space then
    convert to RGB.
    """
    brightness = 1.0 if bright else 0.7
    hsv = [(i / N, 1, brightness) for i in range(N)]
    colors = list(map(lambda c: colorsys.hsv_to_rgb(*c), hsv))
    random.shuffle(colors)
    return colors
	
def apply_mask(image, mask, color, alpha=0.5):
    """Apply the given mask to the image.
    """
    for c in range(3):
        image[:, :, c] = np.where(mask == 1,
                                  image[:, :, c] *
                                  (1 - alpha) + alpha * color[c] * 255,
                                  image[:, :, c])
    return image

################################################################ 原本程式是透過這行指令，呼叫visualize.py的display_instances function
#visualize.display_instances(image, r['rois'], r['masks'], r['class_ids'], 
#                            class_names, r['scores'])
################################################################ visualize.py的display_instances function
#display_instances(image, boxes, masks, class_ids, class_names,         #title=圖片上方的名字
#                     scores=None, title="",
#                      figsize=(16, 16), ax=None,
#                      show_mask=True, show_bbox=True,
#                      colors=None, captions=None):
#    """
#    boxes: [num_instance, (y1, x1, y2, x2, class_id)] in image coordinates.
#    masks: [height, width, num_instances]
#    class_ids: [num_instances]
#    class_names: list of class names of the dataset
#    scores: (optional) confidence scores for each box
#    title: (optional) Figure title
#    show_mask, show_bbox: To show masks and bounding boxes or not
#    figsize: (optional) the size of the image
#    colors: (optional) An array or colors to use with each object
#    captions: (optional) A list of strings to use as captions for each object
#    """

# Number of instances  計算有幾個目標區域(影像包含N個物件)
N = boxes1.shape[0]
#若不包含任何物件，則顯示Error
if not N:                                                              
    print("\n*** No instances to display *** \n")
else:
    assert boxes1.shape[0] == masks1.shape[-1] == class_ids1.shape[0]
		
# fig, ax = plt.subplots()在一個視窗繪製多個圖表	
# If no axis is passed, create one and automatically call show()  	# 如果沒有傳遞axis變數，則創建一個軸並自動調用auto_show() ((show img
auto_show = False
if not ax:
    _, ((ax1,ax2),(ax3,ax4)) = plt.subplots(nrows=2,ncols=2,figsize=figsize)    
    #_, ax = plt.subplots(1, figsize=figsize)	原始code show 單張result			
    #ax3 = plt.subplots(3,3 ,figsize=figsize)   會新創建一個3*3的window
    auto_show = True
	
# 顯示超出圖像邊界的區域。
# Show area outside image boundaries.
height, width = image1.shape[:2]
ax1.set_ylim(height + 10, -10)         #設置y軸高度限制
ax1.set_xlim(-10, width + 10)          #設置x軸寬度限制
ax1.axis('off')                        #不顯示座標尺寸
ax1.set_title(title)                   #設定圖片標題，title上面有宣告過為""
	
ax2.set_ylim(height + 10, -10)
ax2.set_xlim(-10, width + 10)
ax2.axis('off')
ax2.set_title(title)

ax3.set_ylim(height + 10, -10)
ax3.set_xlim(-10, width + 10)
ax3.axis('off')
ax3.set_title(title)
	
ax4.set_ylim(height + 10, -10)
ax4.set_xlim(-10, width + 10)
ax4.axis('off')
ax4.set_title(title)	

masked_image1 = image1.astype(np.uint32).copy()         #np.numpy從中讀取數據並轉為numpy的數組  #將影像的型別轉變成32位元(整數)，並複製影像
masked_image2 = image2.astype(np.uint32).copy()
masked_image3 = image3.astype(np.uint32).copy()
masked_image4 = image4.astype(np.uint32).copy()



for j in range(1,5):
    print(j)
    boxes=eval('boxes'+str(j))                          #轉成boxes1變數  (為了能跑for迴圈讀變數(ax1、ax2、.....)   
    N = boxes.shape[0]                                  #N=影像中欲辨識的目標物
#   color = colors[j]  原先是random color
    
#   a="tom"+str(i)  #b=eval(a)  #print(b)  可轉成變數
    for i in range(N):
      
	    # 強制color標記設為紅色  ((M圖上為藍色
        color = (0.0, 0.0, 1.0)
	
		# Bounding box
        if not np.any(boxes):
			# Skip this instance. Has no bbox. Likely lost in image cropping.
            continue
        
        y1, x1, y2, x2 = boxes[i]                        #擷取bb的座標值
                                                         #在影像上框出目標物bb座標值
        if show_bbox:
            p = patches.Rectangle((x1, y1), x2 - x1, y2 - y1, linewidth=2,
									alpha=0.7, linestyle="dashed",
									edgecolor=color, facecolor='none') 					
            ax=eval('ax'+str(j))                         #變數累加((ax1、ax2
            ax.add_patch(p)                              #加到ax上
				
			# Label
        if not captions:
            class_ids=eval('class_ids'+str(j))           #變數累加((classid1、classid2
            class_id = class_ids[i]                   
            score = scores[i] if scores is not None else None
            label = class_names[class_id]              
            caption = "{} {:.3f}".format(label, score) if score else label
        else:
            caption = captions[i]
        ax.text(x1, y1 + 8, caption,
					color='w', size=11, backgroundcolor="none")	 #放置text

	    # Mask
        #mask=eval('mask'+str(j))
        masks=eval('masks'+str(j))                       #變數累加((mask1、mask2
        mask = masks[:, :, i]

		
        if show_mask:
            masked_image=eval('masked_image'+str(j))
            masked_image = apply_mask(masked_image, mask, color)
			# mask多邊形
			# 填充以確保接觸圖像邊緣的mask具有正確的多邊形。
			# Mask Polygon
			# Pad to ensure proper polygons for masks that touch image edges.
        padded_mask = np.zeros(
				(mask.shape[0] + 2, mask.shape[1] + 2), dtype=np.uint8)
        padded_mask[1:-1, 1:-1] = mask
        contours = find_contours(padded_mask, 0.5)
        for verts in contours:
				# Subtract the padding and flip (y, x) to (x, y)
            verts = np.fliplr(verts) - 1
            p = Polygon(verts, facecolor="none", edgecolor=color)
		
            ax.add_patch(p)

#純秀image + seg 鈣化點		
ax1.imshow(masked_image1.astype(np.uint8))
ax2.imshow(masked_image2.astype(np.uint8))
ax3.imshow(masked_image3.astype(np.uint8))
ax4.imshow(masked_image4.astype(np.uint8))

#將影像左右、上下合併  但缺少label
#leftright = np.hstack((masked_image1.astype(np.uint8), masked_image2.astype(np.uint8)))
#leftright_down = np.hstack((masked_image3.astype(np.uint8), masked_image4.astype(np.uint8)))
updown1 = np.vstack((masked_image1.astype(np.uint8),masked_image2.astype(np.uint8)))
updown2 = np.vstack((masked_image3.astype(np.uint8),masked_image4.astype(np.uint8)))
updown = np.vstack((updown1.astype(np.uint8),updown2.astype(np.uint8)))

# 能儲存影像跟mask  合圖
cv2.imwrite("./run/merge1.bmp", updown1)
cv2.imwrite("./run/merge2.bmp", updown2)
cv2.imwrite("./run/merge.bmp", updown)
cv2.imwrite("D:/Users/user/Desktop/maskRCNN/breast_ui/run/result/1195730/merge.bmp", updown)

crop_ori = skimage.io.imread('D:/Users/user/Desktop/maskRCNN/breast_ui/run/result/1195730/crop.bmp')

compared = np.hstack((crop_ori.astype(np.uint8),updown.astype(np.uint8)))
cv2.imwrite("D:/Users/user/Desktop/maskRCNN/breast_ui/run/result/1195730/compared.bmp", compared)


#僅能儲存影像跟mask (沒label
cv2.imwrite('./run/examples2.png', masked_image1.astype(np.uint8))    

#    要保持left<right ====>  即是保持"左側"和"底部"較小即可。
#    plt.subplots_adjust(left=0,bottom=0,top=1,right=0.5, wspace = 0,hspace = 0) 中間切割置左，左右間距較小 
#    plt.subplots_adjust(left=0.15,bottom=0,top=1,right=0.85, wspace = 0,hspace = 0) 等同 1,1
#    plt.subplots_adjust(left=0.1,bottom=0,top=1,right=1, wspace = 0,hspace = 0)   等同1,1 偏右     
#    plt.subplots_adjust(left=0,bottom=0,top=1,right=0.7, wspace = 0,hspace = 0)   等同1,1 偏左      
#    plt.subplots_adjust(left=0,bottom=0,top=1,right=0.6, wspace = 0,hspace = 0)  中間切割置左，上下間距較小      
#    plt.subplots_adjust(left=0,bottom=0,top=1,right=0.5,wspace = 0,hspace = 0)     #imshow最fit
plt.subplots_adjust(left=0,bottom=0,top=1,right=1,wspace = 0.01,hspace = 0.01)       #save最fit
plt.tight_layout()

#能儲存影像+標記+label  //matplotlib
plt.savefig('D:/Users/user/Desktop/maskRCNN/breast_ui/run/plot.png')  

#show 合併的image  
img = Image.open('D:/Users/user/Desktop/maskRCNN/breast_ui/run/merge.bmp')
#img.show()                      
                                    
    
#if auto_show:     #有這行才會show images
    #plt.show() 

