import cv2
import logging

class Camera:
    def __init__(self, device_id=0):
        self.device_id = device_id
        self.capturing = False
        self.logger = logging.getLogger("camera")
    
    def start_capture(self):
        if not self.capturing:
            self.capturing = True
            self.camera = cv2.VideoCapture(self.device_id)
            self.logger.info("start camera capture")
        else:
            self.logger.warn("camera already capturing")
    
    def stop_capture(self):
        if self.capturing:
            self.capturing = False
            self.camera.release()
            self.logger.info("camera capture stopped")
        else:
            self.logger.warn("camera already stopped")
    
    def get_frame_bytes(self):
        if not self.capturing:
            self.start_capture()
        success, frame = self.camera.read()
        if not success:
            self.logger.error("error reading from camera")
            return None
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            return buffer.tobytes()

instance = Camera(device_id=0)