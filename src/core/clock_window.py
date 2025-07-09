import tkinter as tk
from typing import Optional
from ..interfaces.theme_interface import ITheme
from .clock_config import ClockConfig

class ClockWindow:
    """時計表示専用ウィンドウクラス - Single Responsibility Principle"""
    
    def __init__(self, root: tk.Tk, config: ClockConfig):
        self._root = root
        self._config = config
        self._canvas: Optional[tk.Canvas] = None
        self._digital_label: Optional[tk.Label] = None
        self._digital_frame: Optional[tk.Frame] = None
        
        self._setup_window()
        self._create_widgets()
    
    def _setup_window(self) -> None:
        """ウィンドウの基本設定"""
        self._root.title("アナログ時計")
        self._update_window_size()
        self._root.resizable(False, False)
        
        # ウィンドウを中央に配置
        self._center_window()
        
        # アイコン設定
        try:
            self._root.iconbitmap('clock.ico')
        except:
            pass
    
    def _update_window_size(self) -> None:
        """ウィンドウサイズを更新"""
        window_size = self._config.get_window_size()
        self._root.geometry(f"{window_size['width']}x{window_size['height']}")
    
    def _center_window(self) -> None:
        """ウィンドウを画面中央に配置"""
        self._root.update_idletasks()
        window_size = self._config.get_window_size()
        x = (self._root.winfo_screenwidth() // 2) - (window_size['width'] // 2)
        y = (self._root.winfo_screenheight() // 2) - (window_size['height'] // 2)
        self._root.geometry(f"{window_size['width']}x{window_size['height']}+{x}+{y}")
    
    def _create_widgets(self) -> None:
        """ウィジェットを作成"""
        # デジタル時計フレーム
        self._digital_frame = tk.Frame(self._root)
        
        # 設定に応じて表示/非表示
        if self._config.get("show_digital_clock", True):
            self._digital_frame.pack(pady=5)
        
        self._digital_label = tk.Label(
            self._digital_frame,
            font=('Arial', 14, 'bold')
        )
        self._digital_label.pack()
        
        # キャンバス
        clock_size = self._config.get_clock_size()
        self._canvas = tk.Canvas(
            self._root,
            width=clock_size['width'],
            height=clock_size['height'],
            highlightthickness=0
        )
        self._canvas.pack(pady=10)
    
    def apply_theme(self, theme: ITheme) -> None:
        """テーマを適用"""
        colors = theme.get_colors()
        
        self._root.configure(bg=colors['bg'])
        
        if self._digital_frame:
            self._digital_frame.configure(bg=colors['bg'])
        
        if self._digital_label:
            self._digital_label.configure(bg=colors['bg'], fg=colors['digital_fg'])
        
        if self._canvas:
            self._canvas.configure(bg=colors['canvas_bg'])
    
    def update_digital_display(self, time_text: str) -> None:
        """デジタル表示を更新"""
        if self._digital_label and self._config.get("show_digital_clock", True):
            self._digital_label.config(text=time_text)
    
    def update_size(self) -> None:
        """サイズを更新"""
        # ウィンドウサイズを更新
        self._update_window_size()
        self._center_window()
        
        # キャンバスサイズを更新
        if self._canvas:
            clock_size = self._config.get_clock_size()
            self._canvas.config(
                width=clock_size['width'],
                height=clock_size['height']
            )
        
        # デジタル表示の表示/非表示を更新
        if self._config.get("show_digital_clock", True):
            if self._digital_frame:
                self._digital_frame.pack(pady=5)
        else:
            if self._digital_frame:
                self._digital_frame.pack_forget()
    
    def get_canvas(self) -> tk.Canvas:
        """キャンバスを取得"""
        if not self._canvas:
            raise RuntimeError("Canvas not initialized")
        return self._canvas
    
    def get_root(self) -> tk.Tk:
        """ルートウィンドウを取得"""
        return self._root