from enum import auto
from crac_client.converter.telescope_converter import TelescopeConverter
from crac_client.gui import Gui
from crac_client.retriever.retriever import Retriever
from crac_protobuf.button_pb2 import (
    ButtonKey,
)
from crac_protobuf.telescope_pb2 import (
    TelescopeAction,
    TelescopeRequest,
)
from crac_protobuf.telescope_pb2_grpc import TelescopeStub


class TelescopeRetriever(Retriever):
    def __init__(self, g_ui: Gui) -> None:
        super().__init__(g_ui)
        self.client = TelescopeStub(self.channel)

    key_to_telescope_action_conversion = [
        ButtonKey.KEY_SYNC,
        ButtonKey.KEY_PARK,
        ButtonKey.KEY_FLAT,
    ]

    def setAction(self, action: str, autolight: bool):
        request = TelescopeRequest(action=TelescopeAction.Value(action), autolight=autolight)
        call_future = self.client.SetAction.future(request, wait_for_ready=True)
        call_future.add_done_callback(self.callback)

    def converter(self, response: object, g_ui: Gui):
        TelescopeConverter().convert(response, g_ui)