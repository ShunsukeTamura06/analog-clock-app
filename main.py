#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Analog Clock Application (SOLID Refactored Version with Separated UI)
アナログ時計アプリケーション（UI分離版 SOLID原則リファクタリング版）

This is the modernized version following SOLID principles with separated UI:
- 時計表示と設定画面の分離
- 常に最前面表示機能
- サイズ変更機能
- 右クリックメニューで設定アクセス
- 設定の自動保存

Features:
- Separated clock display and settings windows
- Always on top functionality
- Resizable clock (4 presets + custom size)
- Right-click context menu for quick access
- Automatic settings persistence
- Clean, SOLID architecture for easy extension
"""

import sys
import os

# Add src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.core.clock_application import ClockApplication

def main():
    """メインエントリーポイント"""
    app = ClockApplication()
    
    try:
        print("アナログ時計アプリケーションを起動中...")
        print("操作方法:")
        print("- 時計を右クリックして設定を開く")
        print("- 設定でテーマ、サイズ、表示オプションを変更")
        print("- 常に最前面表示で他のアプリの上に表示")
        print("")
        
        app.initialize()
        app.run()
    except KeyboardInterrupt:
        print("\nアプリケーションを終了します...")
    except Exception as e:
        print(f"エラーが発生しました: {e}")
        import traceback
        traceback.print_exc()
    finally:
        app.shutdown()

if __name__ == "__main__":
    main()