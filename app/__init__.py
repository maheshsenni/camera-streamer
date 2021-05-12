from flask import (
    Flask, render_template
)
from . import video

def create_app():
    app = Flask(__name__)

    app.register_blueprint(video.create_video_bp())

    @app.route("/")
    def home():
        return render_template("index.html")

    @app.route("/status")
    def status():
        return "Up"

    return app