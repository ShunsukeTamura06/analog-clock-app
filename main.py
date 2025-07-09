#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Analog Clock Application (SOLID Refactored Version)
アナログ時計アプリケーション（SOLID原則リファクタリング版）

This is the modernized version following SOLID principles:
- Single Responsibility: Each class has one reason to change
- Open/Closed: Open for extension, closed for modification  
- Liskov Substitution: Derived classes are substitutable for their base classes
- Interface Segregation: Clients don't depend on interfaces they don't use
- Dependency Inversion: Depend on abstractions, not concretions

このSOLID原則に従った現代版は以下の特徴を持ちます：
- 単一責任：各クラスは一つの変更理由を持ちます
- 開放/閉鎖：拡張に対して開放、修正に対して閉鎖
- リスコフの置換：派生クラスはベースクラスと置換可能
- インターフェース分離：クライアントは使用しないインターフェースに依存しない
- 依存性逆転：具象ではなく抽象に依存
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
        app.initialize()
        app.run()
    except KeyboardInterrupt:
        print("
アプリケーションを終了します...")
    except Exception as e:
        print(f"エラーが発生しました: {e}")
    finally:
        app.shutdown()

if __name__ == "__main__":
    main()