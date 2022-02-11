import logging
from crac_client.config import Config
from crac_client.converter.button_converter import ButtonConverter
from crac_client.converter.curtains_converter import CurtainsConverter
from crac_client.converter.roof_converter import RoofConverter
from crac_client.converter.telescope_converter import TelescopeConverter
from crac_client.gui import Gui
from crac_protobuf.button_pb2 import (
    ButtonResponse,
    ButtonsResponse,
)
from crac_protobuf.curtains_pb2 import (
    CurtainsResponse,
)
from crac_protobuf.roof_pb2 import (
    RoofResponse,
)
from crac_protobuf.telescope_pb2 import (
    TelescopeResponse,
)
import grpc


logger = logging.getLogger('crac_client.app')


class Retriever:
    def __init__(self, g_ui: Gui) -> None:
        
        self.channel = grpc.insecure_channel(f'{Config.getValue("ip", "server")}:{Config.getValue("port", "server")}')
        self.g_ui = g_ui

    def callback(self, call_future):
        try:
            response = call_future.result()
            logger.info(f"response to be converted is {response}")
        except BaseException as err:
            logger.error(f"the retrieval of the response threw an error {err=}, {type(err)=}")
        else:
            self.converter(response, self.g_ui)
            self.channel.close()
    
    def converter(self, response: object, g_ui: Gui):
        raise NotImplementedError()