from datetime import datetime, timezone
from typing import Optional
from ..interfaces.time_provider_interface import ITimeProvider

class TimeProvider(ITimeProvider):
    """時間提供クラス - Single Responsibility Principle"""
    
    def __init__(self, default_timezone: Optional[str] = None):
        self._timezone = default_timezone or "local"
    
    def get_current_time(self) -> datetime:
        """現在時刻を取得"""
        if self._timezone == "local":
            return datetime.now()
        else:
            # Future: timezone support
            return datetime.now()
    
    def set_timezone(self, timezone_name: str) -> None:
        """タイムゾーンを設定"""
        self._timezone = timezone_name
    
    def get_timezone(self) -> str:
        """現在のタイムゾーンを取得"""
        return self._timezone
    
    def format_time(self, time: datetime, format_string: str) -> str:
        """時刻をフォーマット"""
        return time.strftime(format_string)