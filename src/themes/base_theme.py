from abc import ABC
from typing import Dict, Any
from ..interfaces.theme_interface import ITheme

class BaseTheme(ITheme):
    """テーマのベースクラス - Template Method Pattern"""
    
    def __init__(self, name: str):
        self._name = name
        self._colors = self._define_colors()
        self._font_settings = self._define_font_settings()
        self._hand_settings = self._define_hand_settings()
    
    def get_name(self) -> str:
        return self._name
    
    def get_colors(self) -> Dict[str, str]:
        return self._colors.copy()
    
    def get_font_settings(self) -> Dict[str, Any]:
        return self._font_settings.copy()
    
    def get_hand_settings(self) -> Dict[str, Any]:
        return self._hand_settings.copy()
    
    def apply_special_effects(self, canvas, draw_func, *args, **kwargs) -> Any:
        """デフォルトでは特殊効果なし"""
        return draw_func(*args, **kwargs)
    
    def _define_colors(self) -> Dict[str, str]:
        """色設定を定義（サブクラスでオーバーライド）"""
        return {
            'bg': '#ffffff',
            'canvas_bg': '#ffffff',
            'face': '#ffffff',
            'hour_hand': '#000000',
            'minute_hand': '#000000',
            'second_hand': '#ff0000',
            'numbers': '#000000',
            'marks': '#808080',
            'center': '#000000',
            'digital_fg': '#000000',
            'outline': '#000000'
        }
    
    def _define_font_settings(self) -> Dict[str, Any]:
        """フォント設定を定義"""
        return {
            'family': 'Arial',
            'size': 16,
            'weight': 'bold'
        }
    
    def _define_hand_settings(self) -> Dict[str, Any]:
        """針の設定を定義"""
        return {
            'hour_width': 6,
            'minute_width': 4,
            'second_width': 2
        }