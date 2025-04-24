import cv2
from PIL import Image
from ultralytics import YOLO

from camera import CheepAssChineseCamera

model = YOLO("/home/nathan/robotics_line/camera/model/best.pt")
camera = CheepAssChineseCamera()
camera.start_camera()
cv2.namedWindow("YOLO Inference")

i = 4

for frame in camera:

    results = model(frame)
    # Visualize the results on the frame
    annotated_frame = results[0].plot()
    # Display the annotated frame
    cv2.imshow("YOLO Inference", annotated_frame)

    # Break the loop if 'q' is pressed
    if cv2.waitKey(5) & 0xFF == ord("q"):
        break

camera.release_camera()
cv2.destroyAllWindows()