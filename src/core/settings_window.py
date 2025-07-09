import tkinter as tk
from tkinter import ttk
from typing import List, Callable
from .clock_config import ClockConfig

class SettingsWindow:
    """設定ウィンドウクラス - Single Responsibility Principle"""
    
    def __init__(self, root: tk.Toplevel, config: ClockConfig, theme_names: List[str],
                 on_theme_changed: Callable, on_settings_changed: Callable):
        self._root = root
        self._config = config
        self._theme_names = theme_names
        self._on_theme_changed = on_theme_changed
        self._on_settings_changed = on_settings_changed
        
        self._setup_window()
        self._create_widgets()
    
    def _setup_window(self) -> None:
        """ウィンドウの基本設定"""
        self._root.title("時計設定")
        self._root.geometry("350x400")
        self._root.resizable(False, False)
        
        # ウィンドウを中央に配置
        self._center_window()
        
        # アイコン設定
        try:
            self._root.iconbitmap('settings.ico')
        except:
            pass
    
    def _center_window(self) -> None:
        """ウィンドウを画面中央に配置"""
        self._root.update_idletasks()
        x = (self._root.winfo_screenwidth() // 2) - (350 // 2)
        y = (self._root.winfo_screenheight() // 2) - (400 // 2)
        self._root.geometry(f'350x400+{x}+{y}')
    
    def _create_widgets(self) -> None:
        """ウィジェットを作成"""
        # メインフレーム
        main_frame = tk.Frame(self._root, padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # タイトル
        title_label = tk.Label(main_frame, text="時計設定", font=("Arial", 16, "bold"))
        title_label.pack(pady=(0, 20))
        
        # テーマ設定
        self._create_theme_settings(main_frame)
        
        # 表示設定
        self._create_display_settings(main_frame)
        
        # サイズ設定
        self._create_size_settings(main_frame)
        
        # ボタン
        self._create_buttons(main_frame)
    
    def _create_theme_settings(self, parent: tk.Widget) -> None:
        """テーマ設定を作成"""
        theme_frame = tk.LabelFrame(parent, text="テーマ", padx=10, pady=10)
        theme_frame.pack(fill=tk.X, pady=(0, 15))
        
        tk.Label(theme_frame, text="テーマを選択:").pack(anchor=tk.W)
        
        self._theme_var = tk.StringVar(value=self._config.get_current_theme())
        self._theme_combo = ttk.Combobox(
            theme_frame,
            textvariable=self._theme_var,
            values=self._theme_names,
            state="readonly",
            width=25
        )
        self._theme_combo.pack(fill=tk.X, pady=(5, 0))
        self._theme_combo.bind('<<ComboboxSelected>>', self._on_theme_change)
    
    def _create_display_settings(self, parent: tk.Widget) -> None:
        """表示設定を作成"""
        display_frame = tk.LabelFrame(parent, text="表示設定", padx=10, pady=10)
        display_frame.pack(fill=tk.X, pady=(0, 15))
        
        # 常に最前面表示
        self._topmost_var = tk.BooleanVar(value=self._config.get("always_on_top", False))
        topmost_check = tk.Checkbutton(
            display_frame,
            text="常に最前面に表示",
            variable=self._topmost_var,
            command=self._on_topmost_change
        )
        topmost_check.pack(anchor=tk.W)
        
        # デジタル時計表示
        self._digital_var = tk.BooleanVar(value=self._config.get("show_digital_clock", True))
        digital_check = tk.Checkbutton(
            display_frame,
            text="デジタル時計を表示",
            variable=self._digital_var,
            command=self._on_digital_change
        )
        digital_check.pack(anchor=tk.W)
    
    def _create_size_settings(self, parent: tk.Widget) -> None:
        """サイズ設定を作成"""
        size_frame = tk.LabelFrame(parent, text="サイズ設定", padx=10, pady=10)
        size_frame.pack(fill=tk.X, pady=(0, 15))
        
        # サイズプリセット
        tk.Label(size_frame, text="サイズプリセット:").pack(anchor=tk.W)
        
        size_frame_inner = tk.Frame(size_frame)
        size_frame_inner.pack(fill=tk.X, pady=(5, 10))
        
        sizes = [
            ("小", 250),
            ("中", 350),
            ("大", 450),
            ("特大", 550)
        ]
        
        current_size = self._config.get_clock_size()["width"]
        self._size_var = tk.IntVar(value=current_size)
        
        for i, (text, size) in enumerate(sizes):
            rb = tk.Radiobutton(
                size_frame_inner,
                text=f"{text} ({size}px)",
                variable=self._size_var,
                value=size,
                command=self._on_size_change
            )
            rb.grid(row=i//2, column=i%2, sticky=tk.W, padx=(0, 20))
        
        # カスタムサイズ
        custom_frame = tk.Frame(size_frame)
        custom_frame.pack(fill=tk.X, pady=(10, 0))
        
        tk.Label(custom_frame, text="カスタムサイズ:").pack(side=tk.LEFT)
        
        self._custom_size_var = tk.StringVar(value=str(current_size))
        custom_entry = tk.Entry(custom_frame, textvariable=self._custom_size_var, width=8)
        custom_entry.pack(side=tk.LEFT, padx=(5, 5))
        
        tk.Label(custom_frame, text="px").pack(side=tk.LEFT)
        
        apply_size_btn = tk.Button(
            custom_frame,
            text="適用",
            command=self._on_custom_size_apply
        )
        apply_size_btn.pack(side=tk.RIGHT)
    
    def _create_buttons(self, parent: tk.Widget) -> None:
        """ボタンを作成"""
        button_frame = tk.Frame(parent)
        button_frame.pack(fill=tk.X, pady=(20, 0))
        
        # リセットボタン
        reset_btn = tk.Button(
            button_frame,
            text="リセット",
            command=self._on_reset
        )
        reset_btn.pack(side=tk.LEFT)
        
        # 閉じるボタン
        close_btn = tk.Button(
            button_frame,
            text="閉じる",
            command=self._root.withdraw
        )
        close_btn.pack(side=tk.RIGHT)
    
    def _on_theme_change(self, event=None) -> None:
        """テーマ変更イベント"""
        theme_name = self._theme_var.get()
        self._on_theme_changed(theme_name)
    
    def _on_topmost_change(self) -> None:
        """最前面表示変更イベント"""
        self._config.set("always_on_top", self._topmost_var.get())
        self._on_settings_changed("always_on_top", self._topmost_var.get())
    
    def _on_digital_change(self) -> None:
        """デジタル時計表示変更イベント"""
        self._config.set("show_digital_clock", self._digital_var.get())
        self._on_settings_changed("show_digital_clock", self._digital_var.get())
    
    def _on_size_change(self) -> None:
        """サイズ変更イベント"""
        size = self._size_var.get()
        self._custom_size_var.set(str(size))
        self._apply_size_change(size)
    
    def _on_custom_size_apply(self) -> None:
        """カスタムサイズ適用イベント"""
        try:
            size = int(self._custom_size_var.get())
            if 200 <= size <= 800:  # サイズ制限
                self._size_var.set(size)
                self._apply_size_change(size)
            else:
                tk.messagebox.showwarning("範囲エラー", "サイズは200から800の範囲で入力してください。")
        except ValueError:
            tk.messagebox.showerror("入力エラー", "数値を入力してください。")
    
    def _apply_size_change(self, size: int) -> None:
        """サイズ変更を適用"""
        # 設定を更新
        self._config.set("window_size", {"width": size + 50, "height": size + 100})
        self._config.set("clock_size", {"width": size, "height": size})
        self._config.set("center_position", {"x": size // 2, "y": size // 2})
        self._config.set("radius", (size - 50) // 2)
        
        # イベントを発行
        self._on_settings_changed("size_changed", size)
    
    def _on_reset(self) -> None:
        """リセットイベント"""
        # 設定をデフォルトに戻す
        self._config.set("current_theme", self._config.get_default_theme())
        self._config.set("always_on_top", False)
        self._config.set("show_digital_clock", True)
        self._config.set("window_size", {"width": 400, "height": 450})
        self._config.set("clock_size", {"width": 350, "height": 350})
        self._config.set("center_position", {"x": 175, "y": 175})
        self._config.set("radius", 150)
        
        # UIを更新
        self._theme_var.set(self._config.get_default_theme())
        self._topmost_var.set(False)
        self._digital_var.set(True)
        self._size_var.set(350)
        self._custom_size_var.set("350")
        
        # イベントを発行
        self._on_theme_changed(self._config.get_default_theme())
        self._on_settings_changed("reset", True)