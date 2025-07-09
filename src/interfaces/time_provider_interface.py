from abc import ABC, abstractmethod
from datetime import datetime
from typing import Optional

class ITimeProvider(ABC):
    """時間提供のインターフェース"""
    
    @abstractmethod
    def get_current_time(self) -> datetime:
        """現在時刻を取得"""
        pass
    
    @abstractmethod
    def set_timezone(self, timezone: str) -> None:
        """タイムゾーンを設定"""
        pass
    
    @abstractmethod
    def get_timezone(self) -> str:
        """現在のタイムゾーンを取得"""
        pass
    
    @abstractmethod
    def format_time(self, time: datetime, format_string: str) -> str:
        """時刻をフォーマット"""
        pass