from crac_client.gui import Gui
from crac_client.gui_constants import GuiLabel
from crac_protobuf.roof_pb2 import (
    RoofStatus,
    RoofResponse,
    RoofAction,
)


class RoofConverter:
    def convert(self, response: RoofResponse, g_ui: Gui):
        if response.status is RoofStatus.ROOF_CLOSED:
            g_ui.hide_background_image()
            name = GuiLabel.ROOF_CLOSED.value
        elif response.status is RoofStatus.ROOF_OPENED:
            g_ui.show_background_image()
            name = GuiLabel.ROOF_OPEN.value
        elif response.status is RoofStatus.ROOF_CLOSING:
            g_ui.show_background_image()
            name = GuiLabel.ROOF_CLOSING.value
        elif response.status is RoofStatus.ROOF_OPENING:
            g_ui.show_background_image()
            name = GuiLabel.ROOF_OPENING.value

        g_ui.win[response.button_gui.key](
            name, 
            disabled=response.button_gui.is_disabled,
            button_color=(
                response.button_gui.button_color.text_color, 
                response.button_gui.button_color.background_color
            )
        )
        g_ui.win[response.button_gui.key].metadata = RoofAction.Name(response.button_gui.metadata)
