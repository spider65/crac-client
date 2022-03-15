from flask import Flask, render_template, Response
from crac_client.retriever.camera_retriever import CameraRetriever


STREAMING = Flask(__name__)
camera_retriever = CameraRetriever()

@STREAMING.route('/video_feed')
def video_feed():
    #Video streaming route. Put this in the src attribute of an img tag
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

def gen_frames():
    for response in camera_retriever.video():
        yield response.video

@STREAMING.route('/')
def index():
    """Video streaming home page."""
    return render_template('index.html')

if __name__ == '__main__':
    STREAMING.run(debug=True)
