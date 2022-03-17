

import logging
from crac_client.converter.converter import Converter
from crac_client.gui import Gui
from crac_client.loc import _name
from crac_client.retriever.retriever import Retriever
from crac_client.streaming import start_server, stop_server
from crac_protobuf.camera_pb2 import (
    CameraAction,
    CameraResponse,
)

logger = logging.getLogger(__name__)


class CameraConverter(Converter):
    
    def convert(self, response: CameraResponse, g_ui: Gui, retriever: Retriever, camera_action: CameraAction):
        if camera_action is CameraAction.CAMERA_CONNECT:
            start_server(retriever=retriever)
        elif camera_action is CameraAction.CAMERA_DISCONNECT:
            stop_server()
        
        if g_ui is None:
            return
        
        for button_gui in response.buttons_gui:
            g_ui.win[button_gui.key](
                _name(button_gui.label),
                disabled=button_gui.is_disabled,
                button_color=(
                    button_gui.button_color.text_color, 
                    button_gui.button_color.background_color
                )
            )
            g_ui.win[button_gui.key].metadata = CameraAction.Name(button_gui.metadata)
        
