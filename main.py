import cv2
import numpy as np
from matplotlib import pyplot as plt

fileName = './images/test.png'
cigarRatio = 8
habanoRatio = 3.5

# cigarH = 101
# cigarS = 50
# cigarV = 215

# puroH = 109
# puroS = 131
# puroV = 158

# jointH = 100
# jointS = 22
# jointV = 187

# habanoH = 107
# habanoS = 116
# habanoV = 145

def cropRectangle(img, rect, box):

    # rotate img
    angle = rect[2]
    rows, cols = img.shape[0], img.shape[1]
    M = cv2.getRotationMatrix2D((cols/2, rows/2), angle, 1)
    rotatedImage = cv2.warpAffine(img, M, (cols, rows))

    # rotate bounding box
    pts = np.int0(cv2.transform(np.array([box]), M))[0]    
    pts[pts < 0] = 0

    # crop
    croppedImage = rotatedImage[pts[1][1]:pts[0][1], 
                       pts[1][0]:pts[2][0]]

    return croppedImage

def autoCanny(image, sigma = 0.33):
    v = np.median(image)
    lower = int(max(0, (1.0 - sigma) * v))
    upper = int(min(255, (1.0 + sigma) * v))
    edged = cv2.Canny(image, lower, upper)
    return edged

def classificate(width, height, roi):
    if width > height:
        ratio = width / height
    else:
        ratio = height / width

    b,g,r,_=np.uint8(cv2.mean(roi))
    hsv = cv2.cvtColor(np.uint8([[[b,g,r]]]),cv2.COLOR_BGR2HSV)
    h = hsv[0][0][0]
    s = hsv[0][0][1]
    v = hsv[0][0][2]

    if ratio > cigarRatio:
        # Debemos clasificar entre purito y cigarrillo. Ver valores aproximados al inicio del codigo.
        if s < 90 and v > 190:
            color = [255, 0, 0] # Cigarrillo
        else:
            color = [255, 0, 255] # Purito

    elif ratio > habanoRatio:
        # Debemos clasificar entre habano y porro. Ver valores aproximados al inicio del codigo.
        if h < 103 and s < 75:
            color = [0, 255, 0] # Porro
        else:
            color = [0, 255, 255] # Habano
    else:
        color = [0, 0, 255] # Pipa
    return color

def getRectangleValues(rectangle):
    width = rectangle[1][0]
    height = rectangle[1][1]
    x = int(rectangle[0][0])
    y = int(rectangle[0][1])
    return width, height, x, y

if __name__ == "__main__":
    origImage = cv2.imread(fileName)
    rgbImage = cv2.cvtColor(origImage, cv2.COLOR_BGR2RGB)
    image = cv2.cvtColor(origImage, cv2.COLOR_BGR2GRAY)
    opening = cv2.morphologyEx(image, cv2.MORPH_OPEN, np.ones((7, 7), np.uint8))
    
    # ret3, thresholdImage = cv2.threshold(opening, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    ret, thresh1 = cv2.threshold(opening, 245, 255, cv2.THRESH_BINARY)
    edged = autoCanny(thresh1)

    (_,contour,_) = cv2.findContours(edged, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for i in range(len(contour)):
        cnt = contour[i]
        rect = cv2.minAreaRect(cnt)
        width, height, x, y = getRectangleValues(rect)
        
        if width != 0 and height != 0:
            box = cv2.boxPoints(rect)
            box = np.int0(box)
            roi = cropRectangle(rgbImage, rect, box)
            color = classificate(width, height, roi)
            cv2.drawContours(rgbImage, [box], 0, color, 2)

    plt.figure(1)
    plt.title('Threshold')
    plt.imshow(thresh1, cmap='gray')
    plt.figure(2)
    plt.title('Imagen clasificada')
    plt.imshow(rgbImage)
    plt.show()