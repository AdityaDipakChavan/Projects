
import imutils
from imutils.perspective import four_point_transform
import cv2
import numpy as np
from pathlib import Path
import os
#################################################################
# Load the Image
#################################################################
height = 800
width = 600
green = (0, 255, 0)

image = cv2.imread(r"C:\Users\adity\Downloads\IMG_20220510_220334.jpg")
image = cv2.resize(image, (width, height))
orig_image = image.copy()
height, width, channels = image.shape  # Find Height And Width Of Image

#################################################################
# Image Processing
#################################################################

gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) # convert the image to gray scale
blur = cv2.GaussianBlur(gray, (5, 5), 0) # Add Gaussian blur
edged = cv2.Canny(blur, 75, 200) # Apply the Canny algorithm to find the edges

# Show the image and the edges
cv2.imshow('Original image:', image)
cv2.imshow('Edged:', edged)
cv2.waitKey(0)
cv2.destroyAllWindows()

#################################################################
# Use the Edges to Find all the Contours
#################################################################

contours, _ = cv2.findContours(edged, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
contours = sorted(contours, key=cv2.contourArea, reverse=True)

# Show the image and all the contours
cv2.imshow("Image", image)
cv2.drawContours(image, contours, -1, green, 3)
cv2.imshow("All contours", image)
cv2.waitKey(0)
cv2.destroyAllWindows()

#################################################################
# Select Only the Edges of the Document
#################################################################

# go through each contour
#for contour in contours:
    # we approximate the contour
    #peri = cv2.arcLength(contour, True)
    #approx = cv2.approxPolyDP(contour, 0.05 * peri, True)
    # if we found a countour with 4 points we break the for loop
    # (we can assume that we have found our document)
    #if len(approx) == 4:

       # break
areas = [cv2.contourArea(c) for c in contours]
max_index = np.argmax(areas)
print(max_index)


epsilon = 0.1 * cv2.arcLength(contours[max_index], True)
approx = cv2.approxPolyDP(contours[max_index], epsilon, True)

#################################################################
# Apply Warp Perspective to Get the Top-Down View of the Document
#################################################################

# We draw the contours on the original image not the modified one
#cv2.drawContours(orig_image, doc_cnts, -1, green, 3)
#cv2.imshow("Contours of the document", orig_image)
# apply warp perspective to get the top-down view
#warped = four_point_transform(orig_image, doc_cnts.reshape(4, 2))
# convert the warped image to grayscale
#warped = cv2.cvtColor(warped, cv2.COLOR_BGR2GRAY)
#cv2.imshow("Scanned", cv2.resize(warped, (600, 800)))
#cv2.waitKey(0)
#cv2.destroyAllWindows()

# Crop The Image To approxPoly
pts1 = np.float32(approx)
pts = np.float32([[0, 0], [width, 0], [width, height], [0, height]])
matrix = cv2.getPerspectiveTransform(pts1, pts)
result = cv2.warpPerspective(image, matrix, (600, 800))

flip = cv2.flip(result, 1)  # Flip Image
rotate = cv2.rotate(flip, cv2.ROTATE_90_COUNTERCLOCKWISE)  # Rotate Image

cv2.imshow('Result', rotate)
cv2.imwrite('Scan ho gya.jpg', rotate)

cv2.waitKey(0)
cv2.destroyAllWindows()
