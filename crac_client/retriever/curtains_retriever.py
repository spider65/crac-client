from crac_client.converter.curtains_converter import CurtainsConverter
from crac_client.gui import Gui
from crac_client.retriever.retriever import Retriever
from crac_protobuf.curtains_pb2 import (
    CurtainsAction,
    CurtainsRequest,
)
from crac_protobuf.curtains_pb2_grpc import CurtainStub
from crac_protobuf.button_pb2 import (
    ButtonKey,
)

class CurtainsRetriever(Retriever):
    def __init__(self, g_ui: Gui) -> None:
        super().__init__(g_ui)
        self.client = CurtainStub(self.channel)

    key_to_curtains_action_conversion = [
        ButtonKey.KEY_CURTAINS,
        ButtonKey.KEY_CALIBRATE,
    ]

    def setAction(self, action: str):
        request = CurtainsRequest(action=CurtainsAction.Value(action))
        call_future = self.client.SetAction.future(request, wait_for_ready=True)
        call_future.add_done_callback(self.callback)

    def converter(self, response: object, g_ui: Gui):
        CurtainsConverter().convert(response, g_ui)