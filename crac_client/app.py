from crac_protobuf.roof_pb2 import (
    RoofAction,
    RoofStatus,
    RoofRequest,
)
from crac_protobuf.roof_pb2_grpc import (
    RoofStub,
)
import grpc

from crac_client import config, gui
from crac_client.gui_constants import GuiKey, GuiLabel

channel = grpc.insecure_channel("localhost:50051")
client = RoofStub(channel)
# request = RoofRequest(action=RoofAction.OPEN)
# client.SetAction(request)

g_ui = gui.Gui()
while True:
    timeout = config.Config.getInt("sleep", "automazione")
    v, _ = g_ui.win.Read(timeout=timeout)

    if v is None or v is GuiKey.EXIT or v is GuiKey.SHUTDOWN:
        break
    elif v is GuiKey.CLOSE_ROOF:
        request = RoofRequest(action=RoofAction.CLOSE)
        response = client.SetAction(request)
        if response.status == RoofStatus.ROOF_CLOSED:
            g_ui.hide_background_image()
            g_ui.update_status_roof(GuiLabel.ROOF_CLOSED)
            g_ui.update_enable_button_open_roof()
    elif v is GuiKey.OPEN_ROOF:
        request = RoofRequest(action=RoofAction.OPEN)
        response = client.SetAction(request)
        if response.status == RoofStatus.ROOF_OPENED:
            g_ui.show_background_image()
            g_ui.update_status_roof(GuiLabel.ROOF_OPEN, text_color="#2c2825", background_color="green")
            g_ui.update_enable_disable_button()
