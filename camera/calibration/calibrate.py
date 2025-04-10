"""
Camera Calibration using chess board patterns.
CS 455 - S25
Nathan Hampton

Generates a json file containing camera calibration information.
Based off of the Opencv Camera Calibration guide.

https://docs.opencv.org/4.x/dc/dbb/tutorial_py_calibration.html
"""
import argparse
import json
from pathlib import Path

import cv2 as cv
import numpy as np

from camera import CheepAssChineseCamera

# Define the dimensions of checkerboard
CHECKERBOARD = (6,4)

# Output json file
OUTPUT_JSON_PATH = Path(__file__).parent / "camera-params.json"

# Get image folder path, Images should be in a folder next to this file
# called 'images'
folder_path = Path(__file__).parent / "images"

# Allows directly encoding np array as json data
class NumpyEncoder(json.JSONEncoder):
    """
    Json Encoder for numpy arrays.

    credit: David Hempy 
    https://stackoverflow.com/questions/26646362/numpy-array-is-not-json-serializable
    """

    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return super().default(obj)


def get_images(save_path):
    out_path = Path(save_path)
    idx = 0

    with CheepAssChineseCamera() as camera:
        try:
            for frame in camera:
                idx +=1
                file = out_path / f"img_{idx:02}.jpg"
                print(f"Writing Image to: {file}")
                cv.imwrite(str(file), frame)

                yield frame
                print("Hit c to continue")

                while (cv.waitKey(1) & 0xFF) != ord('c'):
                    pass
        except OSError:
            raise OSError("Could not open camera!")


###########################################################################
# Image Calibration Functions
###########################################################################

def calibrate_camera(args):
    # termination criteria
    criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)

    # prepare object points
    # Set the dimensions of the object array to (1, number_of_corners, XYZ)
    dimensions = (1, CHECKERBOARD[0] * CHECKERBOARD[1], 3)
    # Create array with those dimensions and fill it with zeros
    obj_points_ref = np.zeros(dimensions, np.float32)
    # Update the array to contain all 2d sequences, ie [[[0,0,0],[0,1,0]],[0,2,0]...[x,y,0]]]
    obj_points_ref[0, :, :2] = np.mgrid[0:CHECKERBOARD[0], 0:CHECKERBOARD[1]].T.reshape(-1, 2)

    # Arrays to store object points and image points from all the images.
    obj_points = [] # 3d point in real world space
    img_points = [] # 2d points in image plane.
    image_dir = args.images_dir
    if image_dir is None:
        images = get_images(args.camera_files)
    else:
        image_paths = Path(image_dir).glob('**/*.jpg')
        def image_reader(images):
            for fname in images:
                fname = str(Path(fname).absolute().resolve())
                img = cv.imread(fname)
                yield img
        images = image_reader(image_paths)
    cv.namedWindow("img")
    processed_images = 0
    for img in images:
        if processed_images >= 10:
            break
        # Convert to grayscale for better recognition
        gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

        # Find the chess board corners
        ret, corners = cv.findChessboardCorners(gray, CHECKERBOARD, None)

        # If found, add object points, image points (after refining them)
        if ret:
            obj_points.append(obj_points_ref)

            corners2 = cv.cornerSubPix(gray,corners, (11,11), (-1,-1), criteria)
            img_points.append(corners2)
            # Draw and display the corners
            cv.drawChessboardCorners(img, (7,6), corners2, ret)
            cv.imshow('img', img)
            cv.waitKey(500)
            processed_images +=1
            print(f"Processed: {processed_images}/10")

        else:
            print("Could not find Chessboard in image!")
            cv.imshow('img', img)
            cv.waitKey(1000)

    if image_dir is None:
        images.close()

    # Clear any display windows
    cv.destroyAllWindows()

    try:
        # Get the calibration info
        ret, mtx, dist, rvecs, tvecs = cv.calibrateCamera(obj_points, img_points, gray.shape[::-1], None, None)

        # Make Json array
        json_data = {
            "ret" : ret,
            "mtx" : mtx,
            "dist": dist,
            "rvecs": rvecs,
            "tvecs": tvecs
        }

        with open(args.output, "w") as fp:
            json.dump(json_data, fp, indent=2, cls=NumpyEncoder)
        print(f"Output Matrix Generated! Saved to {args.output}")
    except Exception:
        print("Could not generate output matrix")

def undistort_image(args):
    image = Path(args.input)
    camera_calibration_json = Path(args.calibration_data)
    output_dir = Path(args.output)
    images = []
    if image.is_dir():
        for i in image.glob('**/*.jpg'):
            images.append(i)
    else:
        images.append(str(image))
    # Load calibration data
    calibration_data = {}
    with open(camera_calibration_json, "r") as fd:
        calibration_data = json.load(fd)
    # Convert items back to numpy arrays
    calibration_data['dist'] = np.array(calibration_data['dist'])
    calibration_data['mtx'] = np.array(calibration_data['mtx'])
    output_dir.mkdir(parents=True, exist_ok=True)
    for key in ['rvecs', 'tvecs']:
        temp = []
        for sub in calibration_data[key]:
            temp.append(np.array(sub))
        calibration_data[key] = tuple(temp)
    print(f"undistorting '{image}'")
    for img_path in images:
        img_name = Path(img_path).name
        img = cv.imread(str(img_path))
        h,  w = img.shape[:2]
        new_camera_mtx, roi = cv.getOptimalNewCameraMatrix(
            calibration_data['mtx'],
            calibration_data["dist"],
            (w,h),
            1,
            (w,h)
        )
        dst = cv.undistort(img, calibration_data['mtx'], calibration_data["dist"], None, new_camera_mtx)
        # crop the image
        x, y, w, h = roi
        dst = dst[y:y+h, x:x+w]
        output = output_dir / f'{img_name}_undistorted.jpg'
        cv.imwrite(str(output), dst)
        print(f"Saving undistorted image to: '{output}")

###########################################################################
# Command Line Parsers
###########################################################################

parser = argparse.ArgumentParser("Camera Calibrator")
subparsers = parser.add_subparsers(help='subcommand help', required=True)

calibrate_parser = subparsers.add_parser('calibrate')
calibrate_parser.add_argument(
    '-i',
    '--images_dir', 
    help=('A Directory containing the calibration images.'
          "Leave blank if you want to take the images as you go."),
    default=None,
    action="store"
)
calibrate_parser.add_argument(
    '-c',
    '--camera', 
    help=('The hardware index to use if taking images as you go.'
          "Defaults to: 0 (The default system camera)."),
    default=0,
    action="store"
)
calibrate_parser.add_argument(
    '-f',
    '--camera_files', 
    help=('The folder to output captured images to.'),
    default="./images",
    action="store"
)
calibrate_parser.add_argument(
    '-o', '--output',
    default="camera-params.json",
    help='output file for the calibration data',
    action="store"
)
calibrate_parser.set_defaults(func = calibrate_camera)

undistort_parser = subparsers.add_parser('undistort')
undistort_parser.add_argument('input', help='file or directory of images to un-distort')
undistort_parser.add_argument(
    'calibration_data',
    default="camera-params.json",
    help='The calibration data file.'
)
undistort_parser.set_defaults(func = undistort_image)

undistort_parser.add_argument('-o', '--output', default="./output", help='Directory to export the undistorted images to.')


if __name__ == "__main__":
    args = parser.parse_args()
    args.func(args)

# End
