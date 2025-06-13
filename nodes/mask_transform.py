import torch
import torch.nn.functional as F

class MaskTransform:
    def __init__(self):
        pass
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "mask": ("MASK",),
                "x_offset": ("FLOAT", {
                    "default": 0.0,
                    "min": -2.0,
                    "max": 2.0,
                    "step": 0.01,
                    "display": "number"
                }),
                "y_offset": ("FLOAT", {
                    "default": 0.0,
                    "min": -2.0,
                    "max": 2.0,
                    "step": 0.01,
                    "display": "number"
                }),
                "interpolation": (["bilinear", "nearest", "bicubic"], {
                    "default": "bilinear"
                }),
                "boundary_mode": (["zeros", "border", "reflection"], {
                    "default": "zeros"
                }),
            }
        }
    
    RETURN_TYPES = ("MASK",)
    FUNCTION = "transform_mask"
    CATEGORY = "mask/transform"
    
    def transform_mask(self, mask, x_offset, y_offset, interpolation, boundary_mode):
        # マスクの形状を取得
        if len(mask.shape) == 2:
            mask = mask.unsqueeze(0)  # バッチ次元を追加
        
        batch_size, height, width = mask.shape
        
        # オフセットをピクセル単位に変換（fractionからピクセルへ）
        x_pixels = x_offset * width
        y_pixels = y_offset * height
        
        # アフィン変換行列を作成（移動のみ）
        # PyTorchのaffine_gridは正規化座標系を使用するため、オフセットを正規化
        theta = torch.zeros(batch_size, 2, 3, dtype=mask.dtype, device=mask.device)
        theta[:, 0, 0] = 1.0  # x軸のスケール
        theta[:, 1, 1] = 1.0  # y軸のスケール
        theta[:, 0, 2] = -2.0 * x_offset  # x方向の移動（正規化座標系）
        theta[:, 1, 2] = -2.0 * y_offset  # y方向の移動（正規化座標系）
        
        # グリッドを生成
        grid = F.affine_grid(theta, [batch_size, 1, height, width], align_corners=False)
        
        # マスクを4Dテンソルに変換（バッチ、チャンネル、高さ、幅）
        mask_4d = mask.unsqueeze(1)
        
        # 境界モードを設定
        padding_mode = {
            "zeros": "zeros",
            "border": "border", 
            "reflection": "reflection"
        }[boundary_mode]
        
        # 補間モードを設定
        mode = interpolation
        
        # グリッドサンプリングを実行
        transformed_mask = F.grid_sample(
            mask_4d, 
            grid, 
            mode=mode, 
            padding_mode=padding_mode,
            align_corners=False
        )
        
        # 元の形状に戻す
        result = transformed_mask.squeeze(1)
        
        return (result,)

# ノード登録用の辞書
NODE_CLASS_MAPPINGS = {
    "MaskTransform": MaskTransform
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "MaskTransform": "Mask Transform (XY Offset)"
}