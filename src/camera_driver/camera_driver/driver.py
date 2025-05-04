
import sys

import numpy as np
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image

from camera_driver.camera import Camera


def cv2_to_image(cv_img):
    """
    Manually pack a numpy array into a sensor_msgs/Image.
    """
    img = Image()
    img.height, img.width = cv_img.shape[:2]
    if cv_img.ndim == 2:
        img.encoding = "mono8"
        chans = 1
    else:
        chans = cv_img.shape[2]
        # OpenCV default is BGR
        img.encoding = "bgr8" if chans == 3 else "rgba8"
    byteorder = cv_img.dtype.byteorder
    if byteorder == ">":
        img.is_bigendian = 1
    elif byteorder == "<" or byteorder == "=":
        img.is_bigendian = 0
    else:
        img.is_bigendian = sys.byteorder == "big"
    img.step = img.width * chans * cv_img.dtype.itemsize
    img.data = cv_img.reshape(-1).tobytes()
    return img

class CameraDriver(Node):

    def __init__(self):
        super().__init__('camera_driver')
        # QoS history depth of 10
        self.cam = Camera()
        self.cam.start_camera()
        self.publisher_ = self.create_publisher(
            Image,
            'camera/image_raw',
            10
        )
        self._img_timer = self.create_timer(
            0.03,
            callback=self.capture_image
        )

    def capture_image(self):
        frame = self.cam.get_frame()
        self.publish_image(frame)

    def publish_image(self, frame: np.ndarray):
        self.get_logger().info("Publishing Image")
        # Convert OpenCV image (BGR8) to ROS2 Image
        img_msg = cv2_to_image(frame)
        # Stamp with acquisition time
        img_msg.header.stamp = self.get_clock().now().to_msg()
        # Optical frame of your camera
        img_msg.header.frame_id = 'camera_optical_frame'
        # Publish
        self.publisher_.publish(img_msg)


def main():
    rclpy.init()

    node = CameraDriver()
    node.get_logger().info("Starting camera")
    try:
        rclpy.spin(node)
        # while True:
        #     node.cam.start_camera()
        #     node.get_logger().info("camera started")
        #     node.cam.release_camera()
    except Exception as e:
        node.get_logger().error(f"Error: {e}")
    finally:
        node.cam.release_camera()

    node.destroy_node()
    rclpy.shutdown()
if __name__ == '__main__':
    main()