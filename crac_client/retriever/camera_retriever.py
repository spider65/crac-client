from crac_client.config import Config
from crac_client.gui import Gui
from crac_client.retriever.retriever import Retriever
from crac_client.streaming import start_server, stop_server
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


class CameraRetriever(Retriever):
    def __init__(self, converter) -> None:
        super().__init__(converter)
        self.channel = grpc.insecure_channel(f'{Config.getValue("ip", "server")}:{Config.getValue("port", "server")}')
        self.client = CameraStub(self.channel)

    def video(self) -> CameraResponse:
        return self.client.Video(CameraRequest(), wait_for_ready=True)

    def setAction(self, action, g_ui: Gui) -> CameraResponse:
        camera_action = CameraAction.Value(action)
        request = CameraRequest(action=camera_action)
        response = self.client.SetAction(request, wait_for_ready=True)
        self.converter.convert(response, g_ui, self, camera_action)
