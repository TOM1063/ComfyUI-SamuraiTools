
# nodes/int_bool_switch.py
class IntBoolSwitch:
    """
    bool値に基づいてint値を切り替えるノード
    """
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "condition": ("BOOLEAN", {"default": True}),
                "int_true": ("INT", {"default": 1, "min": -999999, "max": 999999, "step": 1}),
                "int_false": ("INT", {"default": 0, "min": -999999, "max": 999999, "step": 1}),
            }
        }
    
    RETURN_TYPES = ("INT",)
    RETURN_NAMES = ("int",)
    FUNCTION = "switch_int"
    CATEGORY = "conditioning/switch"

    def switch_int(self, condition, int_true, int_false):
        """
        conditionがTrueの場合はint_trueを、Falseの場合はint_falseを返す
        """
        if condition:
            return (int_true,)
        else:
            return (int_false,)

# ComfyUIへの登録用辞書
NODE_CLASS_MAPPINGS = {
    "IntBoolSwitch": IntBoolSwitch
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "IntBoolSwitch": "Int Bool Switch"
}