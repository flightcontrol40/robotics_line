import asyncio

import rclpy
from cv_bridge import CvBridge
from rclpy.node import Node
from sensor_msgs.msg import Image

from camera_driver.camera import CheepAssChineseCamera


class MinimalPublisher(Node):

    def __init__(self):
        super().__init__('minimal_publisher')
        self.bridge = CvBridge()
        self.publisher_ = self.create_publisher(
            Image,
            '/camera/image_raw',
            10
        )

    async def publish_image(self, image):
        msg = self.bridge.cv2_to_imgmsg(image, encoding="bgr8")
        self.publisher_.publish(msg)
        self.get_logger().debug('Publishing image')



async def camera_loop(node: MinimalPublisher):
    cam = CheepAssChineseCamera()
    print("Starting camera")
    try:
        cam.start_camera()
        for frame in cam:
            await node.publish_image(frame)
            await asyncio.sleep(1e-4)


    finally:
        cam.release_camera()

async def ros_loop(node):
    while rclpy.ok():
        rclpy.spin_once(node, timeout_sec=0)
        await asyncio.sleep(1e-4)

def main():
    rclpy.init()

    node = MinimalPublisher()
    future = asyncio.wait([ros_loop(node), camera_loop(node)])
    asyncio.get_event_loop().run_until_complete(future)

    node.destroy()
    rclpy.shutdown()
if __name__ == '__main__':
    main()