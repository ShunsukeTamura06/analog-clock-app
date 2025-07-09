from typing import Dict, Any, Optional
import json
import os

class ClockConfig:
    """設定管理クラス - Single Responsibility Principle"""
    
    def __init__(self, config_file: Optional[str] = None):
        self._config_file = config_file or "clock_config.json"
        self._config: Dict[str, Any] = self._load_default_config()
        self._load_config()
    
    def _load_default_config(self) -> Dict[str, Any]:
        """デフォルト設定を読み込み"""
        return {
            "default_theme": "モダン",
            "current_theme": "モダン",
            "window_size": {"width": 400, "height": 500},
            "clock_size": {"width": 350, "height": 350},
            "center_position": {"x": 175, "y": 175},
            "radius": 150,
            "timezone": "local",
            "save_settings": True,
            "show_digital_clock": True,
            "enable_sounds": False,
            "enable_animations": True
        }
    
    def _load_config(self) -> None:
        """設定ファイルから設定を読み込み"""
        try:
            if os.path.exists(self._config_file):
                with open(self._config_file, 'r', encoding='utf-8') as f:
                    saved_config = json.load(f)
                    self._config.update(saved_config)
        except Exception:
            # If loading fails, use default config
            pass
    
    def save_config(self) -> None:
        """設定をファイルに保存"""
        if not self._config.get("save_settings", True):
            return
            
        try:
            with open(self._config_file, 'w', encoding='utf-8') as f:
                json.dump(self._config, f, indent=2, ensure_ascii=False)
        except Exception:
            # If saving fails, continue silently
            pass
    
    def get(self, key: str, default: Any = None) -> Any:
        """設定値を取得"""
        return self._config.get(key, default)
    
    def set(self, key: str, value: Any) -> None:
        """設定値を設定"""
        self._config[key] = value
        self.save_config()
    
    def get_default_theme(self) -> str:
        """デフォルトテーマを取得"""
        return self._config.get("default_theme", "モダン")
    
    def get_current_theme(self) -> str:
        """現在のテーマを取得"""
        return self._config.get("current_theme", "モダン")
    
    def set_current_theme(self, theme_name: str) -> None:
        """現在のテーマを設定"""
        self.set("current_theme", theme_name)
    
    def get_window_size(self) -> Dict[str, int]:
        """ウィンドウサイズを取得"""
        return self._config.get("window_size", {"width": 400, "height": 500})
    
    def get_clock_size(self) -> Dict[str, int]:
        """時計サイズを取得"""
        return self._config.get("clock_size", {"width": 350, "height": 350})
    
    def get_center_position(self) -> Dict[str, int]:
        """中心座標を取得"""
        return self._config.get("center_position", {"x": 175, "y": 175})
    
    def get_radius(self) -> int:
        """半径を取得"""
        return self._config.get("radius", 150)