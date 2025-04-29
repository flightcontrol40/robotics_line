
import os

import cv2
import rclpy
from cv_bridge import CvBridge
from rclpy.node import Node
from sensor_msgs.msg import Image
from ultralytics import YOLO
from ultralytics.engine.results import Results
from robot_3_interfaces.srv import QaDice
import numpy as np

BLANK_IMAGE = np.zeros((1024,1000,3), np.uint8)
ROBOT_NAME = 'beaker'


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

class DiceQA(Node):

    def __init__(self):
        super().__init__('DiceQA')

        self.robot_name = ROBOT_NAME
        self.bridge = CvBridge()
        self.model = YOLO(MODEL_FILE)
        self.latest_img = BLANK_IMAGE
        self.qa_image = BLANK_IMAGE
        self._image_sub = self.create_subscription(
            Image,
            '/camera/image_raw',
            self._img_sub,
            10
        )
        self.srv = self.create_service(
            QaDice,
            f"{self.robot_name}/qa_dice",
            self._qa_image
        )

    def _img_sub(self, image: Image):
        self.latest_img = self.bridge.imgmsg_to_cv2(image)

    def _preform_qa(self):
        img = self.latest_img[500:-1, 100:700]
        results: list[Results] = self.model(img)
        assert isinstance(results, list)
        logger = self.get_logger()
        logger.debug(f"len(results): {len(results):}")
        # Get the results
        result = results[0]

        self.qa_image = result.plot()
        names = self.model.names
        boxes = result.boxes
        logger.debug(f"Boxes: {boxes}")
        logger.debug(f"Boxes.cls: {boxes.cls}")
        if not len(boxes):
            return (self.bridge.cv2_to_imgmsg(self.qa_image), "None")

        qa_class = names[int(boxes.cls[0])]
        return (self.bridge.cv2_to_imgmsg(self.qa_image), qa_class)

    def _qa_image(self, _:QaDice.Request, response:QaDice.Response):
        # Crop the image down
        qa_img, qa_class = self._preform_qa()
        response.obj_cls = qa_class
        response.qa_image = qa_img
        return response

def main():
    rclpy.init()

    node = DiceQA()
    while rclpy.ok():
        rclpy.spin_once(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()