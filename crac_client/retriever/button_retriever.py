from crac_client.gui import Gui
from crac_client.retriever.retriever import Retriever
from crac_protobuf.button_pb2 import (
    ButtonAction,
    ButtonType,
    ButtonRequest,
    ButtonsRequest,
)
from crac_protobuf.button_pb2_grpc import (
    ButtonStub,
)


class ButtonRetriever(Retriever):
    def __init__(self, g_ui: Gui) -> None:
        super().__init__(g_ui)
        self.client = ButtonStub(self.channel)

    def setAction(self, roofAction: ButtonAction, roofType: ButtonType):
        request = ButtonRequest(action=roofAction, type=roofType)
        call_future = self.client.SetAction.future(request, wait_for_ready=True)
        call_future.add_done_callback(self.callback)

    def getStatus(self):
        call_future = self.client.GetStatus.future(ButtonsRequest(), wait_for_ready=True)
        call_future.add_done_callback(self.callback)