import logging
from crac_client.gui import Gui
from crac_client.gui_constants import GuiLabel
from crac_protobuf.curtains_pb2 import (
    CurtainStatus,
    CurtainOrientation,
    CurtainsResponse
)


logger = logging.getLogger('crac_client.app')


class CurtainsConverter:
    def convert(self, response: CurtainsResponse, g_ui: Gui):
        curtains_disabled = 0
        east_steps = 0
        west_steps = 0
        for curtain in response.curtains:
            orientation = CurtainOrientation.Name(curtain.orientation).lower()
            if curtain.orientation is CurtainOrientation.CURTAIN_EAST:
                east_steps = curtain.steps
            else:
                west_steps = curtain.steps

            if curtain.status in [CurtainStatus.CURTAIN_ERROR, CurtainStatus.CURTAIN_DANGER]:
                g_ui.status_alert(GuiLabel.ALERT_CHECK_CURTAINS_SWITCH.value)
                # g_ui.update_disable_button_close_roof()
                logger.debug("disabled close roof button")
            elif curtain.status is CurtainStatus.CURTAIN_DISABLED:
                g_ui.status_alert(GuiLabel.NO_ALERT.value)
                curtains_disabled += 1
            else:
                g_ui.status_alert(GuiLabel.NO_ALERT.value)
                # g_ui.update_disable_button_close_roof()
                logger.debug("disabled close roof button")

            g_ui.update_status_curtain(orientation, GuiLabel[CurtainStatus.Name(curtain.status)].value)

        # if curtains_disabled == 2:
            # g_ui.update_disable_button_disabled_curtains()
            # g_ui.update_enable_button_close_roof()

        logger.debug(f"East steps: {east_steps}")
        logger.debug(f"West steps: {west_steps}")
        if g_ui.is_curtains_position_changed(east_steps, west_steps):
            alpha_e, alpha_w = g_ui.convert_steps_to_angular_values(east_steps, west_steps)
            g_ui.update_curtains_text(alpha_e, alpha_w)
            g_ui.update_curtains_graphic(alpha_e, alpha_w)
