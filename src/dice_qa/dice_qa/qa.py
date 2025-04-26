import asyncio

import cv2
import rclpy
from cv_bridge import CvBridge
from rclpy.node import Node
from sensor_msgs.msg import Image
from std_msgs.msg import String
from ultralytics import YOLO


class DiceQA(Node):

    def __init__(self):
        super().__init__('DiceQA')
        self.bridge = CvBridge()
        self.model = YOLO("/home/nathan/robotics_line/camera/model/best.pt")
        self._image_sub = self.create_subscription(
            Image,
            '/camera/image_raw',
            callback=self._qa_image,
        )
        self.qa_publisher = self.create_publisher(
            String,
            '/qa/status',
            10
        )

    def _qa_image(self, image):
        img = self.bridge.imgmsg_to_cv2(image, encoding="bgr8")
        # Crop the image down
        img = img[0:500, 0:500]
        results = self.model(img)
        self.qa_image = results[0].plot()
        # Get the results
        names = self.model.names
        boxes = results[0]
        qa_class = names[int(boxes.cls[0])]
        self.qa_publisher.publish(String(data=qa_class))


def main():
    rclpy.init()

    node = DiceQA()
    while rclpy.ok():
        rclpy.spin_once(node)
        if node.qa_image is not None:
            cv2.imshow("QA Image", node.qa_image)
            cv2.waitKey(1)
    node.destroy()
    rclpy.shutdown()
if __name__ == '__main__':
    main()