from typing import Dict, Any
from .base_theme import BaseTheme

class ModernTheme(BaseTheme):
    """モダンテーマ"""
    
    def __init__(self):
        super().__init__("モダン")
    
    def _define_colors(self) -> Dict[str, str]:
        return {
            'bg': '#2c3e50',
            'canvas_bg': '#34495e',
            'face': '#ecf0f1',
            'hour_hand': '#e74c3c',
            'minute_hand': '#f39c12',
            'second_hand': '#e67e22',
            'numbers': '#2c3e50',
            'marks': '#7f8c8d',
            'center': '#c0392b',
            'digital_fg': '#ecf0f1',
            'outline': '#bdc3c7'
        }

class ClassicTheme(BaseTheme):
    """クラシックテーマ"""
    
    def __init__(self):
        super().__init__("クラシック")
    
    def _define_colors(self) -> Dict[str, str]:
        return {
            'bg': '#f4f1de',
            'canvas_bg': '#f4f1de',
            'face': '#fefefe',
            'hour_hand': '#2d3436',
            'minute_hand': '#2d3436',
            'second_hand': '#d63031',
            'numbers': '#2d3436',
            'marks': '#636e72',
            'center': '#2d3436',
            'digital_fg': '#2d3436',
            'outline': '#ddd'
        }
    
    def _define_hand_settings(self) -> Dict[str, Any]:
        return {
            'hour_width': 8,
            'minute_width': 6,
            'second_width': 2
        }

class DarkTheme(BaseTheme):
    """ダークテーマ"""
    
    def __init__(self):
        super().__init__("ダーク")
    
    def _define_colors(self) -> Dict[str, str]:
        return {
            'bg': '#0d1117',
            'canvas_bg': '#161b22',
            'face': '#21262d',
            'hour_hand': '#58a6ff',
            'minute_hand': '#79c0ff',
            'second_hand': '#f85149',
            'numbers': '#c9d1d9',
            'marks': '#484f58',
            'center': '#f85149',
            'digital_fg': '#c9d1d9',
            'outline': '#30363d'
        }

class LightTheme(BaseTheme):
    """ライトテーマ"""
    
    def __init__(self):
        super().__init__("ライト")
    
    def _define_colors(self) -> Dict[str, str]:
        return {
            'bg': '#ffffff',
            'canvas_bg': '#f8f9fa',
            'face': '#ffffff',
            'hour_hand': '#495057',
            'minute_hand': '#6c757d',
            'second_hand': '#dc3545',
            'numbers': '#212529',
            'marks': '#adb5bd',
            'center': '#dc3545',
            'digital_fg': '#212529',
            'outline': '#dee2e6'
        }

class NeonTheme(BaseTheme):
    """ネオンテーマ（特殊効果付き）"""
    
    def __init__(self):
        super().__init__("ネオン")
    
    def _define_colors(self) -> Dict[str, str]:
        return {
            'bg': '#0a0a0a',
            'canvas_bg': '#1a1a1a',
            'face': '#000000',
            'hour_hand': '#00ff41',
            'minute_hand': '#ff0080',
            'second_hand': '#00d4ff',
            'numbers': '#ffffff',
            'marks': '#666666',
            'center': '#ff0080',
            'digital_fg': '#00ff41',
            'outline': '#333333'
        }
    
    def apply_special_effects(self, canvas, draw_func, *args, **kwargs) -> Any:
        """ネオン発光効果を適用"""
        # 発光効果のために複数回描画
        results = []
        for i in range(3):
            # 針の太さやオフセットを調整して発光効果を作成
            if 'width' in kwargs:
                kwargs['width'] = kwargs.get('width', 2) + i
            result = draw_func(*args, **kwargs)
            results.append(result)
        return results[-1]  # 最終結果を返す

class MinimalTheme(BaseTheme):
    """ミニマルテーマ"""
    
    def __init__(self):
        super().__init__("ミニマル")
    
    def _define_colors(self) -> Dict[str, str]:
        return {
            'bg': '#fafafa',
            'canvas_bg': '#fafafa',
            'face': '#ffffff',
            'hour_hand': '#424242',
            'minute_hand': '#757575',
            'second_hand': '#ff5722',
            'numbers': '#212121',
            'marks': '#bdbdbd',
            'center': '#ff5722',
            'digital_fg': '#212121',
            'outline': '#e0e0e0'
        }
    
    def _define_font_settings(self) -> Dict[str, Any]:
        return {
            'family': 'Arial',
            'size': 18,
            'weight': 'normal'
        }
    
    def _define_hand_settings(self) -> Dict[str, Any]:
        return {
            'hour_width': 4,
            'minute_width': 2,
            'second_width': 1
        }