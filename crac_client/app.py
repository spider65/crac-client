from crac_protobuf.roof_pb2 import (
    RoofAction,
    RoofResponse,
)
from crac_protobuf.button_pb2 import (
    ButtonAction,
    ButtonType,
    ButtonResponse,
)
from crac_client import config, gui
from crac_client.converter.button_converter import ButtonConverter
from crac_client.converter.roof_converter import RoofConverter
from crac_client.gui_constants import GuiKey
from crac_client.retriever.roof_retriever import RoofRetriever
from crac_client.retriever.button_retriever import ButtonRetriever

def callback(call_future):
    response = call_future.result()
    if isinstance(response, (RoofResponse)):
        converter = RoofConverter().convert
    elif isinstance(response, (ButtonResponse)):
        converter = ButtonConverter().convert

    converter(response, g_ui)

g_ui = gui.Gui()
while True:
    timeout = config.Config.getInt("sleep", "automazione")
    v, _ = g_ui.win.Read(timeout=timeout)

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