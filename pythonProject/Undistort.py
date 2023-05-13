import cv2
import numpy as np


def loadUndistortedImage(filename):
    # load image
    image = cv2.imread(r"C:\Users\adity\Downloads\36.jpg")
    # print(image)

    # set distortion coeff and intrinsic camera matrix (focal length, centerpoint offset, x-y skew)
    cameraMatrix = np.array([[1.89071621e+03, 0, 4.92307669e+02], [0, 4.24517610e+03, 3.27605142e+02], [0, 0, 1]])
    distCoeffs = np.array([[4.11479837e-01,-1.29690891e+01, -2.26993905e-03, 3.76154325e-03, 7.03416857e+01]])

    # setup enlargement and offset for new image
    y_shift = 60  # experiment with
    x_shift = 70  # experiment with
    imageShape = image.shape  # image.size
    print(imageShape)
    imageSize = (int(imageShape[0]) + 2 * y_shift, int(imageShape[1]) + 2 * x_shift, 3)
    print(imageSize)

    # create a new camera matrix with the principal point offest according to the offset above
    newCameraMatrix, validPixROI = cv2.getOptimalNewCameraMatrix(cameraMatrix, distCoeffs, imageSize,
                                                                 1)
    # newCameraMatrix = cv2.getDefaultNewCameraMatrix(cameraMatrix, imageSize, True) # imageSize, True

    # create undistortion maps
    R = np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]])
    map1, map2 = cv2.initUndistortRectifyMap(cameraMatrix, distCoeffs, R, newCameraMatrix, imageSize,
                                             cv2.CV_16SC2)

    # remap
    outputImage = cv2.remap(image, map1, map2, INTER_LINEAR)
    # save output image as file with "FIX" appened to name - only works with .jpg files at the moment
    index = filename.find(r"C:\Users\adity\Downloads\36.jpg")
    fixed_filename = filename[:index] + '_undistorted' + fileName[index:]
    cv2.imwrite(fixed_filename, outputImage)
    cv2.imshow('fix_img', outputImage)
    cv2.waitKey(0)
    return


# Undistort the images, then save the restored images
loadUndistortedImage('./calib/WIN_20200626_11_29_16_Pro.jpg')