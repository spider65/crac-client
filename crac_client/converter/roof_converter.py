from crac_client.gui import Gui
from crac_client.gui_constants import GuiLabel
from crac_protobuf.roof_pb2 import (
    RoofStatus,
    RoofResponse,
)


class RoofConverter:
    def convert(self, response: RoofResponse, g_ui: Gui):
        if response.status is RoofStatus.ROOF_CLOSED:
            g_ui.hide_background_image()
            g_ui.update_status_roof(GuiLabel.ROOF_CLOSED.value)
            g_ui.update_enable_button_open_roof()
        elif response.status is RoofStatus.ROOF_OPENED:
            g_ui.show_background_image()
            g_ui.update_status_roof(GuiLabel.ROOF_OPEN.value, text_color="#2c2825", background_color="green")
            g_ui.update_enable_disable_button()
