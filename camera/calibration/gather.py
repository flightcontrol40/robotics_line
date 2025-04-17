import random
import time
from pathlib import Path

import cv2 as cv
import pycomm3
import yaml

from camera import CheepAssChineseCamera
from robot_controller import robot

ARM_POS = Path(__file__).parent / "new_pos.yaml"

BASE_POS = [
    78.920166015625,
    40.431846618652344,
    -65.54582977294922,
    13.552433013916016,
    65.8383560180664,
    27.833118438720703,
]

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
    main()
    # learning()
    # [ 19.348966598510742 25.419536590576172 -59.648879652366155 -106.83952826778284 -78.25675079659895 -177.95411682128906
    # ]
