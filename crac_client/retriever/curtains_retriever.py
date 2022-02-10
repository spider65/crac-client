from crac_client.gui import Gui
from crac_client.retriever.retriever import Retriever
from crac_protobuf.curtains_pb2 import (
    CurtainsAction,
    CurtainsRequest,
)
from crac_protobuf.curtains_pb2_grpc import CurtainStub


class CurtainsRetriever(Retriever):
    def __init__(self, g_ui: Gui) -> None:
        super().__init__(g_ui)
        self.client = CurtainStub(self.channel)

    def setAction(self, action: CurtainsAction):
        request = CurtainsRequest(action=action)
        call_future = self.client.SetAction.future(request, wait_for_ready=True)
        call_future.add_done_callback(self.callback)
