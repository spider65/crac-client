from array import array
import enum
import logging
import logging.config


logging.config.fileConfig('logging.conf')


from crac_protobuf.roof_pb2 import (
    RoofAction,
)
from crac_protobuf.button_pb2 import (
    ButtonAction,
    ButtonType,
)
from crac_protobuf.telescope_pb2 import (
    TelescopeAction,
)
from crac_protobuf.curtains_pb2 import (
    CurtainsAction
)
from crac_client import config, gui
from crac_client.gui_constants import GuiKey
from crac_client.retriever.button_retriever import ButtonRetriever
from crac_client.retriever.curtains_retriever import CurtainsRetriever
from crac_client.retriever.roof_retriever import RoofRetriever
from crac_client.retriever.telescope_retriever import TelescopeRetriever


logger = logging.getLogger('crac_client.app')
def list_buttons_names(enum_type_wrapper: enumerate) -> list[str]:
    return [
        enum_type_wrapper.Name(curtainsAction) for curtainsAction in enum_type_wrapper.values()
    ]


g_ui = gui.Gui()
while True:
    timeout = config.Config.getInt("sleep", "automazione")
    v, _ = g_ui.win.Read(timeout=timeout)
    logger.info(f"Premuto pulsante: {v}")

    if v is None or v is GuiKey.EXIT or v is GuiKey.SHUTDOWN:
        break
    elif v == "ROOF":
        retriever = RoofRetriever(g_ui)
        retriever.setAction(action=int(RoofAction.Value(g_ui.win[v].metadata)))
    elif v in list_buttons_names(ButtonType):
        if v == ButtonType.Name(ButtonType.DOME_LIGHT):
            logger.debug("is inside check for dome light")
            g_ui.set_autolight(False)
        retriever = ButtonRetriever(g_ui)
        retriever.setAction(action=int(ButtonAction.Value(g_ui.win[v].metadata)), buttonType=ButtonType.Value(v))
    elif v in list_buttons_names(TelescopeAction):
        retriever = TelescopeRetriever(g_ui)
        retriever.setAction(action=int(TelescopeAction.Value(g_ui.win[v].Key)), autolight=g_ui.is_autolight())
    elif v in list_buttons_names(CurtainsAction):
        retriever = CurtainsRetriever(g_ui)
        retriever.setAction(action=int(CurtainsAction.Value(g_ui.win[v].metadata)))
    else:
        retriever = RoofRetriever(g_ui)
        retriever.setAction(RoofAction.CHECK_ROOF)

        retriever = TelescopeRetriever(g_ui)
        retriever.setAction(TelescopeAction.CHECK_TELESCOPE, g_ui.is_autolight())

        retriever = CurtainsRetriever(g_ui)
        retriever.setAction(CurtainsAction.CHECK_CURTAIN)

        retriever = ButtonRetriever(g_ui)
        retriever.getStatus()

