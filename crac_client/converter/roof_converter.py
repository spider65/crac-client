
from crac_protobuf.roof_pb2 import RoofStatus
from crac_client.gui_constants import GuiLabel


class RoofConverter:
    def convert(self, response, g_ui):
        if response.status == RoofStatus.ROOF_CLOSED:
            g_ui.hide_background_image()
            g_ui.update_status_roof(GuiLabel.ROOF_CLOSED)
            g_ui.update_enable_button_open_roof()
        elif response.status == RoofStatus.ROOF_OPENED:
            g_ui.show_background_image()
            g_ui.update_status_roof(GuiLabel.ROOF_OPEN, text_color="#2c2825", background_color="green")
            g_ui.update_enable_disable_button()