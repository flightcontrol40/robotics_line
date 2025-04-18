import math
import random
import time
from copy import copy
from pathlib import Path

import cv2 as cv
import numpy as np
import pycomm3
import yaml

from camera import CheepAssChineseCamera
from robot_controller import robot

ARM_POS = Path(__file__).parent / "training2.yaml"

BASE_POS = [
    78.920166015625,
    40.431846618652344,
    -65.54582977294922,
    13.552433013916016,
    65.8383560180664,
    27.833118438720703,
]

OUTPUT_PATH = Path("output/newest")

AVG_Z = -130.1991424560547

def learning():
    r = robot("172.29.208.124")
    while True:
        data = None
        with open(ARM_POS, "r") as fd:
            data = yaml.safe_load(fd)
        if data is None:
            data = {}
        choice = input("read, move, command: ")
        if "read" in choice:
            n = input("Name: ")
            pos = r.read_current_joint_position()
            data[n] = pos
            pos = r.read_current_cartesian_pose()
            data[n + "_cart"] = pos
            with open(ARM_POS, "w") as fd:
                yaml.safe_dump(data, fd)
        elif "move" in choice:
            parts = choice.split(" ")
            if parts[1] == "c":
                if parts[2] == "raw":
                    pos = input("Input Pos: ")
                    pos = pos.strip().split(" ")
                    p = [float(x) for x in pos]
                    r.write_cartesian_position(p)
                    continue
                else:
                    p = parts[2] + "_cart"
                    if p not in data:
                        print("invalid pos")
                        continue
                r.write_cartesian_position(data[p])
            elif parts[1]:
                if parts[2] == "raw":
                    pos = input("Input Pos: ")
                    pos = pos.strip().split(" ")
                    print(pos)
                    p = [float(x) for x in pos]
                    r.write_joint_pose(p)
                    continue
                else:
                    p = parts[2]
                    if p not in data:
                        print("invalid pos")
                        continue
                r.write_joint_pose(data[p])

        elif choice == "command":
            p = input("command: ")
            if p == "open" or p == "o":
                r.schunk_gripper("open")
            elif p == "close" or p == "c":
                r.schunk_gripper("close")
            else:
                print("bad command")
        else:
            print("bad Choice")

def random_place():
    r = robot("172.29.208.124")
    data = None
    with open(ARM_POS, "r") as fd:
        data = yaml.safe_load(fd)
    if data is None:
        data = {}
    tl = data["top_left_cart"]
    br = data["bottom_right_cart"]
    # print(f"top left: {tl}")
    # print(f"bottom right: {br}")
    z_cord = np.average([tl[2], br[2]])
    x_range = [tl[0], br[0]]
    y_range = [tl[1], br[1]]
    yaw_range = [-90, 90]

    store_place_location = []
    camera = CheepAssChineseCamera()

    try:
        camera.start_camera()
        while True:
            for _ in range(20):
                x_cord = random.uniform(*x_range)
                y_cord = random.uniform(*y_range)
                yaw_cord = random.uniform(*yaw_range)
                rand_pos = list(tl)
                rand_pos[0] = x_cord
                rand_pos[1] = y_cord
                rand_pos[2] = z_cord+80
                rand_pos[5] = yaw_cord
                r.write_cartesian_position(rand_pos)
                rand_pos[2] = z_cord
                r.write_cartesian_position(rand_pos)
                r.schunk_gripper("open")
                time.sleep(0.5)
                rand_pos[2] = z_cord+80
                store_place_location = copy(rand_pos)
                r.write_cartesian_position(rand_pos)
                rand_pos[0] = 500
                rand_pos[1] = 0
                r.write_cartesian_position(rand_pos)
                # Take Photo
                take_photo(store_place_location, camera)
                rand_pos = copy(store_place_location)
                r.write_cartesian_position(rand_pos)
                rand_pos[2] = z_cord
                r.write_cartesian_position(rand_pos)
                r.schunk_gripper("close")
                time.sleep(.5)
                rand_pos[2] = z_cord+80
                r.write_cartesian_position(rand_pos)

            input("Rotate and Continue:")
    finally:
        camera.release_camera()

