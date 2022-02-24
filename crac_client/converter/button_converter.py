
from crac_client.gui import Gui
from crac_protobuf.button_pb2 import (
    ButtonAction,
    ButtonType,
    ButtonsResponse,
    ButtonResponse,
)

from crac_client.gui_constants import GuiKey


class ButtonConverter:
    def convert(self, response: ButtonResponse, g_ui: Gui):
        g_ui.win[ButtonType.Name(response.type)](
            response.button_gui.name, 
            disabled=response.button_gui.is_disabled,
            button_color=(
                response.button_gui.button_color.text_color, 
                response.button_gui.button_color.background_color
            )
        )
        g_ui.win[ButtonType.Name(response.type)].metadata = ButtonAction.Name(response.button_gui.metadata)

    def buttons_convert(self, response: ButtonsResponse, g_ui: Gui):
        for button in response.buttons:
            self.convert(button, g_ui)
