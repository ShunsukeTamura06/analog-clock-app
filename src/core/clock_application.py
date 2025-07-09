import tkinter as tk
from tkinter import messagebox
from typing import Optional
from ..interfaces.time_provider_interface import ITimeProvider
from ..interfaces.renderer_interface import IRenderer
from ..interfaces.window_manager_interface import IWindowManager
from .window_manager import WindowManager
from .time_provider import TimeProvider
from .clock_config import ClockConfig
from .event_manager import EventManager
from ..themes.theme_manager import ThemeManager
from ..rendering.analog_clock_renderer import AnalogClockRenderer

class ClockApplication:
    """メインアプリケーションクラス - Single Responsibility Principle"""
    
    def __init__(self):
        self._window_manager: Optional[IWindowManager] = None
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
        
        # Create window manager
        self._window_manager = WindowManager(self._config)
        
        # Setup event management
        self._event_manager = EventManager()
        self._setup_events()
        
        # Initialize window manager with callbacks
        self._window_manager.initialize(
            self._theme_manager.get_theme_names(),
            self._on_theme_changed,
            self._on_settings_changed,
            self._on_close
        )
        
        # Initialize renderer
        clock_window = self._window_manager.get_clock_window()
        if clock_window:
            self._renderer = AnalogClockRenderer()
            self._renderer.initialize(clock_window.get_canvas(), self._config)
        
        # Set initial theme
        initial_theme = self._theme_manager.get_theme(self._config.get_current_theme())
        if initial_theme:
            self._window_manager.apply_theme(initial_theme)
    
    def _setup_events(self) -> None:
        """イベントハンドラーを設定"""
        self._event_manager.subscribe('theme_changed', self._on_theme_changed)
        self._event_manager.subscribe('settings_changed', self._on_settings_changed)
        self._event_manager.subscribe('close_application', self._on_close)
    
    def _on_theme_changed(self, theme_name: str) -> None:
        """テーマ変更イベントハンドラー"""
        theme = self._theme_manager.get_theme(theme_name)
        if theme and self._window_manager and self._renderer:
            self._window_manager.apply_theme(theme)
            self._renderer.clear_all()
            self._renderer.render_clock_face(theme)
            self._config.set_current_theme(theme_name)
    
    def _on_settings_changed(self, setting_name: str, value) -> None:
        """設定変更イベントハンドラー"""
        if setting_name == "always_on_top":
            self._apply_topmost_setting()
        elif setting_name == "show_digital_clock":
            self._update_digital_display_visibility()
        elif setting_name == "size_changed":
            self._handle_size_change()
        elif setting_name == "reset":
            self._handle_reset()
    
    def _apply_topmost_setting(self) -> None:
        """常に最前面表示設定を適用"""
        if self._window_manager:
            clock_root = self._window_manager.get_clock_root()
            if clock_root:
                is_topmost = self._config.get("always_on_top", False)
                clock_root.attributes("-topmost", is_topmost)
    
    def _update_digital_display_visibility(self) -> None:
        """デジタル表示の表示/非表示を更新"""
        if self._window_manager:
            clock_window = self._window_manager.get_clock_window()
            if clock_window:
                clock_window.update_size()  # サイズ更新で表示も更新される
    
    def _handle_size_change(self) -> None:
        """サイズ変更を処理"""
        if self._window_manager and self._renderer:
            # ウィンドウサイズを更新
            self._window_manager.update_clock_size()
            
            # レンダラーを再初期化
            clock_window = self._window_manager.get_clock_window()
            if clock_window:
                self._renderer.initialize(clock_window.get_canvas(), self._config)
                
                # 時計を再描画
                current_theme = self._theme_manager.get_theme(self._config.get_current_theme())
                if current_theme:
                    self._renderer.clear_all()
                    self._renderer.render_clock_face(current_theme)
    
    def _handle_reset(self) -> None:
        """リセットを処理"""
        # サイズ変更とテーマ変更を適用
        self._handle_size_change()
        self._apply_topmost_setting()
        self._update_digital_display_visibility()
    
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
        if self._window_manager:
            self._window_manager.update_digital_display(digital_time)
        
        # Update analog display
        hours = current_time.hour % 12
        minutes = current_time.minute
        seconds = current_time.second
        
        current_theme = self._theme_manager.get_theme(self._config.get_current_theme())
        
        if self._renderer and current_theme:
            self._renderer.clear_hands()
            self._renderer.render_hands(hours, minutes, seconds, current_theme)
        
        # Schedule next update
        if self._window_manager:
            clock_root = self._window_manager.get_clock_root()
            if clock_root:
                clock_root.after(1000, self._update_clock)
    
    def run(self) -> None:
        """アプリケーションを実行"""
        if not self._window_manager:
            raise RuntimeError("Application must be initialized before running")
        
        self._is_running = True
        
        # Show clock window
        self._window_manager.show_clock_window()
        
        # Initial render
        current_theme = self._theme_manager.get_theme(self._config.get_current_theme())
        if self._renderer and current_theme:
            self._renderer.render_clock_face(current_theme)
        
        # Apply initial settings
        self._apply_topmost_setting()
        
        # Start clock updates
        self._update_clock()
        
        # Start main loop
        try:
            clock_root = self._window_manager.get_clock_root()
            if clock_root:
                clock_root.mainloop()
        finally:
            self._is_running = False
    
    def _on_close(self) -> None:
        """アプリケーション終了イベント"""
        self.shutdown()
    
    def shutdown(self) -> None:
        """アプリケーションを終了"""
        self._is_running = False
        if self._window_manager:
            clock_root = self._window_manager.get_clock_root()
            if clock_root:
                clock_root.quit()
                clock_root.destroy()