def take_photo(cords, camera):
    img_number = 0
    for img in OUTPUT_PATH.glob("images/*.png"):
        tmp = int(img.stem.removeprefix("img_"))
        if tmp >= img_number:
            img_number = tmp
    img_number = img_number + 1
    print(f"taking Photo: {img_number}")
    output_file = OUTPUT_PATH / "images" / f"img_{img_number:03d}.png"
    output_file.parent.mkdir(parents=True, exist_ok=True)
    print("Getting Frame")
    frame = camera.get_frame()
    temp = frame[430:1010, 60:]
    print(f"Writing to file: {output_file}")
    cv.imwrite(str(output_file), temp)

    cord_file = OUTPUT_PATH / "Cords" /f"img_{img_number:03d}.txt"
    cord_file.parent.mkdir(exist_ok=True, parents=True)
    with open(cord_file, 'w') as fd:
        fd.write(str(cords))



    # while True:
        # tmp = cv.imread(output_file)
        # tmp = cv.circle(tmp, (x,y), radius=0, color=(0, 0, 255), thickness=-1)
        # cv.waitKey(1)
        # crop = input("Crop: ")
        # if crop in ["", " ", None]:
        #     cv.imwrite(str(output_file), temp)
        # else:
        #     x1,x2,y1,y2 = crop.split(" ")
        #     temp = frame[y1:y2, x1:x2]


# Assuming dice is in hand
def rotate_v(robot: robot, data: dict):
    # Move above
    robot.write_joint_pose(data["convAbove"])
    # Move to place pos
    robot.write_joint_pose(data["convV"])
    robot.schunk_gripper("open")
    time.sleep(0.5)
    # Move above
    robot.write_joint_pose(data["convAbove"])
    # rotate 90
    robot.write_joint_pose(data["convAbove2"])
    # Move Down
    robot.write_joint_pose(data["convV2"])
    robot.schunk_gripper("close")
    time.sleep(0.5)
    robot.write_joint_pose(data["convAbove2"])

def rotate_h(robot: robot, data: dict):
    robot.write_joint_pose(data["convHOffset"])
    robot.write_joint_pose(data["hPlace"])
    robot.schunk_gripper("open")
    time.sleep(0.5)
    robot.write_joint_pose(data["convHOffset"])
    robot.write_joint_pose(data["convAbove"])
    robot.write_joint_pose(data["convV"])
    robot.schunk_gripper("close")
    time.sleep(0.5)
    robot.write_joint_pose(data["convAbove"])

def capture_face(robot, data, face):
    robot.write_joint_pose(data["scanPos"])
    print("scanning...")
    with CheepAssChineseCamera() as camera:
        frame = camera.get_frame()
        cv.imshow("image", frame)
        d = Path(f"./output/f{face}")
        d.mkdir(parents=True, exist_ok=True)
        for image_number in range(100):
            try: 
                new_pos = []
                for i, x in enumerate(data["scanPos_cart"]):
                    if i > 4:
                        new_pos.append(x)
                    else:
                        new_pos.append(x + ((random.random() - 0.5) * 10))
                print(new_pos)
                robot.write_cartesian_position(new_pos)
                frame = camera.get_frame()
                crop = frame[600:900, 50:350]
                cv.imshow("image", crop)
                im_path = d / f"img_{image_number:02d}.png"
                print(f"saving image {im_path}")
                cv.imwrite(im_path, crop)
            except pycomm3.exceptions.CommError as e:
                print(f"comm Error!: {e}")
                time.sleep(.5)
                continue

def cycle(robot: robot, data: dict):
    for i in range(4):
        capture_face(robot, data, i)
        rotate_v(robot, data)
    for i in range(4, 6):
        capture_face(robot, data, i)
        rotate_h(robot, data)

def main():
    r = robot("172.29.208.124")
    r.set_speed(250)

    data = None
    with open(ARM_POS, "r") as fd:
        data = yaml.safe_load(fd)
    if data is None:
        data = {}

    cycle(r, data)


if __name__ == "__main__":
    # main()
    # learning()
    random_place()
    # [ 19.348966598510742 25.419536590576172 -59.648879652366155 -106.83952826778284 -78.25675079659895 -177.95411682128906
    # ]
