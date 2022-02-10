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
from crac_client.converter.button_converter import ButtonConverter
from crac_client.converter.curtains_converter import CurtainsConverter
from crac_client.converter.roof_converter import RoofConverter
from crac_client.converter.telescope_converter import TelescopeConverter
from crac_client.gui_constants import GuiKey
from crac_client.retriever.button_retriever import ButtonRetriever
from crac_client.retriever.curtains_retriever import CurtainsRetriever
from crac_client.retriever.roof_retriever import RoofRetriever
from crac_client.retriever.telescope_retriever import TelescopeRetriever


logger = logging.getLogger('crac_client.app')


g_ui = gui.Gui()
while True:
    timeout = config.Config.getInt("sleep", "automazione")
    v, _ = g_ui.win.Read(timeout=timeout)
    logger.info(f"Premuto pulsante: {v}")

    if v is None or v is GuiKey.EXIT or v is GuiKey.SHUTDOWN:
        break
    elif v is GuiKey.CLOSE_ROOF:
        retriever = RoofRetriever(g_ui)
        retriever.setAction(RoofAction.CLOSE)
    elif v is GuiKey.OPEN_ROOF:
        retriever = RoofRetriever(g_ui)
        retriever.setAction(RoofAction.OPEN)
    elif v is GuiKey.POWER_ON_TELE:
        retriever = ButtonRetriever(g_ui)
        retriever.setAction(ButtonAction.TURN_ON, ButtonType.TELE_SWITCH)
    elif v is GuiKey.POWER_OFF_TELE:
        retriever = ButtonRetriever(g_ui)
        retriever.setAction(ButtonAction.TURN_OFF, ButtonType.TELE_SWITCH)
    elif v is GuiKey.POWER_ON_CCD:
        retriever = ButtonRetriever(g_ui)
        retriever.setAction(ButtonAction.TURN_ON, ButtonType.CCD_SWITCH)
    elif v is GuiKey.POWER_OFF_CCD:
        retriever = ButtonRetriever(g_ui)
        retriever.setAction(ButtonAction.TURN_OFF, ButtonType.CCD_SWITCH)
    elif v is GuiKey.LIGHT_ON:
        retriever = ButtonRetriever(g_ui)
        retriever.setAction(ButtonAction.TURN_ON, ButtonType.DOME_LIGHT)
    elif v is GuiKey.LIGHT_OFF:
        retriever = ButtonRetriever(g_ui)
        retriever.setAction(ButtonAction.TURN_OFF, ButtonType.DOME_LIGHT)
    elif v is GuiKey.PANEL_ON:
        retriever = ButtonRetriever(g_ui)
        retriever.setAction(ButtonAction.TURN_ON, ButtonType.FLAT_LIGHT)
    elif v is GuiKey.PANEL_OFF:
        retriever = ButtonRetriever(g_ui)
        retriever.setAction(ButtonAction.TURN_OFF, ButtonType.FLAT_LIGHT)
    elif v is GuiKey.SYNC_TELE:
        retriever = TelescopeRetriever(g_ui)
        retriever.setAction(TelescopeAction.SYNC)
    elif v is GuiKey.PARK_TELE:
        retriever = TelescopeRetriever(g_ui)
        retriever.setAction(TelescopeAction.PARK_POSITION)
    elif v is GuiKey.FLAT_TELE:
        retriever = TelescopeRetriever(g_ui)
        retriever.setAction(TelescopeAction.FLAT_POSITION)
    elif v is GuiKey.ENABLED_CURTAINS:
        retriever = CurtainsRetriever(g_ui)
        retriever.setAction(CurtainsAction.ENABLE)
    elif v is GuiKey.DISABLED_CURTAINS:
        retriever = CurtainsRetriever(g_ui)
        retriever.setAction(CurtainsAction.DISABLE)
    else:
        retriever = ButtonRetriever(g_ui)
        retriever.getStatus()

        retriever = RoofRetriever(g_ui)
        retriever.setAction(RoofAction.CHECK_ROOF)

        retriever = TelescopeRetriever(g_ui)
        retriever.setAction(TelescopeAction.CHECK_TELESCOPE)

        retriever = CurtainsRetriever(g_ui)
        retriever.setAction(CurtainsAction.CHECK_CURTAIN)

