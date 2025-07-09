from abc import ABC, abstractmethod
from typing import Any

class IRenderer(ABC):
    """レンダラーのインターフェース"""
    
    @abstractmethod
    def initialize(self, canvas: Any, config: Any) -> None:
        """レンダラーを初期化"""
        pass
    
    @abstractmethod
    def render_clock_face(self, theme: Any) -> None:
        """時計の文字盤を描画"""
        pass
    
    @abstractmethod
    def render_hands(self, hours: int, minutes: int, seconds: int, theme: Any) -> None:
        """時計の針を描画"""
        pass
    
    @abstractmethod
    def clear_hands(self) -> None:
        """針をクリア"""
        pass
    
    @abstractmethod
    def clear_all(self) -> None:
        """すべてをクリア"""
        pass