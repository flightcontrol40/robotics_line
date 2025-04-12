import mvsdk
import numpy as np


class CameraConnectionError(Exception):
    """Raised For camera connection issues."""

class CheepAssChineseCamera:
    """An interface for the overhead camera."""

    def __init__(self):
        self._opened = False

    def __enter__(self):
        self.start_camera()
        return self
    
    def __exit__(self, *args, **kwargs):
        self.release_camera()

    def __iter__(self):
        while True:
            try:
                for i in range(3):
                    pRawData, FrameHead = mvsdk.CameraGetImageBuffer(self.hCamera, 200)
                    mvsdk.CameraImageProcess(self.hCamera, pRawData, self.pFrameBuffer, FrameHead)
                    mvsdk.CameraReleaseImageBuffer(self.hCamera, pRawData)

                    frame_data = (mvsdk.c_ubyte * FrameHead.uBytes).from_address(self.pFrameBuffer)
                    frame = np.frombuffer(frame_data, dtype=np.uint8)
                    frame = frame.reshape((FrameHead.iHeight, FrameHead.iWidth, 3 ))
                    if i == 2:
                        yield frame

            except mvsdk.CameraException as e:
                if e.error_code != mvsdk.CAMERA_STATUS_TIME_OUT:
                    print("CameraGetImageBuffer failed({}): {}".format(e.error_code, e.message) )
                    return

    def start_camera(self):
        attempts = 0
        self.hCamera = 0
        while True:
            DevList = mvsdk.CameraEnumerateDevice()
            nDev = len(DevList)
            if nDev < 1:
                if attempts > 5:
                    raise CameraConnectionError("No camera was found!")
                else:
                    attempts+=1
                    print("Failed to connect to camera, Trying again")
            else:
                break
        DevInfo = DevList[0]
        try:
            self.hCamera = mvsdk.CameraInit(DevInfo, -1, -1)
        except mvsdk.CameraException as e:
            raise CameraConnectionError("CameraInit Failed({}): {}".format(e.error_code, e.message))

        self.cap = mvsdk.CameraGetCapability(self.hCamera)
        mvsdk.CameraSetIspOutFormat(self.hCamera, mvsdk.CAMERA_MEDIA_TYPE_BGR8)
        mvsdk.CameraSetTriggerMode(self.hCamera, 0)
        # mvsdk.CameraSetAeState(self.hCamera, 0)
        # mvsdk.CameraSetExposureTime(self.hCamera, 30 * 1000)

        self.FrameBufferSize = self.cap.sResolutionRange.iWidthMax * self.cap.sResolutionRange.iHeightMax *  3
        mvsdk.CameraSetDenoise3DParams(self.hCamera,True, 3, 0)
        mvsdk.CameraPlay(self.hCamera)

        mvsdk.CameraReadParameterFromFile(self.hCamera, "new_cam_settings.txt")
        self.pFrameBuffer = mvsdk.CameraAlignMalloc(self.FrameBufferSize, 16)

        self._opened = True

    def release_camera(self):
        mvsdk.CameraUnInit(self.hCamera)
        mvsdk.CameraAlignFree(self.pFrameBuffer)
        self._opened = False

    def get_frame(self):
        while True:
            if self._opened:
                try:
                    for i in range(4):
                        self.pFrameBuffer = mvsdk.CameraAlignMalloc(self.FrameBufferSize, 16)
                        pRawData, FrameHead = mvsdk.CameraGetImageBuffer(self.hCamera, 200)
                        mvsdk.CameraImageProcess(self.hCamera, pRawData, self.pFrameBuffer, FrameHead)
                        mvsdk.CameraReleaseImageBuffer(self.hCamera, pRawData)

                        frame_data = (mvsdk.c_ubyte * FrameHead.uBytes).from_address(self.pFrameBuffer)
                        frame = np.frombuffer(frame_data, dtype=np.uint8)
                        frame = frame.reshape((FrameHead.iHeight, FrameHead.iWidth, 3 ))
                    return frame

                except mvsdk.CameraException as e:
                    if e.error_code != mvsdk.CAMERA_STATUS_TIME_OUT:
                        print("CameraGetImageBuffer failed({}): {}".format(e.error_code, e.message) )
                    

