import cv2 as cv

coords = [408.4205811788871, 416.0050172814008, -50.19914245605469, 178.7895050048828, 0.4933678209781647, 34.763002933765605, 0, 0, 0]
img_path = r"/home/nathan/robotics_line/camera/calibration/output/newest/img_001.png"



img = cv.imread(img_path)

y_cord = int(coords[1] -148)
x_cord = int(coords[0] -345)

tmp = cv.rectangle(img, (x_cord-40, y_cord-40), (x_cord+40,y_cord+40),(0,0,255))
# y_scaled = (y_cord / v_span) * h
# x_scaled = (x_cord / w_span) * w
# print(x_scaled, y_scaled)
# tmp = cv.circle(img, (int(x_cord- 345),int(y_cord-148)), radius=2, color=(0, 0, 255), thickness=-1)


cv.imshow("crop",tmp)



cv.waitKey(0)
cv.destroyAllWindows()