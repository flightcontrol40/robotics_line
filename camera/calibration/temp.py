from __future__ import print_function

import argparse
import random as rng
from pathlib import Path

import cv2 as cv
import numpy as np

rng.seed(12345)
SHOW_CANNY = False
IMAGE = None
IMAGE_GRAYSCALE = None
BLUR_GRAYSCALE = None
X_BLUR = 7
Y_BLUR = 7
CIRCLE_DIST = 1
HSV_MIN = np.array([40, 138, 1])
HSV_MAX = np.array([255, 255, 102])
COLOR_MASK = np.zeros((300, 512, 3), np.uint8)


def thresh_callback(val):
    threshold = val
    global \
        SHOW_CANNY, \
        BLUR_GRAYSCALE, \
        X_BLUR, \
        Y_BLUR, \
        IMAGE_GRAYSCALE, \
        IMAGE, \
        CIRCLE_DIST, \
        HSV_MIN, \
        HSV_MAX, \
        COLOR_MASK

    m1 = cv.Canny(COLOR_MASK, 50, 100)
    contours_1, hierarchy = cv.findContours(
        m1, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE
    )
    cv.imshow("MASK", m1)

    output = IMAGE.copy()

    bound_rect: list[cv.typing.Rect] = []
    for i, c in enumerate(contours_1):
        area = cv.contourArea(c)
        if area < 100:
            continue
        contours_poly = cv.approxPolyDP(c, 3, True)
        bound_rect.append(cv.boundingRect(contours_poly))

    for i in range(len(bound_rect)):
        print(int(bound_rect[i][0]), int(bound_rect[i][1]))
        cv.rectangle(
            output,
            # p1,p2
            (int(bound_rect[i][0])-5, int(bound_rect[i][1])-5),
            (
                int(bound_rect[i][0] + bound_rect[i][2])+5,
                int(bound_rect[i][1] + bound_rect[i][3])+5,
            ),
            (0, 0, 0),
            2,
        )

    cv.imshow("OUTPUT", output)

    # BLUR_GRAYSCALE = cv.blur(IMAGE_GRAYSCALE, (X_BLUR, Y_BLUR))

    canny_output = m1

    if SHOW_CANNY:
        contours, _ = cv.findContours(
            canny_output, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE
        )

        contours_poly = [None] * len(contours)
        bound_rect = [None] * len(contours)
        centers = [None] * len(contours)
        radius = [None] * len(contours)
        for i, c in enumerate(contours):
            contours_poly[i] = cv.approxPolyDP(c, 3, True)
            bound_rect[i] = cv.boundingRect(contours_poly[i])
            centers[i], radius[i] = cv.minEnclosingCircle(contours_poly[i])

        drawing = np.zeros(
            (canny_output.shape[0], canny_output.shape[1], 3), dtype=np.uint8
        )
        for i in range(len(contours)):
            color = (rng.randint(0, 256), rng.randint(0, 256), rng.randint(0, 256))
            cv.drawContours(drawing, contours_poly, i, color)

        cv.imshow("Contours", drawing)

    else:
        cv.imshow("Contours", canny_output)


def check_boundaries(value, tolerance, ranges, upper_or_lower):
    if ranges == 0:
        # set the boundary for hue
        boundary = 180
    elif ranges == 1:
        # set the boundary for saturation and value
        boundary = 255

    if(value + tolerance > boundary):
        value = boundary
    elif (value - tolerance < 0):
        value = 0
    else:
        if upper_or_lower == 1:
            value = value + tolerance
        else:
            value = value - tolerance
    return value

image_hsv = None
pixel = (0,0,0) #RANDOM DEFAULT VALUE

def pick_color(event,x,y,flags,param):
    global HSV_MAX, HSV_MIN, COLOR_MASK
    if event == cv.EVENT_LBUTTONDOWN:
        pixel = image_hsv[y,x]

        #HUE, SATURATION, AND VALUE (BRIGHTNESS) RANGES. TOLERANCE COULD BE ADJUSTED.
        # Set range = 0 for hue and range = 1 for saturation and brightness
        # set upper_or_lower = 1 for upper and upper_or_lower = 0 for lower
        hue_upper = check_boundaries(pixel[0], 10, 0, 1)
        hue_lower = check_boundaries(pixel[0], 10, 0, 0)
        saturation_upper = check_boundaries(pixel[1], 10, 1, 1)
        saturation_lower = check_boundaries(pixel[1], 10, 1, 0)
        value_upper = check_boundaries(pixel[2], 40, 1, 1)
        value_lower = check_boundaries(pixel[2], 40, 1, 0)

        upper =  np.array([hue_upper, saturation_upper, value_upper])
        lower =  np.array([hue_lower, saturation_lower, value_lower])
        print(lower, upper)
        HSV_MAX = upper
        HSV_MIN = lower
        #A MONOCHROME MASK FOR GETTING A BETTER VISION OVER THE COLORS 
        
        cv.setTrackbarPos("H", "Color Threshold Max", hue_upper)
        cv.setTrackbarPos("S", "Color Threshold Max", saturation_upper)
        cv.setTrackbarPos("V", "Color Threshold Max", value_upper)
        cv.setTrackbarPos("H", "Color Threshold Min", hue_lower)
        cv.setTrackbarPos("S", "Color Threshold Min", saturation_lower)
        cv.setTrackbarPos("V", "Color Threshold Min", value_lower)
        nothing(0)


