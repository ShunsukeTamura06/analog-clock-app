from abc import ABC, abstractmethod
from typing import Optional, Any

class IWindowManager(ABC):
    """ウィンドウ管理のインターフェース"""
    
    @abstractmethod
    def show_clock_window(self) -> None:
        """時計ウィンドウを表示"""
        pass
    
    @abstractmethod
    def hide_clock_window(self) -> None:
        """時計ウィンドウを非表示"""
        pass
    
    @abstractmethod
    def show_settings_window(self) -> None:
        """設定ウィンドウを表示"""
        pass
    
    @abstractmethod
    def hide_settings_window(self) -> None:
        """設定ウィンドウを非表示"""
        pass
    
    @abstractmethod
    def get_clock_window(self) -> Optional[Any]:
        """時計ウィンドウを取得"""
        pass
    
    @abstractmethod
    def get_settings_window(self) -> Optional[Any]:
        """設定ウィンドウを取得"""
        pass