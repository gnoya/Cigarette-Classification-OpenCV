import cv2
import numpy as np
from matplotlib import pyplot as plt

fileName = './images/test2.png'

def autoCanny(image, sigma = 0.33):
    v = np.median(image)
    lower = int(max(0, (1.0 - sigma) * v))
    upper = int(min(255, (1.0 + sigma) * v))
    edged = cv2.Canny(image, lower, upper)
    return edged

if __name__ == "__main__":
    origImage = cv2.imread(fileName)
    image = cv2.cvtColor(origImage, cv2.COLOR_BGR2GRAY)
    rgbImage = cv2.cvtColor(origImage, cv2.COLOR_BGR2RGB)
    opening = cv2.morphologyEx(image, cv2.MORPH_OPEN, np.ones((7, 7), np.uint8))
    
    ret3, thresholdImage = cv2.threshold(opening, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    edged = autoCanny(thresholdImage)

    (_,contour,_) = cv2.findContours(edged, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for i in range(len(contour)):
        cnt = contour[i]
        rect = cv2.minAreaRect(cnt)
        width = rect[1][0]
        height = rect[1][1]
        if width != 0 and height != 0:
            box = cv2.boxPoints(rect)
            box = np.int0(box)

            if width > height:
                ratio = width / height
            else:
                ratio = height / width

            if ratio > 8.5:
                color = [255, 0, 0]
            elif ratio > 6:
                color = [0, 255, 0]
            else:
                color = [0, 0, 255]

            cv2.drawContours(rgbImage, [box], 0, color, 2)

    plt.figure(1)
    plt.title('Size Test')
    plt.imshow(thresholdImage, cmap='gray')
    plt.show()