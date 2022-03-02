from crac_protobuf.button_pb2 import ButtonLabel
import gettext

it = gettext.translation('base', localedir='../locales', languages=['it'])
it.install()

_ = it.gettext # Italian

def _name(label: ButtonLabel) -> str:
    return _(ButtonLabel.Name(label))