import logging
import logging.config

from crac_client.streaming import start_server, stop_server


logging.config.fileConfig('logging.conf')


from crac_client import config, gui
from crac_client.converter.button_converter import ButtonConverter
from crac_client.converter.camera_converter import CameraConverter
from crac_client.converter.curtains_converter import CurtainsConverter
from crac_client.converter.roof_converter import RoofConverter
from crac_client.converter.telescope_converter import TelescopeConverter
from crac_client.gui_constants import GuiKey
from crac_client.jobs import JOBS
from crac_client.retriever.button_retriever import ButtonRetriever
from crac_client.retriever.camera_retriever import CameraRetriever
from crac_client.retriever.curtains_retriever import CurtainsRetriever
from crac_client.retriever.roof_retriever import RoofRetriever
from crac_client.retriever.telescope_retriever import TelescopeRetriever
from crac_protobuf.button_pb2 import ButtonKey
from crac_protobuf.camera_pb2 import CameraAction
from crac_protobuf.curtains_pb2 import CurtainsAction
from crac_protobuf.roof_pb2 import RoofAction
from crac_protobuf.telescope_pb2 import TelescopeAction


logger = logging.getLogger('crac_client.app')
g_ui = gui.Gui()
roof_retriever = RoofRetriever(RoofConverter())
button_retriever = ButtonRetriever(ButtonConverter())
telescope_retriever = TelescopeRetriever(TelescopeConverter())
curtains_retriever = CurtainsRetriever(CurtainsConverter())
camera_retriever = CameraRetriever(CameraConverter())
camera_retriever.listCameras()


def deque():
    while len(JOBS) > 0:
        logger.debug(f"there are {len(JOBS)} jobs")
        job = JOBS.popleft()
        job['convert'](job['response'], g_ui)

deque()

start_server()

while True:
    timeout = config.Config.getInt("sleep", "automazione")
    v, _ = g_ui.win.Read(timeout=timeout)
    logger.debug(f"Premuto pulsante: {v}")
    match v:
        case v if v in [None, GuiKey.EXIT, GuiKey.SHUTDOWN]:
            g_ui = None
            telescope_retriever.setAction(action=TelescopeAction.Name(TelescopeAction.TELESCOPE_DISCONNECT), autolight=False)
            camera_retriever.setAction(action=CameraAction.Name(CameraAction.CAMERA_DISCONNECT), name="camera1", g_ui=g_ui)
            camera_retriever.setAction(action=CameraAction.Name(CameraAction.CAMERA_DISCONNECT), name="camera2", g_ui=g_ui)
            deque()
            stop_server()
            break
        case ButtonKey.KEY_ROOF:
            roof_retriever.setAction(action=g_ui.win[v].metadata)
        case v if v in ButtonRetriever.key_to_button_type_conversion.keys():
            button_retriever.setAction(action=g_ui.win[v].metadata, key=v, g_ui=g_ui)
        case v if v in TelescopeRetriever.key_to_telescope_action_conversion:
            telescope_retriever.setAction(action=g_ui.win[v].metadata, autolight=g_ui.is_autolight())
        case v if v in CurtainsRetriever.key_to_curtains_action_conversion:
            curtains_retriever.setAction(action=g_ui.win[v].metadata)
        case ButtonKey.KEY_CAMERA1_CONNECTION | ButtonKey.KEY_CAMERA1_DISPLAY:
            connection_button = g_ui.win[v]
            camera_retriever.setAction(action=connection_button.metadata, name="camera1", g_ui=g_ui)
        case ButtonKey.KEY_CAMERA2_CONNECTION | ButtonKey.KEY_CAMERA2_DISPLAY:
            connection_button = g_ui.win[v]
            camera_retriever.setAction(action=connection_button.metadata, name="camera2", g_ui=g_ui)
        case _:
            roof_retriever.setAction(action=RoofAction.Name(RoofAction.CHECK_ROOF))
            telescope_retriever.setAction(action=TelescopeAction.Name(TelescopeAction.CHECK_TELESCOPE), autolight=g_ui.is_autolight())
            curtains_retriever.setAction(action=CurtainsAction.Name(CurtainsAction.CHECK_CURTAIN))
            camera_retriever.setAction(action=CameraAction.Name(CameraAction.CAMERA_CHECK), name="camera1", g_ui=g_ui)
            camera_retriever.setAction(action=CameraAction.Name(CameraAction.CAMERA_CHECK), name="camera2", g_ui=g_ui)
            button_retriever.getStatus()
            
    deque()

