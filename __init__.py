
from .nodes.int_bool_switch import *
from .nodes.horizontal_blur_mask import *
from .nodes.mask_transform import *


# ノードマッピング
NODE_CLASS_MAPPINGS = {
    "HorizontalBlurMask": HorizontalBlurMask,
    "IntBoolSwitch": IntBoolSwitch,
    "MaskTransform": MaskTransform
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "HorizontalBlurMask": "Horizontal Blur Mask",
    "IntBoolSwitch" : "Int Bool Switch",
    "MaskTransform": "Mask Transform (XY Offset)"
}


__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS']