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
        self.t: Thread = None

    # key_to_button_type_conversion = {
    #     ButtonKey.KEY_TELE_SWITCH: ButtonType.TELE_SWITCH,
    #     ButtonKey.KEY_CCD_SWITCH: ButtonType.CCD_SWITCH,
    #     ButtonKey.KEY_FLAT_LIGHT: ButtonType.FLAT_LIGHT,
    #     ButtonKey.KEY_DOME_LIGHT: ButtonType.DOME_LIGHT,
    # }

    # def setAction(self, action: str, key: ButtonKey, g_ui: Gui):
    #     if key is ButtonKey.KEY_DOME_LIGHT:
    #         g_ui.set_autolight(False)
    #     request = ButtonRequest(action=ButtonAction.Value(action), type=ButtonRetriever.key_to_button_type_conversion[key])
    #     call_future = self.client.SetAction.future(request, wait_for_ready=True)
    #     call_future.add_done_callback(self.callback)

    def video(self):
        return self.client.Video(CameraRequest(), wait_for_ready=True)

    def __stream(self, responses: CameraResponse):
        for response in responses:
            yield (
                b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + response.video + b'\r\n'
            )  # concat frame one by one and show result


        #print(None)
        #JOBS.append({"convert": self.update, "response": None})
    
    def close(self):
        self.t.join(timeout=10)
    
    def update(self, video: bytes, g_ui: Gui):
        video_format = "flv"
        server_url = "http://127.0.0.1:8080"
