
from crac_protobuf.telescope_pb2 import (
    TelescopeStatus,
    TelescopeSpeed,
)
from crac_client.gui_constants import GuiLabel


class TelescopeConverter:
    def convert(self, response, g_ui):
        if response.sync:
            g_ui.update_status_sync(GuiLabel.TELESCOPE_SYNC_ON, text_color="#2c2825", background_color="green")
            g_ui.update_button_sync(disabled=True)
        else:
            g_ui.update_status_sync(GuiLabel.TELESCOPE_SYNC_OFF, text_color="red", background_color="white")
            g_ui.update_button_sync(disabled=False)
        
        if response.speed == TelescopeSpeed.DEFAULT:
            g_ui.update_status_tracking(GuiLabel.TELESCOPE_TRACKING_OFF, text_color="red", background_color="white")
            g_ui.update_status_slewing(GuiLabel.TELESCOPE_SLEWING_OFF, text_color="red", background_color="white")
        elif response.speed == TelescopeSpeed.TRACKING:
            g_ui.update_status_tracking(GuiLabel.TELESCOPE_TRACKING_ON, text_color="#2c2825", background_color="green")
            g_ui.update_status_slewing(GuiLabel.TELESCOPE_SLEWING_OFF, text_color="red", background_color="white")
        elif response.speed == TelescopeSpeed.CENTERING:
            g_ui.update_status_tracking(GuiLabel.TELESCOPE_TRACKING_OFF, text_color="red", background_color="white")
            g_ui.update_status_slewing(GuiLabel.TELESCOPE_SLEWING_OFF, text_color="red", background_color="white")
        elif response.speed == TelescopeSpeed.SLEWING:
            g_ui.update_status_tracking(GuiLabel.TELESCOPE_TRACKING_OFF, text_color="red", background_color="white")
            g_ui.update_status_slewing(GuiLabel.TELESCOPE_SLEWING_ON, text_color="#2c2825", background_color="green")
        
        if response.status == TelescopeStatus.PARKED:
            g_ui.update_status_tele(GuiLabel.TELESCOPE_PARKED, text_color="red", background_color="white")
        elif response.status == TelescopeStatus.FLATTER:
            g_ui.update_status_tele(GuiLabel.TELESCOPE_FLATTER, text_color="red", background_color="white")
        elif response.status == TelescopeStatus.SECURE:
            g_ui.update_status_tele(GuiLabel.TELESCOPE_SECURED, text_color="red", background_color="white")
        elif response.status == TelescopeStatus.LOST:
            g_ui.update_status_tele(GuiLabel.TELESCOPE_ANOMALY)
            g_ui.status_alert(GuiLabel.ALERT_THE_SKY_LOST)
        elif response.status == TelescopeStatus.ERROR:
            g_ui.update_status_tele(GuiLabel.TELESCOPE_ERROR)
            g_ui.status_alert(GuiLabel.ALERT_THE_SKY_ERROR)
        else:
            cardinal = vars(GuiLabel).get(f"TELESCOPE_{TelescopeStatus.Name(response.status)}")
            g_ui.update_status_tele(cardinal, text_color="#2c2825", background_color="green")

        g_ui.update_tele_text({"alt": response.aa_coords.alt, "az": response.aa_coords.az})
