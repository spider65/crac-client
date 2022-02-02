
from crac_protobuf.button_pb2 import ButtonStatus
from crac_client.gui_constants import GuiLabel


class ButtonConverter:
    def convert(self, response, g_ui):
        if response.status == ButtonStatus.OFF:
            g_ui.update_disable_button_power_switch_off()
        elif response.status == ButtonStatus.ON:
            g_ui.update_disable_button_power_switch_on()
