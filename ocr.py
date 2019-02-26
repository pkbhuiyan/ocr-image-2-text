from PIL import Image
import pytesseract
import argparse
import cv2
import os
import numpy as np

# arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True,
	help="path to input image to be OCR'd")
ap.add_argument("-p", "--preprocess", type=str, default="thresh",help="type of preprocessing to be done")
args = vars(ap.parse_args())

im = Image.open(args["image"])
image = cv2.imread(args["image"])


gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
cv2.imshow("Image", gray)


# threshing the image
if args["preprocess"] == "thresh":
        gray = cv2.threshold(gray, 0, 255,cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
        # gray = cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,11,2)
        # gray = cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,11,2)
# adative
elif args["preprocess"] == "gaus":
    gray = cv2.GaussianBlur(gray,(5,5),1)
# bluring the image
elif args["preprocess"] == "blur":
	gray = cv2.medianBlur(gray, 3)
elif args["preprocess"] == "bitwise":
	gray = cv2.bitwise_not(gray,gray)
elif args["preprocess"] == "bilfil":
    gray = cv2.bilateralFilter(gray, 9, 75, 75)

# create local image
filename = "{}.png".format(os.getpid())
cv2.imwrite(filename, gray)

# apply ocr + delete local image
text = pytesseract.image_to_string(Image.open(filename))
os.remove(filename)
print(text)

cv2.imshow("Output", gray)
cv2.waitKey(0)
