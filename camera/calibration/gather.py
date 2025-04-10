import argparse
import json
import random
import time
from pathlib import Path

import cv2 as cv
import yaml

from camera import CheepAssChineseCamera
from robot_controller import robot

BASE_POS = [78.920166015625, 40.431846618652344, -65.54582977294922, 13.552433013916016, 65.8383560180664, 27.833118438720703]

def learning():
    r = robot("172.29.208.124")
    while True:
        data = None
        with open("pos2.yaml", "r") as fd:
            data = yaml.safe_load(fd)
        if data is None:
            data = {}
        choice = input("read, move, command: ")
        if "read" in choice:
            n = input("Name: ")
            pos = r.read_current_joint_position()
            data[n] = pos
            pos = r.read_current_cartesian_pose()
            data[n+"_cart"] = pos
            with open("pos2.yaml", "w") as fd:
                yaml.safe_dump(data, fd)
        elif "move" in choice:
            parts = choice.split(" ")
            if parts[1] == "c":
                p = parts[2] + "_cart"
                if p not in data:
                    print("invalid pos")
                    continue
                r.write_cartesian_position(data[p])
            else:
                p = parts[2]
                if p not in data:
                    print("invalid pos")
                    continue
                r.write_joint_pose(data[p])

        elif choice == "command":
            p = input("command: ")
            if p == 'open' or p == 'o':
                r.schunk_gripper("open")
            elif p == 'close' or p == 'c':
                r.schunk_gripper("close")
            else:
                print("bad command")
        else:
            print("bad Choice")



# data = None
# with open("pos.yaml", "r") as fd:
#     data = yaml.safe_load(fd)
# if data is None:
#     data = {}


def rotate_x(robot:robot,data:dict):
    robot.write_joint_pose(data["edgeAbove"])
    robot.write_joint_pose(data["edgeH"])
    robot.schunk_gripper("open")
    time.sleep(.5)
    robot.write_joint_pose(data["edgeAbove"])
    robot.write_joint_pose(data["edgeV"])
    robot.schunk_gripper("close")
    time.sleep(.5)
    robot.write_joint_pose(data["edgeAbove"])


def rotate_y(robot:robot, data:dict):
    robot.write_joint_pose(data["above"])
    robot.write_joint_pose(data['grab'])
    robot.schunk_gripper("open")
    time.sleep(.5)
    robot.write_joint_pose(data["above"])
    robot.write_joint_pose(data["placeRotate"])
    robot.write_joint_pose(data["place"])
    robot.schunk_gripper("close")
    time.sleep(.5)
    robot.write_joint_pose(data["placeRotate"])

def cycle(robot:robot, data:dict):
    for _ in range(3):
        robot.write_joint_pose(data['scanPos'])
        print("scanning...")
        time.sleep(2)
        print("rotating")
        rotate_x(robot, data)
    print("full y rotation...")
    rotate_y(robot, data)
    rotate_y(robot, data)



def main():
    r = robot("172.29.208.124")
    r.schunk_gripper("open")
    # print(data['scanPos'])


    data = None
    with open("pos.yaml", "r") as fd:
        data = yaml.safe_load(fd)
    if data is None:
        data = {}

    # First pickup
    r.write_joint_pose(data["edgeAbove"])
    r.write_joint_pose(data["edgeH"])
    input("Place Dice... Hit enter..")
    r.schunk_gripper("close")
    time.sleep(.5)

    cycle(r,data)

    # r.schunk_gripper("close")
    # time.sleep(.5)
    # r.write_joint_pose(data["edgeAbove"])


    # r.write_joint_pose(data["edgeAbove"])
    # r.write_joint_pose(data["edgeV"])
    # r.schunk_gripper("open")
    # r.write_joint_pose(data["above"])
    # r.write_joint_pose(data["grab"])
    # r.schunk_gripper("close")
    # r.write_joint_pose(data["above"])
    # r.write_joint_pose(data["placeRotate"])
    # r.write_joint_pose(data["place"])
    # r.schunk_gripper("open")
    # r.write_joint_pose(data["placeRotate"])
    # r.write_joint_pose(data["above"])
    # r.write_joint_pose(data["grab"])

    # for _ in range(25):
    #     new_pos = []

    #     for i, x in enumerate(BASE_POS):
    #         if i <2:
    #             new_pos.append(x)
    #         else:
    #             new_pos.append(x +((random.random()-0.5) * 2))
    #     r.write_joint_pose(new_pos)
    #     time.sleep(1)


if __name__ =="__main__":
    # main()
    learning()