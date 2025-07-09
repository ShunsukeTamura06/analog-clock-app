from typing import Dict, List, Optional
from ..interfaces.theme_interface import ITheme
from .concrete_themes import (
    ModernTheme,
    ClassicTheme,
    DarkTheme,
    LightTheme,
    NeonTheme,
    MinimalTheme
)

class ThemeManager:
    """テーマ管理クラス - Open/Closed Principle"""
    
    def __init__(self):
        self._themes: Dict[str, ITheme] = {}
        self._register_default_themes()
    
    def _register_default_themes(self) -> None:
        """デフォルトテーマを登録"""
        default_themes = [
            ModernTheme(),
            ClassicTheme(),
            DarkTheme(),
            LightTheme(),
            NeonTheme(),
            MinimalTheme()
        ]
        
        for theme in default_themes:
            self.register_theme(theme)
    
    def register_theme(self, theme: ITheme) -> None:
        """テーマを登録 - Open/Closed Principle"""
        self._themes[theme.get_name()] = theme
    
    def unregister_theme(self, theme_name: str) -> None:
        """テーマを削除"""
        self._themes.pop(theme_name, None)
    
    def get_theme(self, theme_name: str) -> Optional[ITheme]:
        """テーマを取得"""
        return self._themes.get(theme_name)
    
    def get_theme_names(self) -> List[str]:
        """テーマ名一覧を取得"""
        return list(self._themes.keys())
    
    def get_all_themes(self) -> Dict[str, ITheme]:
        """すべてのテーマを取得"""
        return self._themes.copy()