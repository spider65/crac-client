import logging
from crac_client.gui import Gui
from crac_client.gui_constants import GuiLabel
from crac_protobuf.telescope_pb2 import (
    TelescopeStatus,
    TelescopeSpeed,
    TelescopeResponse,
)


logger = logging.getLogger(__name__)


class TelescopeConverter:
    def convert(self, response: TelescopeResponse, g_ui: Gui):
        if response.sync:
            g_ui.update_status_sync(GuiLabel.TELESCOPE_SYNC_ON.value, text_color="#2c2825", background_color="green")
            g_ui.update_button_sync(is_disabled=True)
        else:
            g_ui.update_status_sync(GuiLabel.TELESCOPE_SYNC_OFF.value, text_color="red", background_color="white")
            g_ui.update_button_sync(is_disabled=False)
        
        if response.speed is TelescopeSpeed.SPEED_NOT_TRACKING:
            g_ui.update_status_tracking(GuiLabel.TELESCOPE_TRACKING_OFF.value, text_color="red", background_color="white")
            g_ui.update_status_slewing(GuiLabel.TELESCOPE_SLEWING_OFF.value, text_color="red", background_color="white")
        elif response.speed is TelescopeSpeed.SPEED_TRACKING:
            g_ui.update_status_tracking(GuiLabel.TELESCOPE_TRACKING_ON.value, text_color="#2c2825", background_color="green")
            g_ui.update_status_slewing(GuiLabel.TELESCOPE_SLEWING_OFF.value, text_color="red", background_color="white")
        elif response.speed is TelescopeSpeed.SPEED_CENTERING or response.speed is TelescopeSpeed.SPEED_ERROR:
            g_ui.update_status_tracking(GuiLabel.TELESCOPE_TRACKING_OFF.value, text_color="red", background_color="white")
            g_ui.update_status_slewing(GuiLabel.TELESCOPE_SLEWING_OFF.value, text_color="red", background_color="white")
        elif response.speed is TelescopeSpeed.SPEED_SLEWING:
            g_ui.update_status_tracking(GuiLabel.TELESCOPE_TRACKING_OFF.value, text_color="red", background_color="white")
            g_ui.update_status_slewing(GuiLabel.TELESCOPE_SLEWING_ON.value, text_color="#2c2825", background_color="green")

        if response.status is TelescopeStatus.PARKED:
            g_ui.update_status_tele(GuiLabel.TELESCOPE_PARKED.value, text_color="red", background_color="white")
            g_ui.update_button_park(is_disabled=True)
            g_ui.update_button_flat(is_disabled=False)
        elif response.status is TelescopeStatus.FLATTER:
            g_ui.update_status_tele(GuiLabel.TELESCOPE_FLATTER.value, text_color="red", background_color="white")
            g_ui.update_button_park(is_disabled=False)
            g_ui.update_button_flat(is_disabled=True)
        elif response.status is TelescopeStatus.SECURE:
            g_ui.update_status_tele(GuiLabel.TELESCOPE_SECURED.value, text_color="red", background_color="white")
            g_ui.update_button_park(is_disabled=False)
            g_ui.update_button_flat(is_disabled=False)
        elif response.status is TelescopeStatus.LOST:
            g_ui.update_status_tele(GuiLabel.TELESCOPE_ANOMALY.value)
            g_ui.status_alert(GuiLabel.ALERT_TELESCOPE_LOST.value)
            g_ui.update_button_park(is_disabled=True)
            g_ui.update_button_flat(is_disabled=True)
        elif response.status is TelescopeStatus.ERROR:
            g_ui.update_status_tele(GuiLabel.TELESCOPE_ERROR.value)
            g_ui.status_alert(GuiLabel.ALERT_TELESCOPE_ERROR.value)
            g_ui.update_button_park(is_disabled=True)
            g_ui.update_button_flat(is_disabled=True)
        else:
            cardinal = vars(GuiLabel).get(f"TELESCOPE_{TelescopeStatus.Name(response.status)}").value
            g_ui.update_status_tele(cardinal, text_color="#2c2825", background_color="green")
            g_ui.update_button_park(is_disabled=False)
            g_ui.update_button_flat(is_disabled=False)

        logger.debug(f"Altaz coords: {response.aa_coords}")
        g_ui.update_tele_text({"alt": response.aa_coords.alt, "az": response.aa_coords.az})
