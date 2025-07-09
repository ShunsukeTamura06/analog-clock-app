import tkinter as tk
from typing import Optional
from ..interfaces.time_provider_interface import ITimeProvider
from ..interfaces.renderer_interface import IRenderer
from .clock_window import ClockWindow
from .time_provider import TimeProvider
from .clock_config import ClockConfig
from .event_manager import EventManager
from ..themes.theme_manager import ThemeManager
from ..rendering.analog_clock_renderer import AnalogClockRenderer

class ClockApplication:
    """メインアプリケーションクラス - Single Responsibility Principle"""
    
    def __init__(self):
        self._root: Optional[tk.Tk] = None
        self._window: Optional[ClockWindow] = None
        self._time_provider: Optional[ITimeProvider] = None
        self._renderer: Optional[IRenderer] = None
        self._config: Optional[ClockConfig] = None
        self._theme_manager: Optional[ThemeManager] = None
        self._event_manager: Optional[EventManager] = None
        self._is_running = False
    
    def initialize(self) -> None:
        """アプリケーションを初期化"""
        # Dependency Injection for easy testing and extensibility
        self._config = ClockConfig()
        self._time_provider = TimeProvider()
        self._theme_manager = ThemeManager()
        
        # Create main window
        self._root = tk.Tk()
        self._window = ClockWindow(self._root, self._config)
        
        # Initialize renderer
        self._renderer = AnalogClockRenderer()
        self._renderer.initialize(self._window.get_canvas(), self._config)
        
        # Setup event management
        self._event_manager = EventManager()
        self._setup_events()
        
        # Set initial theme
        initial_theme = self._theme_manager.get_theme(self._config.get_default_theme())
        self._window.apply_theme(initial_theme)
        
        # Setup theme selector
        self._window.setup_theme_selector(
            self._theme_manager.get_theme_names(),
            self._on_theme_changed
        )
    
    def _setup_events(self) -> None:
        """イベントハンドラーを設定"""
        self._event_manager.subscribe('theme_changed', self._on_theme_changed)
        self._event_manager.subscribe('config_changed', self._on_config_changed)
    
    def _on_theme_changed(self, theme_name: str) -> None:
        """テーマ変更イベントハンドラー"""
        theme = self._theme_manager.get_theme(theme_name)
        self._window.apply_theme(theme)
        self._renderer.clear_all()
        self._renderer.render_clock_face(theme)
        self._config.set_current_theme(theme_name)
    
    def _on_config_changed(self, config: dict) -> None:
        """設定変更イベントハンドラー"""
        # Future: Handle configuration changes
        pass
    
    def _update_clock(self) -> None:
        """時計を更新"""
        if not self._is_running:
            return
            
        current_time = self._time_provider.get_current_time()
        
        # Update digital display
        digital_time = self._time_provider.format_time(
            current_time, 
            "%Y年%m月%d日 %H:%M:%S"
        )
        self._window.update_digital_display(digital_time)
        
        # Update analog display
        hours = current_time.hour % 12
        minutes = current_time.minute
        seconds = current_time.second
        
        current_theme = self._theme_manager.get_theme(self._config.get_current_theme())
        
        self._renderer.clear_hands()
        self._renderer.render_hands(hours, minutes, seconds, current_theme)
        
        # Schedule next update
        if self._root:
            self._root.after(1000, self._update_clock)
    
    def run(self) -> None:
        """アプリケーションを実行"""
        if not self._root or not self._window:
            raise RuntimeError("Application must be initialized before running")
        
        self._is_running = True
        
        # Initial render
        current_theme = self._theme_manager.get_theme(self._config.get_current_theme())
        self._renderer.render_clock_face(current_theme)
        
        # Start clock updates
        self._update_clock()
        
        # Start main loop
        try:
            self._root.mainloop()
        finally:
            self._is_running = False
    
    def shutdown(self) -> None:
        """アプリケーションを終了"""
        self._is_running = False
        if self._root:
            self._root.quit()