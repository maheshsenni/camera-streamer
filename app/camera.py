import cv2
import logging
import time
import threading

STOP_CAMERA_AFTER_SECS = 30

class Camera:
    def __init__(self, device_id=0):
        self.device_id = device_id
        self.capturing = False
        self.logger = logging.getLogger("camera")
        self.last_accessed = time.time()
    
    def start_capture(self):
        if not self.capturing:
            self.capturing = True
            self.camera = cv2.VideoCapture(self.device_id)
            self.logger.info("start camera capture")
            threading.Timer(STOP_CAMERA_AFTER_SECS, self.stop_capture).start()
        else:
            self.logger.warn("camera already capturing")
    
    def stop_capture(self):
        secs_since_last_access = time.time() - self.last_accessed
        if self.capturing and secs_since_last_access > STOP_CAMERA_AFTER_SECS:
            self.capturing = False
            self.camera.release()
            print("camera capture stopped")
        if self.capturing and secs_since_last_access <= STOP_CAMERA_AFTER_SECS:
            print("camera still in use. will check later")
            threading.Timer(STOP_CAMERA_AFTER_SECS, self.stop_capture).start()
        else:
            print("camera already stopped")
    
    def get_frame_bytes(self):
        if not self.capturing:
            self.start_capture()
        self.last_accessed = time.time()
        success, frame = self.camera.read()
        if not success:
            self.logger.error("error reading from camera")
            return None
        else:
            # print("Resolution: " + str(frame.shape[0]) + " x " + str(frame.shape[1]))
            ret, buffer = cv2.imencode('.jpg', frame)
            return buffer.tobytes()

instance = Camera(device_id=0)