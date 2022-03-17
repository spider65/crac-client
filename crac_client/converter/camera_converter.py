

import logging
from crac_client.converter.converter import Converter
from crac_client.gui import Gui
from crac_client.loc import _name
from crac_protobuf.camera_pb2 import (
    CameraAction,
    CameraResponse,
)

logger = logging.getLogger(__name__)


class CameraConverter(Converter):
    
    def convert(self, response: CameraResponse, g_ui: Gui):
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

