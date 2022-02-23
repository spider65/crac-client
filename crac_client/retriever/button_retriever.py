from crac_client.converter.button_converter import ButtonConverter
from crac_client.gui import Gui
from crac_client.retriever.retriever import Retriever
from crac_protobuf.button_pb2 import (
    ButtonAction,
    ButtonType,
    ButtonRequest,
    ButtonsRequest,
    ButtonResponse,
    ButtonsResponse,
)
from crac_protobuf.button_pb2_grpc import (
    ButtonStub,
)


class ButtonRetriever(Retriever):
    def __init__(self, g_ui: Gui) -> None:
        super().__init__(g_ui)
        self.client = ButtonStub(self.channel)

    def setAction(self, buttonAction: ButtonAction, buttonType: ButtonType):
        request = ButtonRequest(action=buttonAction, type=buttonType)
        call_future = self.client.SetAction.future(request, wait_for_ready=True)
        call_future.add_done_callback(self.callback)

    def getStatus(self):
        call_future = self.client.GetStatus.future(ButtonsRequest(), wait_for_ready=True)
        call_future.add_done_callback(self.callback)
    
    def converter(self, response: object, g_ui: Gui):
        if isinstance(response, (ButtonResponse)):
            ButtonConverter().convert(response, g_ui)
        elif isinstance(response, (ButtonsResponse)):
            ButtonConverter().buttons_convert(response, g_ui)
