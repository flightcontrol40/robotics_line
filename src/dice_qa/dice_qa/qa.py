
import os

import cv2
import rclpy
from cv_bridge import CvBridge
from rclpy.node import Node
from sensor_msgs.msg import Image
from std_msgs.msg import String
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

class DiceQA(Node):

    def __init__(self):
        super().__init__('DiceQA')
        self.declare_parameters(
            namespace='',
            parameters=[('robot_name','noNAME')] # custom, default
        )
        self.bridge = CvBridge()
        self.model = YOLO(MODEL_FILE)
        self._image_sub = self.create_subscription(
            Image,
            '/camera/image_raw',
            callback=self._qa_image,
        )
        self.qa_publisher = self.create_publisher(
            String,
            f'/{self.get_parameter('robot_name').value}/qa/status',
            10
        )
        self.qa_image_pub = self.create_publisher(
            Image,
            f'/{self.get_parameter('robot_name').value}/qa/img',
            10
        )

    def _qa_image(self, image):
        img = self.bridge.imgmsg_to_cv2(image, encoding="bgr8")
        # Crop the image down
        img = img[500:-1, 100:700]
        results = self.model(img)
        if not len(results):
            return
        # Get the results
        result = results[0]
        self.qa_image = result.plot()
        names = self.model.names
        boxes = results[0].boxes
        qa_class = names[int(boxes.cls[0])]
        self.qa_publisher.publish(String(data=qa_class))
        self.qa_image_pub.publish(self.bridge.cv2_to_imgmsg(self.qa_image))


def main():
    rclpy.init()

    node = DiceQA()
    while rclpy.ok():
        rclpy.spin_once(node)
        if node.qa_image is not None:
            cv2.imshow("QA Image", node.qa_image)
            cv2.waitKey(1)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()