import tkinter as tk
from tkinter import ttk
from typing import List, Callable, Optional, Any
from ..interfaces.theme_interface import ITheme
from .clock_config import ClockConfig

class ClockWindow:
    """ウィンドウ管理専用クラス - Single Responsibility Principle"""
    
    def __init__(self, root: tk.Tk, config: ClockConfig):
        self._root = root
        self._config = config
        self._canvas: Optional[tk.Canvas] = None
        self._digital_label: Optional[tk.Label] = None
        self._theme_combo: Optional[ttk.Combobox] = None
        self._setup_window()
        self._create_widgets()
    
    def _setup_window(self) -> None:
        """ウィンドウの基本設定"""
        self._root.title("アナログ時計")
        self._root.geometry("400x500")
        self._root.resizable(False, False)
        self._center_window()
        
        # アイコン設定（オプション）
        try:
            self._root.iconbitmap('clock.ico')
        except:
            pass
    
    def _center_window(self) -> None:
        """ウィンドウを画面中央に配置"""
        self._root.update_idletasks()
        x = (self._root.winfo_screenwidth() // 2) - (400 // 2)
        y = (self._root.winfo_screenheight() // 2) - (500 // 2)
        self._root.geometry(f'400x500+{x}+{y}')
    
    def _create_widgets(self) -> None:
        """ウィジェットを作成"""
        # テーマ選択フレーム
        self._theme_frame = tk.Frame(self._root)
        self._theme_frame.pack(pady=5)
        
        tk.Label(self._theme_frame, text="テーマ:", font=('Arial', 10)).pack(side=tk.LEFT, padx=5)
        
        # デジタル時計フレーム
        self._digital_frame = tk.Frame(self._root)
        self._digital_frame.pack(pady=5)
        
        self._digital_label = tk.Label(
            self._digital_frame,
            font=('Arial', 14, 'bold')
        )
        self._digital_label.pack()
        
        # キャンバス
        self._canvas = tk.Canvas(
            self._root,
            width=350,
            height=350,
            highlightthickness=0
        )
        self._canvas.pack(pady=10)
    
    def setup_theme_selector(self, theme_names: List[str], on_change_callback: Callable[[str], None]) -> None:
        """テーマセレクターを設定"""
        self._theme_var = tk.StringVar(value=theme_names[0] if theme_names else "")
        self._theme_combo = ttk.Combobox(
            self._theme_frame,
            textvariable=self._theme_var,
            values=theme_names,
            state="readonly",
            width=12
        )
        self._theme_combo.pack(side=tk.LEFT, padx=5)
        self._theme_combo.bind('<<ComboboxSelected>>', 
                              lambda e: on_change_callback(self._theme_var.get()))
    
    def apply_theme(self, theme: ITheme) -> None:
        """テーマを適用"""
        colors = theme.get_colors()
        
        self._root.configure(bg=colors['bg'])
        self._theme_frame.configure(bg=colors['bg'])
        self._digital_frame.configure(bg=colors['bg'])
        
        if self._digital_label:
            self._digital_label.configure(bg=colors['bg'], fg=colors['digital_fg'])
        
        if self._canvas:
            self._canvas.configure(bg=colors['canvas_bg'])
    
    def update_digital_display(self, time_text: str) -> None:
        """デジタル表示を更新"""
        if self._digital_label:
            self._digital_label.config(text=time_text)
    
    def get_canvas(self) -> tk.Canvas:
        """キャンバスを取得"""
        if not self._canvas:
            raise RuntimeError("Canvas not initialized")
        return self._canvas
    
    def get_root(self) -> tk.Tk:
        """ルートウィンドウを取得"""
        return self._root