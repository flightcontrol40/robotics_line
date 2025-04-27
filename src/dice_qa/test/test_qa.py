import os
from glob import glob

import cv2 as cv
from ultralytics import YOLO


def find_package_share_directory(package_name, join_dirs: list[str] = None):
    """Find the package directory during tests."""
    try:
        # Try the standard approach first
        from ament_index_python.packages import get_package_share_directory
        share_dir = get_package_share_directory(package_name)
        if join_dirs is not None:
            share_dir = os.path.join(share_dir, *join_dirs)
        if not os.path.exists(share_dir):
            raise FileNotFoundError
        return share_dir
    except Exception:
        # Fallback for build-time testing
        # This assumes tests run from the package's test directory
        current_dir = os.path.dirname(os.path.abspath(__file__))
        package_dir = os.path.dirname(current_dir)
        if join_dirs is not None:
            package_dir = os.path.join(package_dir, *join_dirs)
        return package_dir

MODEL_FILE = find_package_share_directory('dice_qa', ['model','best.pt'])
IMAGE_DIR = find_package_share_directory('dice_qa', ['img'])

def test_model():
    model = YOLO(MODEL_FILE)
    print(IMAGE_DIR)
    for img_name in glob("*.bmp", root_dir=IMAGE_DIR):
        image_path = os.path.join(IMAGE_DIR, img_name)
        assert os.path.exists(image_path)

        img = cv.imread(image_path)
        cv.imshow("original",img)

        crop = img[500:-1, 100:700]
        cv.imshow("crop",crop)
        assert True
        results = model(img)
        # # Get the results
        names = model.names
        boxes = results[0].boxes

        qa_class = names[int(boxes.cls[0])]
        print(qa_class)
        qa_image= results[0].plot()
        cv.imshow("Model", qa_image)
        cv.waitKey(-1)


if __name__ == "__main__":
    test_model()