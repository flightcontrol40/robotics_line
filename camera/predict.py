import cv2 as cv
from ultralytics import YOLO

# Load the best model we have so far:

model_file = "best.pt"
model = YOLO(model_file)


# Load test image
image = cv.imread("/content/drive/MyDrive/robotics_line/img_1.bmp")

# predict returns a list of Results object.
# Since we are running on a single image, we'll take the only one result
results = model.predict(image)[0]

