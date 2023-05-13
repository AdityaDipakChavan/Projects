import cv2
import numpy as np
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
                # cnt = cv2.approxPolyDP(cnt, 0.03*cv2.arcLength(cnt, True), True)
                objects_contours.append(cnt)

        return objects_contours


# Load Object Detector
detector = HomogeneousBgDetector()

# Load Image
img = cv2.imread(r"C:\Users\adity\Downloads\IMG_20220430_103139.jpg")
img = cv2.resize(img, (1000, 600))

contours = detector.detect_objects(img)

# Draw object boundaries
for cnt in contours:
    # Get rectangle
    rect = cv2.minAreaRect(cnt)
    (x, y), (w, h), angle = rect

    # Display Rectangle
    box = cv2.boxPoints(rect)
    box = np.int0(box)

    cv2.circle(img, (int(x), int(y)), 5, (0, 0, 255), -1)
    cv2.polylines(img, [box], True, (255, 0, 0), 1)
    cv2.putText(img, "Width {} ".format(round(w, 1)), (int(x), int(y - 15)), cv2.FONT_HERSHEY_PLAIN, 1, (100, 200, 0), 2)
    cv2.putText(img, "Height {} ".format(round(h, 1)), (int(x), int(y + 15)), cv2.FONT_HERSHEY_PLAIN, 1, (100, 200, 0), 2)
    cv2.putText(img, "x {} ".format(round(x, 1)), (int(x), int(y - 40)), cv2.FONT_HERSHEY_PLAIN, 1, (100, 200, 0), 2)
    cv2.putText(img, "y {} ".format(round(y, 1)), (int(x), int(y + 40)), cv2.FONT_HERSHEY_PLAIN, 1, (100, 200, 0), 2)
    cv2.putText(img, "Angle".format(round(angle, 1)), (int(x), int(y + 60)), cv2.FONT_HERSHEY_PLAIN, 1, (100, 200, 0), 2)
print(x, y)
print(w, h)
print(angle)

cv2.imshow("Image", img)
cv2.waitKey(0)
