
from .nodes.int_bool_switch import *
from .nodes.horizontal_blur_mask import *


# ノードマッピング
NODE_CLASS_MAPPINGS = {
    "HorizontalBlurMask": HorizontalBlurMask,
    "IntBoolSwitch": IntBoolSwitch
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "HorizontalBlurMask": "Horizontal Blur Mask",
    "IntBoolSwitch" : "Int Bool Switch"
}


__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS']