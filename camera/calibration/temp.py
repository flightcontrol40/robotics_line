import cv2 as cv

img_path = r"/home/nathan/robotics_line/camera/calibration/output/f0/img_00.png"

img = cv.imread(img_path)
crop = img[600:900, 50:350]


cv.imshow("crop",crop)
cv.waitKey(0)
cv.destroyAllWindows()