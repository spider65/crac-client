from threading import Thread
from crac_client.config import Config
from crac_client.converter.converter import Converter
from crac_client.gui import Gui
from crac_client.jobs import JOBS
from crac_client.retriever.retriever import Retriever
from crac_protobuf.camera_pb2 import (
    CameraAction,
    CameraRequest,
    CameraResponse,
    Move,
)
from crac_protobuf.camera_pb2_grpc import (
    CameraStub,
)
import grpc


class CameraRetriever:
    def __init__(self) -> None:
        self.channel = grpc.insecure_channel(f'{Config.getValue("ip", "server")}:{Config.getValue("port", "server")}')
        self.client = CameraStub(self.channel)

    def video(self):
        return self.client.Video(CameraRequest(), wait_for_ready=True)
