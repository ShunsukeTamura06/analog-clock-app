from typing import Dict, List, Callable, Any

class EventManager:
    """イベント管理クラス - Observer Pattern"""
    
    def __init__(self):
        self._subscribers: Dict[str, List[Callable]] = {}
    
    def subscribe(self, event_type: str, callback: Callable) -> None:
        """イベントにコールバックを登録"""
        if event_type not in self._subscribers:
            self._subscribers[event_type] = []
        self._subscribers[event_type].append(callback)
    
    def unsubscribe(self, event_type: str, callback: Callable) -> None:
        """イベントからコールバックを削除"""
        if event_type in self._subscribers:
            try:
                self._subscribers[event_type].remove(callback)
            except ValueError:
                pass
    
    def publish(self, event_type: str, *args, **kwargs) -> None:
        """イベントを発行"""
        if event_type in self._subscribers:
            for callback in self._subscribers[event_type]:
                try:
                    callback(*args, **kwargs)
                except Exception:
                    # Continue with other callbacks even if one fails
                    pass
    
    def clear_subscribers(self, event_type: str = None) -> None:
        """購読者をクリア"""
        if event_type:
            self._subscribers.pop(event_type, None)
        else:
            self._subscribers.clear()