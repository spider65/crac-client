import logging
import logging.config


logging.config.fileConfig('logging.conf')


from crac_client import config, gui
from crac_client.converter.button_converter import ButtonConverter
from crac_client.converter.curtains_converter import CurtainsConverter
from crac_client.converter.roof_converter import RoofConverter
from crac_client.converter.telescope_converter import TelescopeConverter
from crac_client.gui_constants import GuiKey
from crac_client.jobs import JOBS
from crac_client.retriever.button_retriever import ButtonRetriever
from crac_client.retriever.curtains_retriever import CurtainsRetriever
from crac_client.retriever.roof_retriever import RoofRetriever
from crac_client.retriever.telescope_retriever import TelescopeRetriever
from crac_protobuf.button_pb2 import ButtonKey
from crac_protobuf.curtains_pb2 import CurtainsAction
from crac_protobuf.roof_pb2 import RoofAction
from crac_protobuf.telescope_pb2 import TelescopeAction


logger = logging.getLogger('crac_client.app')
g_ui = gui.Gui()
roof_retriever = RoofRetriever(RoofConverter())
button_retriever = ButtonRetriever(ButtonConverter())
telescope_retriever = TelescopeRetriever(TelescopeConverter())
curtains_retriever = CurtainsRetriever(CurtainsConverter())


def deque():
    while len(JOBS) > 0:
        logger.debug(f"there are {len(JOBS)} jobs")
        job = JOBS.popleft()
        job['convert'](job['response'], g_ui)

while True:
    timeout = config.Config.getInt("sleep", "automazione")
    v, _ = g_ui.win.Read(timeout=timeout)
    logger.debug(f"Premuto pulsante: {v}")
    match v:
        case v if v in [None, GuiKey.EXIT, GuiKey.SHUTDOWN]:
            telescope_retriever.setAction(action=TelescopeAction.Name(TelescopeAction.TELESCOPE_DISCONNECT), autolight=False)
        case ButtonKey.KEY_ROOF:
            roof_retriever.setAction(action=g_ui.win[v].metadata)
        case v if v in ButtonRetriever.key_to_button_type_conversion.keys():
            button_retriever.setAction(action=g_ui.win[v].metadata, key=v, g_ui=g_ui)
        case v if v in TelescopeRetriever.key_to_telescope_action_conversion:
            telescope_retriever.setAction(action=g_ui.win[v].metadata, autolight=g_ui.is_autolight())
        case v if v in CurtainsRetriever.key_to_curtains_action_conversion:
            curtains_retriever.setAction(action=g_ui.win[v].metadata)
        case _:
            roof_retriever.setAction(RoofAction.Name(RoofAction.CHECK_ROOF))
            telescope_retriever.setAction(TelescopeAction.Name(TelescopeAction.CHECK_TELESCOPE), g_ui.is_autolight())
            curtains_retriever.setAction(CurtainsAction.Name(CurtainsAction.CHECK_CURTAIN))
            button_retriever.getStatus()
    deque()
