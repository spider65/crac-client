from crac_protobuf.roof_pb2 import (
    RoofAction,
    RoofRequest
)
from crac_protobuf.roof_pb2_grpc import (
    RoofStub,
)
import grpc


channel = grpc.insecure_channel("localhost:50051")
client = RoofStub(channel)


class RoofRetriever:

    def setAction(self, roofAction: RoofAction):
        request = RoofRequest(action=roofAction)
        call_future = client.SetAction.future(request)
        return call_future
