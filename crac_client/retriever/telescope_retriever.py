from enum import auto
from crac_client.converter.telescope_converter import TelescopeConverter
from crac_client.gui import Gui
from crac_client.retriever.retriever import Retriever
from crac_protobuf.telescope_pb2 import (
    TelescopeAction,
    TelescopeRequest,
)
from crac_protobuf.telescope_pb2_grpc import TelescopeStub


class TelescopeRetriever(Retriever):
    def __init__(self, g_ui: Gui) -> None:
        super().__init__(g_ui)
        self.client = TelescopeStub(self.channel)

    def setAction(self, telescopeAction: TelescopeAction, autolight: bool):
        request = TelescopeRequest(action=telescopeAction, autolight=autolight)
        call_future = self.client.SetAction.future(request, wait_for_ready=True)
        call_future.add_done_callback(self.callback)

    def converter(self, response: object, g_ui: Gui):
        TelescopeConverter().convert(response, g_ui)