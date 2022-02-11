from crac_client.gui import Gui
from crac_client.gui_constants import GuiLabel
from crac_protobuf.telescope_pb2 import (
    TelescopeStatus,
    TelescopeSpeed,
    TelescopeResponse,
)


class TelescopeConverter:
    def convert(self, response: TelescopeResponse, g_ui: Gui):
        if response.sync:
            g_ui.update_status_sync(GuiLabel.TELESCOPE_SYNC_ON.value, text_color="#2c2825", background_color="green")
            g_ui.update_button_sync(disabled=True)
        else:
            g_ui.update_status_sync(GuiLabel.TELESCOPE_SYNC_OFF.value, text_color="red", background_color="white")
            g_ui.update_button_sync(disabled=False)
        
        if response.speed is TelescopeSpeed.DEFAULT:
            g_ui.update_status_tracking(GuiLabel.TELESCOPE_TRACKING_OFF.value, text_color="red", background_color="white")
            g_ui.update_status_slewing(GuiLabel.TELESCOPE_SLEWING_OFF.value, text_color="red", background_color="white")
        elif response.speed is TelescopeSpeed.TRACKING:
            g_ui.update_status_tracking(GuiLabel.TELESCOPE_TRACKING_ON.value, text_color="#2c2825", background_color="green")
            g_ui.update_status_slewing(GuiLabel.TELESCOPE_SLEWING_OFF.value, text_color="red", background_color="white")
        elif response.speed is TelescopeSpeed.CENTERING:
            g_ui.update_status_tracking(GuiLabel.TELESCOPE_TRACKING_OFF.value, text_color="red", background_color="white")
            g_ui.update_status_slewing(GuiLabel.TELESCOPE_SLEWING_OFF.value, text_color="red", background_color="white")
        elif response.speed is TelescopeSpeed.SLEWING:
            g_ui.update_status_tracking(GuiLabel.TELESCOPE_TRACKING_OFF.value, text_color="red", background_color="white")
            g_ui.update_status_slewing(GuiLabel.TELESCOPE_SLEWING_ON.value, text_color="#2c2825", background_color="green")

        if response.status is TelescopeStatus.PARKED:
            g_ui.update_status_tele(GuiLabel.TELESCOPE_PARKED.value, text_color="red", background_color="white")
        elif response.status is TelescopeStatus.FLATTER:
            g_ui.update_status_tele(GuiLabel.TELESCOPE_FLATTER.value, text_color="red", background_color="white")
        elif response.status is TelescopeStatus.SECURE:
            g_ui.update_status_tele(GuiLabel.TELESCOPE_SECURED.value, text_color="red", background_color="white")
        elif response.status is TelescopeStatus.LOST:
            g_ui.update_status_tele(GuiLabel.TELESCOPE_ANOMALY.value)
            g_ui.status_alert(GuiLabel.ALERT_THE_SKY_LOST.value)
        elif response.status is TelescopeStatus.ERROR:
            g_ui.update_status_tele(GuiLabel.TELESCOPE_ERROR.value)
            g_ui.status_alert(GuiLabel.ALERT_THE_SKY_ERROR.value)
        else:
            cardinal = vars(GuiLabel).get(f"TELESCOPE_{TelescopeStatus.Name(response.status)}").value
            g_ui.update_status_tele(cardinal, text_color="#2c2825", background_color="green")

        g_ui.update_tele_text({"alt": response.aa_coords.alt, "az": response.aa_coords.az})
