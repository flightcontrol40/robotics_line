import random
import shutil
from pathlib import Path

import cv2 as cv
import numpy as np

IMAGES_DIR = Path(r"C:\Users\natha\Documents\robotics_line\camera\calibration\dataset_full\dataset")
OUTPUT_COMBINED = Path(r"C:\Users\natha\Documents\robotics_line\Camera\calibration\output\combined")
OUTPUT_COMBINED.mkdir(parents=True, exist_ok=True)
DATASET_DIR = Path(r"C:\Users\natha\Documents\robotics_line\camera\calibration\dataset\images")

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

    output = img.copy()

    bound_rect: list[cv.typing.Rect] = []
    for i, c in enumerate(contours):

        contours_poly = cv.approxPolyDP(c, 3, True)
        bound_rect.append(cv.boundingRect(contours_poly))

    if len(bound_rect) > 1:
        bound_rect = sorted(bound_rect, key=_get_area, reverse=True)
        # cv.imshow("original", img)
        # cv.imshow("hsv", image_hsv)
        # cv.imshow("mask", image_mask)
        # cv.imshow("canny",m1)
        # # for i in range(len(bound_rect)):
        # #     print(int(bound_rect[i][0]), int(bound_rect[i][1]))
        # #     cv.rectangle(
        # #         output,
        # #         # p1,p2
        # #         (int(bound_rect[i][0])-5, int(bound_rect[i][1])-5),
        # #         (
        # #             int(bound_rect[i][0] + bound_rect[i][2])+5,
        # #             int(bound_rect[i][1] + bound_rect[i][3])+5,
        # #         ),
        # #         (0, 0, 0),
        # #         2,
        # #     )
        # # cv.imshow("output", output)
        # cv.waitKey(-1)
    elif len(bound_rect) == 0:
        cv.imshow("original", img)
        cv.imshow("hsv", image_hsv)
        cv.imshow("mask", image_mask)
        cv.imshow("canny",m1)
        cv.waitKey(-1)
        raise ValueError("No contours found in image")
        

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
    cv.imshow("output", output)
    if area < 5000:
        cv.imshow("output", output)
        cv.waitKey(0)
    # Yolo wants class_id x_center y_center width height all normalized
    cords = f"{center_x:.6f} {center_y:.6f} {w1/width:.6f} {h1/height:.6f}"
    return cords


def label_images():
    set_number = 0
    current_set = "0"
    images = list(IMAGES_DIR.glob("**/*.png"))
    image_count = len(images)
    train_count = int(image_count * .8)
    highest_img_count = 0
    cur_imgs = [int(x.stem.split("_")[-1]) for x in DATASET_DIR.glob("**/*.png")]
    cur_imgs.sort()
    highest_img_count = int(cur_imgs[-1])
    print(f'Highest Img Count: {highest_img_count}')
    random.shuffle(images)
    for idx, f_path in enumerate(images):
        cords = get_bounding_box(f_path)
        img = f_path.relative_to(IMAGES_DIR)
        print(img)
        print(img.parts)

        # if img.parts[0] == "1":
        #     new_name = f"one_{img.parts[1].split(".")[0]}"
        # elif img.parts[0] == "2":
        #     new_name = f"two_{img.parts[1].split(".")[0]}"
        # elif img.parts[0] == "3":
        #     new_name = f"three_{img.parts[1].split(".")[0]}"
        # elif img.parts[0] == "4":
        #     new_name = f"four_{img.parts[1].split(".")[0]}"
        # elif img.parts[0] == "5":
        #     new_name = f"five_{img.parts[1].split(".")[0]}"
        # elif img.parts[0] == "6":
        #     new_name = f"six_{img.parts[1].split(".")[0]}"
        # else:
        #     raise ValueError(f"Unknown image folder {img.parts[0]}")
        cords = f"{int(img.parts[0])-1} " + cords
        # cords = "3 " + cords

        new_name = f"img_{idx+highest_img_count+1:04d}"

        if train_count > idx:
            save_type =  "train"
        else:
            save_type = "val"

        print(cords)

        # Copy the image to the output directory
        output_file = OUTPUT_COMBINED / "images" / save_type/ f"{new_name}.png"
        print(output_file)
        output_file.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(
            f_path,
            output_file
        )
        
        # Copy the label file to the output directory
        output_file = OUTPUT_COMBINED / "labels" / save_type / f"{new_name}.txt"
        print(output_file)
        output_file.parent.mkdir(parents=True, exist_ok=True)
        with open(output_file, "w") as f:
            f.write(cords)


    # cv.waitKey()



    # shutil.copyfile(
    #     IMAGES_DIR / img,
    #     OUTPUT_COMBINED 
    # )


def shuffle():
    images_path = IMAGES_DIR / "images"
    images = list(images_path.glob("**/*.png"))
    label_path = IMAGES_DIR / "labels"
    labels = list(label_path.glob("**/*.txt"))
    images.sort()
    labels.sort()
    if len(images) != len(labels):
        raise ValueError("Images and labels do not match in length")
    pairs = list(zip(images, labels))
    for img, label in pairs:
        print(f"Image: {img.stem}, Label: {label.stem}")
        if img.stem != label.stem:
            raise ValueError(f"Image {img.stem} does not match label {label.stem}")
    random.shuffle(pairs)
    train_count = int(len(pairs) * 0.8)
    for idx, (img, label) in enumerate(pairs):
        if idx < train_count:
            save_type = "train"
        else:
            save_type = "val"
        new_name = f"img_{idx:04d}"
        img_dest = OUTPUT_COMBINED / "images" / save_type / f"{new_name}.png"
        label_dest = OUTPUT_COMBINED / "labels" / save_type / f"{new_name}.txt"
        print(f"Copying {img} to {img_dest}")
        print(f"Copying {label} to {label_dest}")

        img_dest.parent.mkdir(parents=True, exist_ok=True)
        label_dest.parent.mkdir(parents=True, exist_ok=True)

        shutil.copyfile(img, img_dest)
        shutil.copyfile(label, label_dest)
    pass

if __name__ == "__main__":
    shuffle()

# temp = Path(r"C:\Users\natha\Documents\robotics_line\camera\calibration\output\tmp")
# for img in temp.glob("**/*.bmp"):
    
#     new = img.with_suffix(".png")
#     cv.imwrite(str(new), cv.imread(str(img)))
