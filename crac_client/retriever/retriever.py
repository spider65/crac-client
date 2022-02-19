from abc import ABC, abstractmethod
import logging
from crac_client.config import Config
from crac_client.gui import Gui
import grpc


logger = logging.getLogger('crac_client.app')


class Retriever(ABC):
    def __init__(self, g_ui: Gui) -> None:
        self.channel = grpc.insecure_channel(f'{Config.getValue("ip", "server")}:{Config.getValue("port", "server")}')
        self.g_ui = g_ui

    def callback(self, call_future) -> None:
        try:
            response = call_future.result()
            logger.info(f"response to be converted is {response}")
        except BaseException as err:
            logger.error(f"the retrieval of the response threw an error {err=}, {type(err)=}")
        else:
            self.converter(response, self.g_ui)
            self.channel.close()

    @abstractmethod
    def converter(self, response: object, g_ui: Gui) -> None:
        raise NotImplementedError()