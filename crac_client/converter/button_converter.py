
from crac_protobuf.button_pb2 import (
    ButtonStatus,
    ButtonType
)
from crac_client.gui_constants import GuiLabel


class ButtonConverter:
    def convert(self, response, g_ui):
        if response.type == ButtonType.TELE_SWITCH:
            if response.status == ButtonStatus.OFF:
                g_ui.update_disable_button_power_switch_off()
            elif response.status == ButtonStatus.ON:
                g_ui.update_disable_button_power_switch_on()
        elif response.type == ButtonType.CCD_SWITCH:
            if response.status == ButtonStatus.OFF:
                g_ui.update_disable_button_power_off_ccd()
            elif response.status == ButtonStatus.ON:
                g_ui.update_disable_button_power_on_ccd()
        elif response.type == ButtonType.FLAT_LIGHT:  
            if response.status == ButtonStatus.OFF:
                g_ui.update_disable_panel_off()
            elif response.status == ButtonStatus.ON:
                g_ui.update_disable_panel_on()
        elif response.type == ButtonType.DOME_LIGHT:
            if response.status == ButtonStatus.OFF:
                g_ui.update_disable_button_light_off()
            elif response.status == ButtonStatus.ON:
                g_ui.update_disable_button_light_on()
            
