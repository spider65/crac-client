from time import sleep
from flask import Flask, render_template, Response
from crac_client.retriever.camera_retriever import CameraRetriever
from crac_protobuf.camera_pb2 import CameraRequest
import cv2


app = Flask(__name__)
camera_retriever = CameraRetriever()

@app.route('/video_feed')
def video_feed():
    #Video streaming route. Put this in the src attribute of an img tag
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

def gen_frames():
    for response in camera_retriever.client.Video(CameraRequest(), wait_for_ready=True):
        yield response.video

@app.route('/')
def index():
    """Video streaming home page."""
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
