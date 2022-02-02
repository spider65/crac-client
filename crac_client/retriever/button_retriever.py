from crac_protobuf.button_pb2 import (
    ButtonAction,
    ButtonType,
    ButtonRequest
)
from crac_protobuf.button_pb2_grpc import (
    ButtonStub,
)
import grpc

channel = grpc.insecure_channel("localhost:50051")
client = ButtonStub(channel)


class ButtonRetriever:

    def setAction(self, roofAction: ButtonAction, roofType: ButtonType):
        request = ButtonRequest(action=roofAction, type=roofType)
        call_future = client.SetAction.future(request)
        return call_future
