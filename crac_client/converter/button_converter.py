
from crac_client.gui import Gui
from crac_protobuf.button_pb2 import (
    ButtonStatus,
    ButtonType,
    ButtonsResponse,
    ButtonResponse,
)


class ButtonConverter:
    def convert(self, response: ButtonResponse, g_ui: Gui):
        if response.type is ButtonType.TELE_SWITCH:
            if response.status is ButtonStatus.OFF:
                g_ui.update_disable_button_power_switch_off()
            elif response.status is ButtonStatus.ON:
                g_ui.update_disable_button_power_switch_on()
        elif response.type is ButtonType.CCD_SWITCH:
            if response.status is ButtonStatus.OFF:
                g_ui.update_disable_button_power_off_ccd()
            elif response.status is ButtonStatus.ON:
                g_ui.update_disable_button_power_on_ccd()
        elif response.type is ButtonType.FLAT_LIGHT:  
            if response.status is ButtonStatus.OFF:
                g_ui.update_disable_panel_off()
            elif response.status is ButtonStatus.ON:
                g_ui.update_disable_panel_on()
        elif response.type is ButtonType.DOME_LIGHT:
            if response.status is ButtonStatus.OFF:
                g_ui.update_disable_button_light_off()
            elif response.status is ButtonStatus.ON:
                g_ui.update_disable_button_light_on()
            
    def buttons_convert(self, response: ButtonsResponse, g_ui: Gui):
        for button in response.buttons:
            self.convert(button, g_ui)
