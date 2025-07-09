import tkinter as tk
from typing import Optional, Callable
from ..interfaces.window_manager_interface import IWindowManager
from .clock_window import ClockWindow
from .settings_window import SettingsWindow
from .clock_config import ClockConfig
from ..interfaces.theme_interface import ITheme

class WindowManager(IWindowManager):
    """ウィンドウ管理クラス - Single Responsibility Principle"""
    
    def __init__(self, config: ClockConfig):
        self._config = config
        self._clock_window: Optional[ClockWindow] = None
        self._settings_window: Optional[SettingsWindow] = None
        self._clock_root: Optional[tk.Tk] = None
        self._settings_root: Optional[tk.Toplevel] = None
        
        # Callbacks
        self._on_theme_changed: Optional[Callable] = None
        self._on_settings_changed: Optional[Callable] = None
        self._on_close_callback: Optional[Callable] = None
    
    def initialize(self, theme_names: list, on_theme_changed: Callable, 
                  on_settings_changed: Callable, on_close: Callable) -> None:
        """ウィンドウマネージャーを初期化"""
        self._on_theme_changed = on_theme_changed
        self._on_settings_changed = on_settings_changed
        self._on_close_callback = on_close
        
        # 時計ウィンドウを作成
        self._create_clock_window()
        
        # 設定ウィンドウのコールバックを設定
        self._theme_names = theme_names
    
    def _create_clock_window(self) -> None:
        """時計ウィンドウを作成"""
        self._clock_root = tk.Tk()
        self._clock_window = ClockWindow(self._clock_root, self._config)
        
        # 右クリックメニューを設定
        self._setup_context_menu()
        
        # 閉じるボタンのイベントを設定
        self._clock_root.protocol("WM_DELETE_WINDOW", self._on_close_callback)
    
    def _setup_context_menu(self) -> None:
        """右クリックメニューを設定"""
        context_menu = tk.Menu(self._clock_root, tearoff=0)
        context_menu.add_command(label="設定", command=self.show_settings_window)
        context_menu.add_separator()
        context_menu.add_command(label="終了", command=self._on_close_callback)
        
        def show_context_menu(event):
            try:
                context_menu.tk_popup(event.x_root, event.y_root)
            finally:
                context_menu.grab_release()
        
        # 時計ウィンドウとキャンバスに右クリックイベントをバインド
        self._clock_root.bind("<Button-3>", show_context_menu)
        canvas = self._clock_window.get_canvas()
        canvas.bind("<Button-3>", show_context_menu)
    
    def show_clock_window(self) -> None:
        """時計ウィンドウを表示"""
        if self._clock_root:
            self._clock_root.deiconify()
            self._apply_window_settings()
    
    def hide_clock_window(self) -> None:
        """時計ウィンドウを非表示"""
        if self._clock_root:
            self._clock_root.withdraw()
    
    def show_settings_window(self) -> None:
        """設定ウィンドウを表示"""
        if self._settings_window is None:
            self._create_settings_window()
        
        if self._settings_root:
            self._settings_root.deiconify()
            self._settings_root.lift()
    
    def hide_settings_window(self) -> None:
        """設定ウィンドウを非表示"""
        if self._settings_root:
            self._settings_root.withdraw()
    
    def _create_settings_window(self) -> None:
        """設定ウィンドウを作成"""
        if self._clock_root is None:
            return
            
        self._settings_root = tk.Toplevel(self._clock_root)
        self._settings_window = SettingsWindow(
            self._settings_root,
            self._config,
            self._theme_names,
            self._on_theme_changed,
            self._on_settings_changed
        )
        
        # 設定ウィンドウを閉じたときは非表示にする
        self._settings_root.protocol("WM_DELETE_WINDOW", self.hide_settings_window)
    
    def _apply_window_settings(self) -> None:
        """ウィンドウ設定を適用"""
        if not self._clock_root:
            return
        
        # 常に最前面表示
        if self._config.get("always_on_top", False):
            self._clock_root.attributes("-topmost", True)
        else:
            self._clock_root.attributes("-topmost", False)
    
    def apply_theme(self, theme: ITheme) -> None:
        """テーマを適用"""
        if self._clock_window:
            self._clock_window.apply_theme(theme)
    
    def update_digital_display(self, time_text: str) -> None:
        """デジタル表示を更新"""
        if self._clock_window:
            self._clock_window.update_digital_display(time_text)
    
    def get_clock_window(self) -> Optional[ClockWindow]:
        """時計ウィンドウを取得"""
        return self._clock_window
    
    def get_settings_window(self) -> Optional[SettingsWindow]:
        """設定ウィンドウを取得"""
        return self._settings_window
    
    def get_clock_root(self) -> Optional[tk.Tk]:
        """時計ルートウィンドウを取得"""
        return self._clock_root
    
    def update_clock_size(self) -> None:
        """時計サイズを更新"""
        if self._clock_window:
            self._clock_window.update_size()
            self._apply_window_settings()