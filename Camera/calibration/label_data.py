import shutil
from pathlib import Path

import cv2 as cv
import numpy as np

IMAGES_DIR = Path(r"C:\Users\natha\Documents\robotics_line\Camera\calibration\output\clean")
OUTPUT_COMBINED = Path(r"C:\Users\natha\Documents\robotics_line\Camera\calibration\output\dataset")
OUTPUT_COMBINED.mkdir(parents=True, exist_ok=True)
IMG_PATH = Path(r"C:\Users\natha\Documents\robotics_line\Camera\calibration")

HSV_THRESH = (124, 93, 0, 255, 255, 96)
# HSV_MAX = (HSV_THRESH[0], HSV_THRESH[1], HSV_THRESH[2])
# HSV_MIN = (HSV_THRESH[3], HSV_THRESH[4], HSV_THRESH[5])
HSV_MIN = np.array([6, 30, 72])
HSV_MAX = np.array([70, 255, 255])

def _get_area(bound_rect):
    x1 = bound_rect[0]
    y1 = bound_rect[1]

    x2 = bound_rect[0] + bound_rect[2]
    y2 = bound_rect[1] + bound_rect[3]
    w1 = x1-x2
    h1 = y1-y2
    area = w1*h1
    return area

def get_bounding_box(path: Path):

    # This function should return the bounding box of the object in the image
    img = cv.imread(str(path), cv.IMREAD_COLOR_BGR)
    # cv.imshow("original", img)
    image_hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)
    # cv.imshow("hsv", image_hsv)
    image_mask = cv.inRange(image_hsv, HSV_MIN, HSV_MAX)
    # cv.imshow("mask", image_mask)
    m1 = cv.Canny(image_mask, 10, 20)
    contours, hierarchy = cv.findContours(
        m1, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE
    )
    # cv.imshow("canny",m1)
    height, width, channels = img.shape

    # print(f"size:  {height, width, channels}")


    output = img.copy()

    bound_rect: list[cv.typing.Rect] = []
    for i, c in enumerate(contours):

        contours_poly = cv.approxPolyDP(c, 3, True)
        bound_rect.append(cv.boundingRect(contours_poly))

    if len(bound_rect) > 1:
        bound_rect = sorted(bound_rect, key=_get_area, reverse=True)


    x1 = bound_rect[0][0]-5
    y1 = bound_rect[0][1]-5

    x2 = bound_rect[0][0]+5 + bound_rect[0][2]+5
    y2 = bound_rect[0][1]+5 + bound_rect[0][3]+5
    w1 = x2-x1
    h1 = y2-y1
    area = w1*h1
    # print(f"height: {h1}, width: {w1}, ")
    # print(f"area: {area}")

    # print(f"bounding box: {x1, y1, x2, y2}")
    # print(f"normalized: {x1/width, y1/height, x2/width, y2/height}")
    cv.rectangle(
        output,
        # p1,p2
        (int(x1), int(y1)),
        (int(x2), int(y2)),
        (0, 0, 0),
        2,
    )
        
    center_x, center_y = ( np.average([x1/width, x2/width]), np.average([y1/height, y2/height]))
    if area < 5000:
        cv.imshow("output", output)
        cv.waitKey(0)
    # Yolo wants class_id x_center y_center width height all normalized
    cords = f"{center_x:.6f} {center_y:.6f} {w1/width:.6f} {h1/height:.6f}"
    return cords


set_number = 0
current_set = "0"
for idx, f_path in enumerate(IMAGES_DIR.glob("**\*.png")):
    cords = get_bounding_box(f_path)
    img = f_path.relative_to(IMAGES_DIR)
    print(img)
    print(img.parts)

    if current_set != img.parts[0]:
        current_set = img.parts[0]
        set_number = 0
    set_number += 1


    if img.parts[0] == "1":
        
        new_name = f"one_{img.parts[1].split(".")[0]}"
    elif img.parts[0] == "2":
        new_name = f"two_{img.parts[1].split(".")[0]}"
    elif img.parts[0] == "3":
        new_name = f"three_{img.parts[1].split(".")[0]}"
    elif img.parts[0] == "4":
        new_name = f"four_{img.parts[1].split(".")[0]}"
    elif img.parts[0] == "5":
        new_name = f"five_{img.parts[1].split(".")[0]}"
    elif img.parts[0] == "6":
        new_name = f"six_{img.parts[1].split(".")[0]}"
    else:
        raise ValueError(f"Unknown image folder {img.parts[0]}")
    cords = f"{int(img.parts[0])-1} " + cords

    if set_number < 80:
        save_type =  "train"
    else:
        save_type = "val"


    print(cords)
    # Copy the image to the output directory
    output_file = OUTPUT_COMBINED / "images" / save_type/ f"{new_name}.png"
    output_file.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(
        f_path,
        output_file
    )
    
    # Copy the label file to the output directory
    output_file = OUTPUT_COMBINED / "labels" / save_type / f"{new_name}.txt"
    output_file.parent.mkdir(parents=True, exist_ok=True)
    with open(output_file, "w") as f:
        f.write(cords)


    # cv.waitKey()



    # shutil.copyfile(
    #     IMAGES_DIR / img,
    #     OUTPUT_COMBINED 
    # )

