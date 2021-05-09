from flask import (
    Blueprint, render_template, Response
)
from . import camera

def create_video_bp():
    bp = Blueprint("video", __name__, url_prefix="/video")
    cam = camera.instance
    
    @bp.route("/", methods=["GET"])
    def video():
        return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')
    
    def gen_frames():
        while True:
            yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + cam.get_frame_bytes() + b'\r\n')

    return bp




# @bp.route("/", methods=["GET"])
# def video():
#     return "test"
    # return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

# def gen_frames():
#     if (not cam_init):
#         print("init camera")
#         camera = cv2.VideoCapture(0)
#         cam_init = True
#     while True:
#         success, frame = camera.read()  # read the camera frame
#         if not success:
#             break
#         else:
#             ret, buffer = cv2.imencode('.jpg', frame)
#             frame = buffer.tobytes()
#             yield (b'--frame\r\n'
#                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result view raw
