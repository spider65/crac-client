import logging
from threading import Thread
from flask import Flask, render_template, Response
from crac_client.retriever.retriever import Retriever
from crac_protobuf.camera_pb2 import (
    CameraStatus,
)
from werkzeug.serving import make_server


logger = logging.getLogger(__name__)
app = Flask(__name__)


@app.route('/video_feed')
def video_feed():
    #Video streaming route. Put this in the src attribute of an img tag
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

def gen_frames():
    stream = camera_retriever.video()
    for response in stream:
        if response.status is CameraStatus.CAMERA_DISCONNECTED:
            stream.cancel()
            break
        yield response.video

@app.route('/')
def index():
    """Video streaming home page."""
    return render_template('index.html')

def start_server(retriever: Retriever):
    global server, camera_retriever
    camera_retriever = retriever
    server = ServerThread(app)
    server.start()
    logger.info('server started')

def stop_server():
    global server
    server.shutdown()


class ServerThread(Thread):

    def __init__(self, app):
        Thread.__init__(self)
        self.server = make_server('127.0.0.1', 5000, app)
        self.ctx = app.app_context()
        self.ctx.push()

    def run(self):
        logger.info('starting server')
        self.server.serve_forever()

    def shutdown(self):
        self.server.shutdown()