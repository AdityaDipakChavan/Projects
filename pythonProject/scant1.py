#################################################################
# Load the Image
#################################################################
import imutils
from imutils.perspective import four_point_transform
import cv2
from pathlib import Path
import os

height = 800
width = 600
green = (0, 255, 0)

image = cv2.imread(r"C:\Users\adity\Downloads\IMG_20220510_220334.jpg")
image = cv2.resize(image, (width, height))
orig_image = image.copy()

#################################################################
# Image Processing
#################################################################

gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) # convert the image to gray scale
blur = cv2.GaussianBlur(gray, (5, 5), 0) # Add Gaussian blur
edged = cv2.Canny(blur, 165, 165) # Apply the Canny algorithm to find the edges

# Show the image and the edges
cv2.imshow('Original image:', image)
cv2.imshow('Edged:', edged)
cv2.waitKey(0)
cv2.destroyAllWindows()

#################################################################
# Use the Edges to Find all the Contours
#################################################################

# If you are using OpenCV v3, v4-pre, or v4-alpha
# cv.findContours returns a tuple with 3 element instead of 2
# where the `contours` is the second one
# In the version OpenCV v2.4, v4-beta, and v4-official
# the function returns a tuple with 2 element
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
for cnt in contours:
    # we approximate the contour
    area = cv2.contourArea(cnt)
    if area > 2000:
        cnt = cv2.approxPolyDP(cnt, 0.03 * cv2.arcLength(cnt, True), True)
    # if we found a countour with 4 points we break the for loop
    # (we can assume that we have found our document)

    break

#################################################################
# Apply Warp Perspective to Get the Top-Down View of the Document
#################################################################

# We draw the contours on the original image not the modified one
cv2.drawContours(orig_image, cnt, -1, green, 3)
cv2.imshow("Contours of the document", orig_image)
# apply warp perspective to get the top-down view
warped = four_point_transform(orig_image, cnt.reshape(8, 4))
# convert the warped image to grayscale
warped = cv2.cvtColor(warped, cv2.COLOR_BGR2GRAY)
cv2.imshow("Scanned", cv2.resize(warped, (600, 800)))
cv2.waitKey(0)
cv2.destroyAllWindows()