def show_canny_callback(*args, **kwargs):
    global SHOW_CANNY
    SHOW_CANNY = not SHOW_CANNY
    t = cv.getTrackbarPos("Canny thresh:", source_window)
    thresh_callback(t)


def blur_x_callback(i):
    if i % 2 == 0:
        i = i + 1
    global X_BLUR
    X_BLUR = i
    t = cv.getTrackbarPos("Canny thresh:", source_window)
    thresh_callback(t)


def blur_y_callback(i):
    if i % 2 == 0:
        i = i + 1
    global Y_BLUR
    Y_BLUR = i
    t = cv.getTrackbarPos("Canny thresh:", source_window)
    thresh_callback(t)


def nothing(x):
    global HSV_MAX, HSV_MIN, COLOR_MASK
    h = cv.getTrackbarPos("H", "Color Threshold Min")
    s = cv.getTrackbarPos("S", "Color Threshold Min")
    v = cv.getTrackbarPos("V", "Color Threshold Min")

    HSV_MIN = np.array([h, s, v])
    min_img = np.zeros((300, 512, 3), np.uint8)
    min_img[:] = list(HSV_MIN)

    cv.imshow("Color Threshold Min", min_img)
    h = cv.getTrackbarPos("H", "Color Threshold Max")
    s = cv.getTrackbarPos("S", "Color Threshold Max")
    v = cv.getTrackbarPos("V", "Color Threshold Max")

    HSV_MAX = np.array([h, s, v])
    max_img = np.zeros((300, 512, 3), np.uint8)
    max_img[:] = list(HSV_MAX)

    image_mask = cv.inRange(image_hsv,HSV_MIN,HSV_MAX)
    COLOR_MASK = image_mask
    cv.imshow("Color Mask", image_mask)

    cv.imshow("Color Threshold Max", max_img)

    t = cv.getTrackbarPos("Canny thresh:", source_window)
    thresh_callback(t)


parser = argparse.ArgumentParser(
    description="Code for Creating Bounding boxes and circles for contours tutorial."
)
parser.add_argument("input", help="Path to input image.")
args = parser.parse_args()

if args.input is None:
    print("Could not open or find the image:", args.input)
    exit(0)

img_path = Path(args.input)

src = cv.imread(str(img_path))
IMAGE = src

# Convert image to gray and blur it
IMAGE_GRAYSCALE = cv.cvtColor(IMAGE, cv.COLOR_BGR2GRAY)

source_window = "Source"
cv.namedWindow(source_window, cv.WINDOW_NORMAL)
cv.imshow(source_window, IMAGE)
max_thresh = 255
thresh = 125  # initial threshold

cv.namedWindow("Color Threshold Min")
cv.namedWindow("Color Threshold Max")

cv.createTrackbar("H", "Color Threshold Min", HSV_MIN[0], 255, nothing)
cv.createTrackbar("S", "Color Threshold Min", HSV_MIN[1], 255, nothing)
cv.createTrackbar("V", "Color Threshold Min", HSV_MIN[2], 255, nothing)

cv.createTrackbar("H", "Color Threshold Max", HSV_MAX[0], 255, nothing)
cv.createTrackbar("S", "Color Threshold Max", HSV_MAX[1], 255, nothing)
cv.createTrackbar("V", "Color Threshold Max", HSV_MAX[2], 255, nothing)

cv.createTrackbar("Canny thresh:", source_window, thresh, max_thresh, thresh_callback)
cv.createTrackbar("Blur-x:", source_window, 0, 100, blur_x_callback)
cv.createTrackbar("Blur-y:", source_window, 0, 100, blur_y_callback)
cv.createTrackbar("Show Canny", source_window, 0, 1, show_canny_callback)


image_hsv = cv.cvtColor(IMAGE,cv.COLOR_BGR2HSV)
cv.setMouseCallback(source_window, pick_color)
nothing(0)
thresh_callback(thresh)
cv.waitKey()
