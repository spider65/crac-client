from crac_client.converter.converter import Converter
from crac_client.gui import Gui
from crac_client.loc import _name
from crac_protobuf.roof_pb2 import (
    RoofStatus,
    RoofResponse,
    RoofAction,
)


class RoofConverter(Converter):
    def convert(self, response: RoofResponse, g_ui: Gui):
        if response.status is RoofStatus.ROOF_CLOSED:
            g_ui.hide_background_image()
        elif response.status is RoofStatus.ROOF_OPENED:
            g_ui.show_background_image()
        elif response.status is RoofStatus.ROOF_CLOSING:
            g_ui.show_background_image()
        elif response.status is RoofStatus.ROOF_OPENING:
            g_ui.show_background_image()

        g_ui.win[response.button_gui.key](
            _name(response.button_gui.label),
            disabled=response.button_gui.is_disabled,
            button_color=(
                response.button_gui.button_color.text_color, 
                response.button_gui.button_color.background_color
            )
        )
        g_ui.win[response.button_gui.key].metadata = RoofAction.Name(response.button_gui.metadata)
