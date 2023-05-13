import cv2
import numpy as np
import cv2.aruco



# Load Aruco Detector

parameters= cv2.aruco.DetectorParameters_create()
aruco_dict= cv2.aruco.Dictionary_get(cv2.aruco.DICT_6X6_50)


class HomogeneousBgDetector():
    def __init__(self):
        pass

    def detect_objects(self, frame):
        # Convert Image to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Create a Mask with adaptive threshold
        mask = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 19, 5)

        # Find contours
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # cv2.imshow("mask", mask)
        objects_contours = []

        for cnt in contours:
            area = cv2.contourArea(cnt)
            if area > 2000:
                cnt = cv2.approxPolyDP(cnt, 0.03*cv2.arcLength(cnt, True), True)
                objects_contours.append(cnt)

        return objects_contours


# Load Object Detector
detector = HomogeneousBgDetector()

# Load Image
img = cv2.imread(r"C:\Users\adity\Downloads\im06.jpg")
img = cv2.resize(img, (1000, 600))

#Get ArUco marker
corners, _, _ = cv2.aruco.detectMarkers(img, aruco_dict, parameters=parameters)

#Draw polygon around the marker
int_corners=np.int0(corners)
#print(int_corners)
cv2.polylines(img, int_corners, True, (0, 255, 0), 1)

#Aruco Perimeter
aruco_perimeter = cv2.arcLength(corners[0], True)
print(aruco_perimeter)

#Pixel to cm ratio
pixel_cm_ratio = aruco_perimeter/17.6

#print(pixel_cm_ratio)

contours = detector.detect_objects(img)

# Draw object boundaries
for cnt in contours:
    # Get rectangle
    rect = cv2.minAreaRect(cnt)
    (x, y), (w, h), angle =rect


    #Get Width and Height of the obj by applying the ratio pixel to cm
    object_width = w / pixel_cm_ratio
    object_height = h / pixel_cm_ratio
    object_xcoor = x / pixel_cm_ratio
    object_ycoor = y/ pixel_cm_ratio


    # Display Rectangle
    box = cv2.boxPoints(rect)
    box = np.int0(box)

    cv2.circle(img, (int(x), int(y)), 5, (0, 0, 255), -1)
    cv2.polylines(img, [box], True, (255, 0, 0), 1)
    cv2.putText(img, "Width {} cm".format(round(object_width, 1)), (int(x), int(y - 15)), cv2.FONT_HERSHEY_PLAIN, 1, (100, 200, 0), 2)
    cv2.putText(img, "Height {} cm".format(round(object_height, 1)), (int(x), int(y + 15)), cv2.FONT_HERSHEY_PLAIN, 1, (100, 200, 0), 2)
    cv2.putText(img, "x {} cm".format(round(object_xcoor, 1)), (int(x), int(y - 40)), cv2.FONT_HERSHEY_PLAIN, 1, (100, 200, 0), 2)
    cv2.putText(img, "y {} cm".format(round(object_ycoor, 1)), (int(x), int(y + 40)), cv2.FONT_HERSHEY_PLAIN, 1, (100, 200, 0), 2)
    cv2.putText(img, "angle".format(round(angle, 1)), (int(x), int(y + 60)), cv2.FONT_HERSHEY_PLAIN, 1, (100, 200, 0), 2)


#print(box)
#print(x, y)
#print(w, h)
print(angle)


cv2.imshow("Image", img)
cv2.waitKey(0)
