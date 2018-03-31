import cv2
import numpy as np
from matplotlib import pyplot as plt

fileName = './images/test.png'

# Parametros que indican cuan largo es respecto a su ancho.
cigarRatio = 8
habanoRatio = 3.5

# Referencias de colores HSV de cada objeto a clasificar.
# cigarHSV = 101, 50, 215
# puroHSV = 109, 131, 158
# jointHSV = 100, 22, 187
# habanoHSV = 107, 116, 145

# Esta función retorna una porción especifíca de una imagen dada.
def cropRectangle(img, rect, box):
    angle = rect[2]
    rows, cols = img.shape[0], img.shape[1]
    M = cv2.getRotationMatrix2D((cols/2, rows/2), angle, 1)
    rotatedImage = cv2.warpAffine(img, M, (cols, rows))

    # Rotamos la imagen segun el angulo de inclinacion del rectángulo obtenido con minAreaRect().
    # Esto lo hacemos para poder cortar la imagen inclinada correspondiente de forma horizontal / vertical.
    pts = np.int0(cv2.transform(np.array([box]), M))[0]    
    pts[pts < 0] = 0

    croppedImage = rotatedImage[pts[1][1]:pts[0][1], pts[1][0]:pts[2][0]]

    return croppedImage

# Esta función retorna el color para pintar los contornos dependiendo de las características detectadas.
def classificate(width, height, roi):
    if width > height:
        ratio = width / height
    else:
        ratio = height / width

    # Tomamos el color promedio de la porción de la imagen proporcionada y lo convertimos a HSV.
    b,g,r,_ = np.uint8(cv2.mean(roi))
    hsv = cv2.cvtColor(np.uint8([[[b,g,r]]]), cv2.COLOR_BGR2HSV)
    h = hsv[0][0][0]
    s = hsv[0][0][1]
    v = hsv[0][0][2]

    if ratio > cigarRatio:
        # Debemos clasificar entre purito y cigarrillo. Ver valores aproximados al inicio del código.
        if s < 90 and v > 190:
            color = [255, 0, 0] # Cigarrillo
        else:
            color = [255, 0, 255] # Purito

    elif ratio > habanoRatio:
        # Debemos clasificar entre habano y porro. Ver valores aproximados al inicio del código.
        if h < 103 and s < 75:
            color = [0, 255, 0] # Porro
        else:
            color = [0, 255, 255] # Habano
    else:
        color = [0, 0, 255] # Pipa
    return color

# Nos retorna el ancho y el largo del rectángulo dado.
def getRectangleValues(rectangle):
    width = rectangle[1][0]
    height = rectangle[1][1]
    return width, height

if __name__ == "__main__":
    origImage = cv2.imread(fileName)
    rgbImage = cv2.cvtColor(origImage, cv2.COLOR_BGR2RGB)
    image = cv2.cvtColor(origImage, cv2.COLOR_BGR2GRAY)
    # Aplicamos opening para eliminar las manchas de los cigarrillos y las líneas en las etiquetas de los habanos.
    opening = cv2.morphologyEx(image, cv2.MORPH_OPEN, np.ones((7, 7), np.uint8))
    # Aplicamos threshold de 245 para diferenciar los objetos del fondo (255).
    ret, thresh1 = cv2.threshold(opening, 245, 255, cv2.THRESH_BINARY_INV)
    (_,contour,_) = cv2.findContours(thresh1, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for i in range(len(contour)):
        cnt = contour[i]
        # Tomamos el rectangulo que encierra al objeto con la menor área.
        rect = cv2.minAreaRect(cnt)
        width, height = getRectangleValues(rect)
        
        if width != 0 and height != 0:
            # Cortamos, clasificamos y pintamos la caja (box) sobre la imagen RGB original.
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