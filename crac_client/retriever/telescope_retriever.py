from crac_protobuf.telescope_pb2 import (
    TelescopeAction,
    TelescopeRequest
)
from crac_protobuf.telescope_pb2_grpc import TelescopeStub
import grpc


channel = grpc.insecure_channel("localhost:50051")
client = TelescopeStub(channel)


class TelescopeRetriever:
    def setAction(self, telescopeAction: TelescopeAction):
        request = TelescopeRequest(action=telescopeAction)
        call_future = client.SetAction.future(request)
        return call_future