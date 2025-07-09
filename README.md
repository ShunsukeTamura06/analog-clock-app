# アナログ時計アプリ

Windows 11用のアナログ時計アプリケーション（Python/tkinter製）

## 🎯 SOLID原則リファクタリング版

このプロジェクトは**SOLID原則**に従って設計されており、将来的な機能拡張を容易にします。

### 📐 アーキテクチャの特徴

- **Single Responsibility (単一責任)**: 各クラスは一つの責任のみを持つ
- **Open/Closed (開放/閉鎖)**: 既存コードを変更せずに新機能を追加可能
- **Liskov Substitution (リスコフの置換)**: 派生クラスは基底クラスと置換可能
- **Interface Segregation (インターフェース分離)**: 必要なインターフェースのみに依存
- **Dependency Inversion (依存性逆転)**: 抽象化に依存し、具象に依存しない

## 🏗️ プロジェクト構造

```
analog-clock-app/
├── src/
│   ├── interfaces/          # インターフェース定義
│   │   ├── theme_interface.py
│   │   ├── time_provider_interface.py
│   │   └── renderer_interface.py
│   ├── core/               # コアコンポーネント
│   │   ├── clock_application.py
│   │   ├── clock_window.py
│   │   ├── time_provider.py
│   │   ├── clock_config.py
│   │   └── event_manager.py
│   ├── themes/             # テーマシステム
│   │   ├── theme_manager.py
│   │   ├── base_theme.py
│   │   └── concrete_themes.py
│   └── rendering/          # 描画システム
│       └── analog_clock_renderer.py
├── main.py                 # 新しいエントリーポイント
├── analog_clock.py         # レガシー版（互換性維持）
└── README.md
```

## 📱 利用可能なテーマ

1. **モダン** - 濃いブルーグレー基調の現代的なデザイン
2. **クラシック** - 伝統的な時計のような上品なデザイン  
3. **ダーク** - GitHub風の暗いテーマ（目に優しい）
4. **ライト** - 明るく清潔感のあるデザイン
5. **ネオン** - サイバーパンク風の発光効果付き
6. **ミニマル** - 無駄を省いたシンプルなデザイン

## 🚀 インストール & 実行

### 必要環境
- Python 3.x
- tkinter（Pythonに標準で含まれています）

### 実行方法

#### SOLID原則版（推奨）
```bash
git clone https://github.com/ShunsukeTamura06/analog-clock-app.git
cd analog-clock-app
python main.py
```

#### レガシー版
```bash
python analog_clock.py
```

## ✨ 将来の機能拡張

このSOLID原則アーキテクチャにより、以下の機能を簡単に追加できます：

### 🔧 予定されている機能
- **アラーム機能** - 指定時刻に通知
- **タイムゾーン対応** - 世界各地の時刻表示
- **カスタムテーマ作成** - ユーザー独自のテーマ
- **設定保存・復元** - ユーザー設定の永続化
- **サウンド機能** - 時報やクリック音
- **プラグインシステム** - 外部機能の追加
- **異なる時計タイプ** - デジタル時計、ワールドクロック
- **通知機能** - システム通知との連携

### 🎨 新しいテーマの追加方法

```python
from src.themes.base_theme import BaseTheme

class MyCustomTheme(BaseTheme):
    def __init__(self):
        super().__init__("マイテーマ")
    
    def _define_colors(self):
        return {
            'bg': '#カスタム背景色',
            'canvas_bg': '#カスタムキャンバス色',
            # ... 他の色設定
        }

# ThemeManagerに登録
theme_manager.register_theme(MyCustomTheme())
```

## 🔧 開発者向け情報

### クラス責任分離

- **ClockApplication**: アプリケーション全体の制御
- **ClockWindow**: UI/ウィンドウ管理
- **TimeProvider**: 時間データの提供
- **ThemeManager**: テーマの管理
- **AnalogClockRenderer**: 時計の描画
- **EventManager**: イベント処理
- **ClockConfig**: 設定管理

### 依存性注入

コンポーネント間は**インターフェース**を通じて疎結合になっており、テストが容易で拡張性が高い設計です。

### テスト

```bash
# 将来的にはユニットテストも追加予定
python -m pytest tests/
```

## 📄 ライセンス

MIT License

## 👤 作者

[@ShunsukeTamura06](https://github.com/ShunsukeTamura06)

---

## 🔄 バージョン比較

| 機能 | レガシー版 | SOLID原則版 |
|------|-----------|-------------|
| テーマ変更 | ✅ | ✅ |
| 設定保存 | ❌ | ✅ |
| 新テーマ追加 | 🔧 要コード変更 | ✅ プラグイン可能 |
| 新機能追加 | 🔧 要大幅変更 | ✅ 簡単に拡張 |
| テスタビリティ | ❌ | ✅ |
| 保守性 | ⚠️ | ✅ |

💡 **推奨**: 新機能の開発や長期的な保守を考慮し、SOLID原則版（`main.py`）の使用を推奨します。レガシー版（`analog_clock.py`）は既存環境との互換性維持のために残されています。
