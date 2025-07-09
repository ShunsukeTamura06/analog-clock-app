from abc import ABC, abstractmethod
from typing import Dict, Any

class ITheme(ABC):
    """テーマのインターフェース"""
    
    @abstractmethod
    def get_name(self) -> str:
        """テーマ名を取得"""
        pass
    
    @abstractmethod
    def get_colors(self) -> Dict[str, str]:
        """色設定を取得"""
        pass
    
    @abstractmethod
    def get_font_settings(self) -> Dict[str, Any]:
        """フォント設定を取得"""
        pass
    
    @abstractmethod
    def get_hand_settings(self) -> Dict[str, Any]:
        """針の設定を取得"""
        pass
    
    @abstractmethod
    def apply_special_effects(self, canvas, draw_func, *args, **kwargs) -> Any:
        """特殊効果を適用（ネオンテーマの発光効果など）"""
        pass