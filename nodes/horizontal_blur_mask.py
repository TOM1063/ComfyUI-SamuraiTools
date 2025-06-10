import torch
import torch.nn.functional as F

class HorizontalBlurMask:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "mask": ("MASK",),
                "blur_strength": ("FLOAT", {
                    "default": 5.0,
                    "min": 0.0,
                    "max": 100.0,
                    "step": 0.1,
                    "display": "slider"
                }),
            }
        }
    
    RETURN_TYPES = ("MASK",)
    FUNCTION = "horizontal_blur"
    CATEGORY = "mask"

    def horizontal_blur(self, mask, blur_strength):
        # マスクの形状を取得
        if len(mask.shape) == 2:
            # 2次元の場合は3次元に拡張
            mask = mask.unsqueeze(0)
        
        # バッチ次元を考慮
        batch_size, height, width = mask.shape
        
        # ガウシアンカーネルのサイズを計算（奇数にする）
        kernel_size = int(blur_strength * 2) + 1
        if kernel_size < 3:
            return (mask,)
        
        # 横方向のみのガウシアンカーネルを作成
        sigma = blur_strength / 3.0
        x = torch.arange(kernel_size, dtype=torch.float32) - kernel_size // 2
        gaussian_1d = torch.exp(-(x ** 2) / (2 * sigma ** 2))
        gaussian_1d = gaussian_1d / gaussian_1d.sum()
        
        # カーネルを横方向（1 x kernel_size）に reshape
        kernel = gaussian_1d.view(1, 1, 1, kernel_size)
        
        # マスクを4次元に変換 (batch, channel, height, width)
        mask_4d = mask.unsqueeze(1)
        
        # パディングを追加（横方向のみ）
        padding = (kernel_size // 2, kernel_size // 2, 0, 0)
        mask_padded = F.pad(mask_4d, padding, mode='reflect')
        
        # 畳み込み演算で横方向のブラーを適用
        blurred = F.conv2d(mask_padded, kernel, padding=0)
        
        # 元の形状に戻す
        result = blurred.squeeze(1)
        
        return (result,)