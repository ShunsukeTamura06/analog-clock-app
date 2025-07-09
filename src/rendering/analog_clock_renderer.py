import tkinter as tk
import math
from typing import Any
from ..interfaces.renderer_interface import IRenderer
from ..interfaces.theme_interface import ITheme
from ..core.clock_config import ClockConfig

class AnalogClockRenderer(IRenderer):
    """アナログ時計の描画クラス - Single Responsibility Principle"""
    
    def __init__(self):
        self._canvas: tk.Canvas = None
        self._config: ClockConfig = None
        self._center_x: int = 175
        self._center_y: int = 175
        self._radius: int = 150
    
    def initialize(self, canvas: tk.Canvas, config: ClockConfig) -> None:
        """レンダラーを初期化"""
        self._canvas = canvas
        self._config = config
        
        # 設定からパラメータを取得
        center_pos = config.get_center_position()
        self._center_x = center_pos['x']
        self._center_y = center_pos['y']
        self._radius = config.get_radius()
    
    def render_clock_face(self, theme: ITheme) -> None:
        """時計の文字盤を描画"""
        colors = theme.get_colors()
        font_settings = theme.get_font_settings()
        
        # 外側の円（文字盤）
        self._canvas.create_oval(
            self._center_x - self._radius,
            self._center_y - self._radius,
            self._center_x + self._radius,
            self._center_y + self._radius,
            fill=colors['face'],
            outline=colors['outline'],
            width=max(1, self._radius // 50)  # サイズに応じて線の太さを調整
        )
        
        # テーマ固有の特殊効果を適用（文字盤用）
        self._apply_face_special_effects(theme)
        
        # 時間の数字を描画
        self._draw_hour_numbers(theme)
        
        # 時間の目盛りを描画
        self._draw_hour_marks(theme)
        
        # 分の目盛りを描画（ミニマルテーマ以外）
        if theme.get_name() != "ミニマル":
            self._draw_minute_marks(theme)
    
    def _apply_face_special_effects(self, theme: ITheme) -> None:
        """文字盤に特殊効果を適用"""
        if theme.get_name() == "ネオン":
            colors = theme.get_colors()
            # ネオン発光効果
            glow_layers = max(2, self._radius // 75)  # サイズに応じて発光レイヤー数を調整
            for i in range(glow_layers):
                self._canvas.create_oval(
                    self._center_x - self._radius - i,
                    self._center_y - self._radius - i,
                    self._center_x + self._radius + i,
                    self._center_y + self._radius + i,
                    fill='',
                    outline=colors['outline'],
                    width=1
                )
    
    def _draw_hour_numbers(self, theme: ITheme) -> None:
        """時間の数字を描画"""
        colors = theme.get_colors()
        font_settings = theme.get_font_settings()
        
        # サイズに応じてフォントサイズを調整
        font_size = max(10, self._radius // 10)
        if theme.get_name() == "ミニマル":
            font_size = max(12, self._radius // 8)
        
        for hour in range(1, 13):
            angle = math.radians(90 - (hour * 30))
            distance = self._radius - max(20, self._radius // 7.5)  # サイズに応じて距離を調整
            x = self._center_x + distance * math.cos(angle)
            y = self._center_y - distance * math.sin(angle)
            
            self._canvas.create_text(
                x, y,
                text=str(hour),
                font=(font_settings['family'], font_size, font_settings['weight']),
                fill=colors['numbers']
            )
    
    def _draw_hour_marks(self, theme: ITheme) -> None:
        """時間の目盛りを描画"""
        colors = theme.get_colors()
        
        mark_width = max(1, self._radius // 75) if theme.get_name() == "ミニマル" else max(2, self._radius // 50)
        mark_length = max(8, self._radius // 18)
        
        for hour in range(12):
            angle = math.radians(hour * 30)
            x1 = self._center_x + (self._radius - mark_length) * math.cos(angle)
            y1 = self._center_y + (self._radius - mark_length) * math.sin(angle)
            x2 = self._center_x + (self._radius - max(3, mark_length // 3)) * math.cos(angle)
            y2 = self._center_y + (self._radius - max(3, mark_length // 3)) * math.sin(angle)
            
            self._canvas.create_line(
                x1, y1, x2, y2,
                fill=colors['marks'],
                width=mark_width
            )
    
    def _draw_minute_marks(self, theme: ITheme) -> None:
        """分の目盛りを描画"""
        colors = theme.get_colors()
        
        mark_length = max(4, self._radius // 30)
        
        for minute in range(60):
            if minute % 5 != 0:  # 5分刻み以外の目盛り
                angle = math.radians(minute * 6)
                x1 = self._center_x + (self._radius - mark_length) * math.cos(angle)
                y1 = self._center_y + (self._radius - mark_length) * math.sin(angle)
                x2 = self._center_x + (self._radius - max(2, mark_length // 2)) * math.cos(angle)
                y2 = self._center_y + (self._radius - max(2, mark_length // 2)) * math.sin(angle)
                
                self._canvas.create_line(
                    x1, y1, x2, y2,
                    fill=colors['marks'],
                    width=1
                )
    
    def render_hands(self, hours: int, minutes: int, seconds: int, theme: ITheme) -> None:
        """時計の針を描画"""
        # 針の角度を計算
        second_angle = seconds * 6  # 秒針: 6度/秒
        minute_angle = minutes * 6 + seconds * 0.1  # 分針: 6度/分 + 滑らかな動き
        hour_angle = hours * 30 + minutes * 0.5  # 時針: 30度/時間 + 滑らかな動き
        
        colors = theme.get_colors()
        hand_settings = theme.get_hand_settings()
        
        # サイズに応じて針の長さと太さを調整
        scale_factor = self._radius / 150  # ベースサイズ150で正規化
        
        hour_length = int(80 * scale_factor)
        minute_length = int(110 * scale_factor)
        second_length = int(120 * scale_factor)
        
        hour_width = max(1, int(hand_settings['hour_width'] * scale_factor))
        minute_width = max(1, int(hand_settings['minute_width'] * scale_factor))
        second_width = max(1, int(hand_settings['second_width'] * scale_factor))
        
        # 針を描画
        self._draw_hand(hour_angle, hour_length, hour_width, colors['hour_hand'], theme, 'hands')
        self._draw_hand(minute_angle, minute_length, minute_width, colors['minute_hand'], theme, 'hands')
        self._draw_hand(second_angle, second_length, second_width, colors['second_hand'], theme, 'hands')
        
        # 中心の円を描画
        center_size = max(4, int((6 if theme.get_name() == "ミニマル" else 8) * scale_factor))
        self._canvas.create_oval(
            self._center_x - center_size,
            self._center_y - center_size,
            self._center_x + center_size,
            self._center_y + center_size,
            fill=colors['center'],
            outline=colors['center'],
            width=max(1, int(2 * scale_factor)),
            tags='hands'
        )
    
    def _draw_hand(self, angle: float, length: int, width: int, color: str, theme: ITheme, tag: str) -> None:
        """時計の針を描画"""
        angle_rad = math.radians(90 - angle)
        end_x = self._center_x + length * math.cos(angle_rad)
        end_y = self._center_y - length * math.sin(angle_rad)
        
        # テーマ固有の特殊効果を適用
        theme.apply_special_effects(
            self._canvas,
            self._canvas.create_line,
            self._center_x, self._center_y,
            end_x, end_y,
            fill=color,
            width=width,
            capstyle='round',
            tags=tag
        )
    
    def clear_hands(self) -> None:
        """針をクリア"""
        self._canvas.delete('hands')
    
    def clear_all(self) -> None:
        """すべてをクリア"""
        self._canvas.delete("all")