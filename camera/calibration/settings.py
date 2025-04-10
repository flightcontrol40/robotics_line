import cv2
import mvsdk
import numpy as np

window_name = "image"

cv2.namedWindow(window_name,cv2.WINDOW_NORMAL)

DevList = mvsdk.CameraEnumerateDevice()
nDev = len(DevList)
if nDev < 1:
    print("No camera was found!")
    exit()

for i, DevInfo in enumerate(DevList):
    print("{}: {} {}".format(i, DevInfo.GetFriendlyName(), DevInfo.GetPortType()))
i = 0 if nDev == 1 else int(input("Select camera: "))
DevInfo = DevList[i]
# print(DevInfo)

hCamera = 0
try:
    hCamera = mvsdk.CameraInit(DevInfo, -1, -1)
except mvsdk.CameraException as e:
    print("CameraInit Failed({}): {}".format(e.error_code, e.message) )
    exit()

cap = mvsdk.CameraGetCapability(hCamera)



mvsdk.CameraSetIspOutFormat(hCamera, mvsdk.CAMERA_MEDIA_TYPE_BGR8)

mvsdk.CameraSetTriggerMode(hCamera, 0)

mvsdk.CameraSetAeState(hCamera, 0)
mvsdk.CameraSetExposureTime(hCamera, 30 * 1000)

mvsdk.CameraPlay(hCamera)

FrameBufferSize = cap.sResolutionRange.iWidthMax * cap.sResolutionRange.iHeightMax *  3

pFrameBuffer = mvsdk.CameraAlignMalloc(FrameBufferSize, 16)

def get_frame():
    while True:
        try:
            pRawData, FrameHead = mvsdk.CameraGetImageBuffer(hCamera, 200)
            mvsdk.CameraImageProcess(hCamera, pRawData, pFrameBuffer, FrameHead)
            mvsdk.CameraReleaseImageBuffer(hCamera, pRawData)

            
            frame_data = (mvsdk.c_ubyte * FrameHead.uBytes).from_address(pFrameBuffer)
            frame = np.frombuffer(frame_data, dtype=np.uint8)
            frame = frame.reshape((FrameHead.iHeight*2, FrameHead.iWidth *2, 3) )

            yield frame
            
        except mvsdk.CameraException as e:
            if e.error_code != mvsdk.CAMERA_STATUS_TIME_OUT:
                print("CameraGetImageBuffer failed({}): {}".format(e.error_code, e.message) )
                return


def on_change_contrast(value):
    mvsdk.CameraSetContrast(hCamera, value)

def on_change_gamma(value):
    mvsdk.CameraSetGamma(hCamera, value)

def on_change_saturation(value):
    mvsdk.CameraSetSaturation(hCamera, value)

def on_change_gain(value):
    mvsdk.CameraSetGain(hCamera, value,value,value)



cv2.createTrackbar('Contrast', window_name,mvsdk.CameraGetContrast(hCamera) , cap.sContrastRange.iMax, on_change_contrast)
cv2.createTrackbar('Gamma', window_name,mvsdk.CameraGetGamma(hCamera) , cap.sGammaRange.iMax, on_change_gamma)
cv2.createTrackbar('Saturation', window_name,mvsdk.CameraGetSaturation(hCamera) , cap.sSaturationRange.iMax, on_change_saturation)
cv2.createTrackbar('Gain', window_name,cap.sSaturationRange.iMin , cap.sSaturationRange.iMax, on_change_gain)

blank_image = np.zeros((200,200,3), np.uint8)

temp = mvsdk.CameraSetDenoise3DParams(hCamera,True, 3, 0)
mvsdk.CameraFlatFieldingCorrectSetEnable(hCamera, True)
mvsdk.CameraSetFriendlyName(hCamera, "Thomas the Dank Engine")
mvsdk.CameraReadParameterFromFile(hCamera, "new_cam_settings.txt")
while True:
    try:
        pRawData, FrameHead = mvsdk.CameraGetImageBuffer(hCamera, 200)
        mvsdk.CameraImageProcess(hCamera, pRawData, pFrameBuffer, FrameHead)
        mvsdk.CameraReleaseImageBuffer(hCamera, pRawData)

        frame_data = (mvsdk.c_ubyte * FrameHead.uBytes).from_address(pFrameBuffer)
        frame = np.frombuffer(frame_data, dtype=np.uint8)
        frame = frame.reshape((FrameHead.iHeight, FrameHead.iWidth , 3) )

        cv2.imshow(window_name, frame)
    except mvsdk.CameraException as e:
        if e.error_code != mvsdk.CAMERA_STATUS_TIME_OUT:
            print("CameraGetImageBuffer failed({}): {}".format(e.error_code, e.message) )

    k = (cv2.waitKey(1) & 0xFF)
    if k == ord('q'):
        break
    elif k == ord('s'):
        file = input("Save Location: ")
        mvsdk.CameraSaveParameterToFile(hCamera, file)


mvsdk.CameraUnInit(hCamera)

mvsdk.CameraAlignFree(pFrameBuffer)

cv2.destroyAllWindows()