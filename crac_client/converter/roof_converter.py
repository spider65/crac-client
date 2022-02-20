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
        elif response.status is RoofStatus.ROOF_CLOSING:
            g_ui.show_background_image()
            g_ui.update_status_roof(GuiLabel.ROOF_CLOSING.value, text_color="#2c2825", background_color="green")
            g_ui.toggle_curtains_buttons(is_disable=True)
            g_ui.update_disable_button_close_roof()
            g_ui.update_disable_button_open_roof()
        elif response.status is RoofStatus.ROOF_OPENING:
            g_ui.show_background_image()
            g_ui.update_status_roof(GuiLabel.ROOF_OPENING.value, text_color="#2c2825", background_color="green")
            g_ui.toggle_curtains_buttons(is_disable=True)
            g_ui.update_disable_button_close_roof()
            g_ui.update_disable_button_open_roof()