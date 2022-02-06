import logging
import logging.config


logging.config.fileConfig('logging.conf')


from crac_protobuf.roof_pb2 import (
    RoofAction,
    RoofResponse,
)
from crac_protobuf.button_pb2 import (
    ButtonAction,
    ButtonType,
    ButtonResponse,
)
from crac_protobuf.telescope_pb2 import (
    TelescopeAction,
    TelescopeResponse,
)
from crac_client import config, gui
from crac_client.converter.button_converter import ButtonConverter
from crac_client.converter.roof_converter import RoofConverter
from crac_client.converter.telescope_converter import TelescopeConverter
from crac_client.gui_constants import GuiKey
from crac_client.retriever.roof_retriever import RoofRetriever
from crac_client.retriever.button_retriever import ButtonRetriever
from crac_client.retriever.telescope_retriever import TelescopeRetriever


logger = logging.getLogger('crac_client.app')


def callback(call_future):
    response = call_future.result()
    logger.info(f"response to be converted is {response}")
    if isinstance(response, (RoofResponse)):
        converter = RoofConverter().convert
    elif isinstance(response, (ButtonResponse)):
        converter = ButtonConverter().convert
    elif isinstance(response, (TelescopeResponse)):
        converter = TelescopeConverter().convert

    converter(response, g_ui)

g_ui = gui.Gui()
while True:
    timeout = config.Config.getInt("sleep", "automazione")
    v, _ = g_ui.win.Read(timeout=timeout)
    logger.info(f"Premuto pulsante: {v}")

    if v is None or v is GuiKey.EXIT or v is GuiKey.SHUTDOWN:
        break
    elif v is GuiKey.CLOSE_ROOF:
        retriever = RoofRetriever()
        call_future = retriever.setAction(RoofAction.CLOSE)
        call_future.add_done_callback(callback)
    elif v is GuiKey.OPEN_ROOF:
        retriever = RoofRetriever()
        call_future = retriever.setAction(RoofAction.OPEN)
        call_future.add_done_callback(callback)
    elif v is GuiKey.POWER_ON_TELE:
        retriever = ButtonRetriever()
        call_future = retriever.setAction(ButtonAction.TURN_ON, ButtonType.TELE_SWITCH)
        call_future.add_done_callback(callback)
    elif v is GuiKey.POWER_OFF_TELE:
        retriever = ButtonRetriever()
        call_future = retriever.setAction(ButtonAction.TURN_OFF, ButtonType.TELE_SWITCH)
        call_future.add_done_callback(callback)
    elif v is GuiKey.POWER_ON_CCD:
        retriever = ButtonRetriever()
        call_future = retriever.setAction(ButtonAction.TURN_ON, ButtonType.CCD_SWITCH)
        call_future.add_done_callback(callback)
    elif v is GuiKey.POWER_OFF_CCD:
        retriever = ButtonRetriever()
        call_future = retriever.setAction(ButtonAction.TURN_OFF, ButtonType.CCD_SWITCH)
        call_future.add_done_callback(callback)
    elif v is GuiKey.LIGHT_ON:
        retriever = ButtonRetriever()
        call_future = retriever.setAction(ButtonAction.TURN_ON, ButtonType.DOME_LIGHT)
        call_future.add_done_callback(callback)
    elif v is GuiKey.LIGHT_OFF:
        retriever = ButtonRetriever()
        call_future = retriever.setAction(ButtonAction.TURN_OFF, ButtonType.DOME_LIGHT)
        call_future.add_done_callback(callback)
    elif v is GuiKey.PANEL_ON:
        retriever = ButtonRetriever()
        call_future = retriever.setAction(ButtonAction.TURN_ON, ButtonType.FLAT_LIGHT)
        call_future.add_done_callback(callback)
    elif v is GuiKey.PANEL_OFF:
        retriever = ButtonRetriever()
        call_future = retriever.setAction(ButtonAction.TURN_OFF, ButtonType.FLAT_LIGHT)
        call_future.add_done_callback(callback)
    elif v is GuiKey.SYNC_TELE:
        retriever = TelescopeRetriever()
        call_future = retriever.setAction(TelescopeAction.SYNC)
        call_future.add_done_callback(callback)
    elif v is GuiKey.PARK_TELE:
        retriever = TelescopeRetriever()
        call_future = retriever.setAction(TelescopeAction.PARK_POSITION)
        call_future.add_done_callback(callback)
    elif v is GuiKey.FLAT_TELE:
        retriever = TelescopeRetriever()
        call_future = retriever.setAction(TelescopeAction.FLAT_POSITION)
        call_future.add_done_callback(callback)
    else:
        retriever = TelescopeRetriever()
        response = retriever.setImmediateAction(TelescopeAction.CHECK_TELESCOPE)
        converter = TelescopeConverter().convert(response, g_ui)