from crac_client.gui import Gui
from crac_client.retriever.retriever import Retriever
from crac_protobuf.roof_pb2 import (
    RoofAction,
    RoofRequest
)
from crac_protobuf.roof_pb2_grpc import (
    RoofStub,
)


class RoofRetriever(Retriever):
    def __init__(self, g_ui: Gui) -> None:
        super().__init__(g_ui)
        self.client = RoofStub(self.channel)

    def setAction(self, roofAction: RoofAction):
        request = RoofRequest(action=roofAction)
        call_future = self.client.SetAction.future(request, wait_for_ready=True)
        call_future.add_done_callback(self.callback)
