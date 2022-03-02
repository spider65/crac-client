from abc import ABC, abstractmethod
import logging
from typing import Any
from crac_client.gui import Gui
from crac_client.jobs import JOBS, JOBS_LOCKER


logger = logging.getLogger('crac_client.app')


class Retriever(ABC):
    def __init__(self, converter: Any) -> None:
        self.converter = converter

    def callback(self, call_future) -> None:
        try:
            response = call_future.result()
            logger.info(f"response to be converted is {response}")
        except BaseException as err:
            logger.error(f"the retrieval of the response threw an error {err=}, {type(err)=}")
            raise err
        else:
            JOBS.append({"convert": self.converter.convert, "response": response})
