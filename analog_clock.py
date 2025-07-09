import tkinter as tk
from tkinter import ttk
import math
import time
from datetime import datetime

class AnalogClock:
    def __init__(self, root):
        self.root = root
        self.root.title("アナログ時計")
        self.root.geometry("400x500")
        self.root.resizable(False, False)
        
        # 現在のテーマ
        self.current_theme = "モダン"
        
        # テーマの定義
        self.themes = {
            "モダン": {
                'bg': '#2c3e50',
                'canvas_bg': '#34495e',
                'face': '#ecf0f1',
                'hour_hand': '#e74c3c',
                'minute_hand': '#f39c12',
                'second_hand': '#e67e22',
                'numbers': '#2c3e50',
                'marks': '#7f8c8d',
                'center': '#c0392b',
                'digital_fg': '#ecf0f1',
                'outline': '#bdc3c7'
            },
            "クラシック": {
                'bg': '#f4f1de',
                'canvas_bg': '#f4f1de',
                'face': '#fefefe',
                'hour_hand': '#2d3436',
                'minute_hand': '#2d3436',
                'second_hand': '#d63031',
                'numbers': '#2d3436',
                'marks': '#636e72',
                'center': '#2d3436',
                'digital_fg': '#2d3436',
                'outline': '#ddd'
            },
            "ダーク": {
                'bg': '#0d1117',
                'canvas_bg': '#161b22',
                'face': '#21262d',
                'hour_hand': '#58a6ff',
                'minute_hand': '#79c0ff',
                'second_hand': '#f85149',
                'numbers': '#c9d1d9',
                'marks': '#484f58',
                'center': '#f85149',
                'digital_fg': '#c9d1d9',
                'outline': '#30363d'
            },
            "ライト": {
                'bg': '#ffffff',
                'canvas_bg': '#f8f9fa',
                'face': '#ffffff',
                'hour_hand': '#495057',
                'minute_hand': '#6c757d',
                'second_hand': '#dc3545',
                'numbers': '#212529',
                'marks': '#adb5bd',
                'center': '#dc3545',
                'digital_fg': '#212529',
                'outline': '#dee2e6'
            },
            "ネオン": {
                'bg': '#0a0a0a',
                'canvas_bg': '#1a1a1a',
                'face': '#000000',
                'hour_hand': '#00ff41',
                'minute_hand': '#ff0080',
                'second_hand': '#00d4ff',
                'numbers': '#ffffff',
                'marks': '#666666',
                'center': '#ff0080',
                'digital_fg': '#00ff41',
                'outline': '#333333'
            },
            "ミニマル": {
                'bg': '#fafafa',
                'canvas_bg': '#fafafa',
                'face': '#ffffff',
                'hour_hand': '#424242',
                'minute_hand': '#757575',
                'second_hand': '#ff5722',
                'numbers': '#212121',
                'marks': '#bdbdbd',
                'center': '#ff5722',
                'digital_fg': '#212121',
                'outline': '#e0e0e0'
            }
        }
        
        # ウィンドウを中央に配置
        self.center_window()
        
        # テーマ選択フレーム
        self.theme_frame = tk.Frame(self.root)
        self.theme_frame.pack(pady=5)
        
        tk.Label(self.theme_frame, text="テーマ:", font=('Arial', 10)).pack(side=tk.LEFT, padx=5)
        
        self.theme_var = tk.StringVar(value=self.current_theme)
        self.theme_combo = ttk.Combobox(
            self.theme_frame,
            textvariable=self.theme_var,
            values=list(self.themes.keys()),
            state="readonly",
            width=12
        )
        self.theme_combo.pack(side=tk.LEFT, padx=5)
        self.theme_combo.bind('<<ComboboxSelected>>', self.change_theme)
        
        # デジタル時計の表示
        self.digital_frame = tk.Frame(self.root)
        self.digital_frame.pack(pady=5)
        
        self.digital_label = tk.Label(
            self.digital_frame,
            font=('Arial', 14, 'bold')
        )
        self.digital_label.pack()
        
        # キャンバスの作成
        self.canvas = tk.Canvas(
            self.root,
            width=350,
            height=350,
            highlightthickness=0
        )
        self.canvas.pack(pady=10)
        
        # 時計の中心と半径
        self.center_x = 175
        self.center_y = 175
        self.radius = 150
        
        # テーマを適用
        self.apply_theme()
        
        # 時計の描画を開始
        self.draw_clock_face()
        self.update_clock()
    
    def center_window(self):
        """ウィンドウを画面中央に配置"""
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (400 // 2)
        y = (self.root.winfo_screenheight() // 2) - (500 // 2)
        self.root.geometry(f'400x500+{x}+{y}')
    
    def change_theme(self, event=None):
        """テーマを変更"""
        self.current_theme = self.theme_var.get()
        self.apply_theme()
        self.redraw_clock()
    
    def apply_theme(self):
        """現在のテーマを適用"""
        theme = self.themes[self.current_theme]
        self.root.configure(bg=theme['bg'])
        self.theme_frame.configure(bg=theme['bg'])
        self.digital_frame.configure(bg=theme['bg'])
        self.digital_label.configure(bg=theme['bg'], fg=theme['digital_fg'])
        self.canvas.configure(bg=theme['canvas_bg'])
    
    def get_current_colors(self):
        """現在のテーマの色を取得"""
        return self.themes[self.current_theme]
    
    def redraw_clock(self):
        """時計を再描画"""
        self.canvas.delete("all")
        self.draw_clock_face()
    
    def draw_clock_face(self):
        """時計の文字盤を描画"""
        colors = self.get_current_colors()
        
        # 外側の円（文字盤）
        self.canvas.create_oval(
            self.center_x - self.radius,
            self.center_y - self.radius,
            self.center_x + self.radius,
            self.center_y + self.radius,
            fill=colors['face'],
            outline=colors['outline'],
            width=3
        )
        
        # ネオンテーマの場合は発光効果を追加
        if self.current_theme == "ネオン":
            for i in range(3):
                self.canvas.create_oval(
                    self.center_x - self.radius - i,
                    self.center_y - self.radius - i,
                    self.center_x + self.radius + i,
                    self.center_y + self.radius + i,
                    fill='',
                    outline=colors['outline'],
                    width=1
                )
        
        # 時間の数字を描画
        for hour in range(1, 13):
            angle = math.radians(90 - (hour * 30))
            x = self.center_x + (self.radius - 30) * math.cos(angle)
            y = self.center_y - (self.radius - 30) * math.sin(angle)
            
            font_size = 18 if self.current_theme == "ミニマル" else 16
            font_weight = 'normal' if self.current_theme == "ミニマル" else 'bold'
            
            self.canvas.create_text(
                x, y,
                text=str(hour),
                font=('Arial', font_size, font_weight),
                fill=colors['numbers']
            )
        
        # 時間の目盛りを描画
        for hour in range(12):
            angle = math.radians(hour * 30)
            x1 = self.center_x + (self.radius - 15) * math.cos(angle)
            y1 = self.center_y + (self.radius - 15) * math.sin(angle)
            x2 = self.center_x + (self.radius - 5) * math.cos(angle)
            y2 = self.center_y + (self.radius - 5) * math.sin(angle)
            
            mark_width = 2 if self.current_theme == "ミニマル" else 3
            
            self.canvas.create_line(
                x1, y1, x2, y2,
                fill=colors['marks'],
                width=mark_width
            )
        
        # 分の目盛りを描画（ミニマルテーマでは省略）
        if self.current_theme != "ミニマル":
            for minute in range(60):
                if minute % 5 != 0:  # 5分刻み以外の目盛り
                    angle = math.radians(minute * 6)
                    x1 = self.center_x + (self.radius - 10) * math.cos(angle)
                    y1 = self.center_y + (self.radius - 10) * math.sin(angle)
                    x2 = self.center_x + (self.radius - 5) * math.cos(angle)
                    y2 = self.center_y + (self.radius - 5) * math.sin(angle)
                    
                    self.canvas.create_line(
                        x1, y1, x2, y2,
                        fill=colors['marks'],
                        width=1
                    )
    
    def draw_hand(self, angle, length, width, color, tag):
        """時計の針を描画"""
        angle_rad = math.radians(90 - angle)
        end_x = self.center_x + length * math.cos(angle_rad)
        end_y = self.center_y - length * math.sin(angle_rad)
        
        # ネオンテーマの場合は発光効果を追加
        if self.current_theme == "ネオン":
            for i in range(3):
                self.canvas.create_line(
                    self.center_x, self.center_y,
                    end_x, end_y,
                    fill=color,
                    width=width + i,
                    capstyle='round',
                    tags=tag
                )
        else:
            self.canvas.create_line(
                self.center_x, self.center_y,
                end_x, end_y,
                fill=color,
                width=width,
                capstyle='round',
                tags=tag
            )
    
    def update_clock(self):
        """時計を更新"""
        # 前の針を削除
        self.canvas.delete('hands')
        
        # 現在時刻を取得
        now = datetime.now()
        hours = now.hour % 12
        minutes = now.minute
        seconds = now.second
        
        # デジタル時計を更新
        digital_time = now.strftime("%Y年%m月%d日 %H:%M:%S")
        self.digital_label.config(text=digital_time)
        
        # 針の角度を計算
        second_angle = seconds * 6  # 秒針: 6度/秒
        minute_angle = minutes * 6 + seconds * 0.1  # 分針: 6度/分 + 滑らかな動き
        hour_angle = hours * 30 + minutes * 0.5  # 時針: 30度/時間 + 滑らかな動き
        
        colors = self.get_current_colors()
        
        # 針の太さをテーマに応じて調整
        if self.current_theme == "ミニマル":
            hour_width, minute_width, second_width = 4, 2, 1
        elif self.current_theme == "クラシック":
            hour_width, minute_width, second_width = 8, 6, 2
        else:
            hour_width, minute_width, second_width = 6, 4, 2
        
        # 針を描画
        self.draw_hand(hour_angle, 80, hour_width, colors['hour_hand'], 'hands')
        self.draw_hand(minute_angle, 110, minute_width, colors['minute_hand'], 'hands')
        self.draw_hand(second_angle, 120, second_width, colors['second_hand'], 'hands')
        
        # 中心の円を描画
        center_size = 6 if self.current_theme == "ミニマル" else 8
        self.canvas.create_oval(
            self.center_x - center_size,
            self.center_y - center_size,
            self.center_x + center_size,
            self.center_y + center_size,
            fill=colors['center'],
            outline=colors['center'],
            width=2,
            tags='hands'
        )
        
        # 1秒後に再度更新
        self.root.after(1000, self.update_clock)

def main():
    # メインウィンドウの作成
    root = tk.Tk()
    
    # アイコンの設定（オプション）
    try:
        root.iconbitmap('clock.ico')  # アイコンファイルがある場合
    except:
        pass
    
    # アプリケーションの作成
    app = AnalogClock(root)
    
    # イベントループの開始
    root.mainloop()

if __name__ == "__main__":
    main()
