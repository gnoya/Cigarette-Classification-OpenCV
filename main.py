import cv2
import numpy as np
from matplotlib import pyplot as plt

fileName = './images/test.png'

def autoCanny(image, sigma = 0.33):
    v = np.median(image)
    lower = int(max(0, (1.0 - sigma) * v))
    upper = int(min(255, (1.0 + sigma) * v))
    edged = cv2.Canny(image, lower, upper)
    return edged

if __name__ == "__main__":
    origImage = cv2.imread(fileName)
    image = cv2.cvtColor(origImage, cv2.COLOR_BGR2GRAY)

    opening = cv2.morphologyEx(image, cv2.MORPH_OPEN, np.ones((7, 7), np.uint8))
    # blur = cv2.GaussianBlur(opening,(5,5),0)
    ret3, thresholdImage = cv2.threshold(opening, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    edged = autoCanny(thresholdImage)

    plt.figure(1)
    plt.title('Imagen con Canny')
    plt.imshow(edged, cmap='gray')

    (_,contour,_) = cv2.findContours(edged, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for i in range(len(contour)):
        cnt = contour[i]
        rect = cv2.minAreaRect(cnt)
        box = cv2.boxPoints(rect)
        box = np.int0(box)
        cv2.drawContours(origImage, [box], 0, (0, 255 , 0), 2)

    rgbImage = cv2.cvtColor(origImage, cv2.COLOR_BGR2RGB)

    plt.figure(2)
    plt.title('Imagen original marcada')
    plt.imshow(rgbImage)
    plt.show()