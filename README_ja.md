# Attribute Assignment Plugin

他の言語で読む: [英語](./README.md)

![logo](./img/logo.png)

QGISで簡単に属性付与

## QGIS Python Plugins Repository

[Attribute Assignment Plugin](https://plugins.qgis.org/plugins/attribute_assignment)  

## blog


## 利用方法

![menu](./img/menu.gif)

1. Attribute Assignmentボタンをクリック
2. ダイアログで「対象レイヤ」「対象フィールド」「値」を設定
3. 対象地物をクリックで属性更新

## 開発

### 必要なツール

- [uv](https://docs.astral.sh/uv/)
- QGIS 3.x

### セットアップ

```bash
# 依存関係のインストール
uv sync

# リント
uv run ruff check .

# フォーマット
uv run ruff format .
```

### ローカル開発

QGISのプラグインディレクトリにシンボリックリンクを作成します：

**macOS:**
```bash
ln -s /path/to/attribute_assignment ~/Library/Application\ Support/QGIS/QGIS3/profiles/default/python/plugins/attribute_assignment
```

**Windows:**
```powershell
mklink /D "%APPDATA%\QGIS\QGIS3\profiles\default\python\plugins\attribute_assignment" "C:\path\to\attribute_assignment"
```

**Linux:**
```bash
ln -s /path/to/attribute_assignment ~/.local/share/QGIS/QGIS3/profiles/default/python/plugins/attribute_assignment
```

コードを編集した後、QGISでプラグインをリロードすると変更が反映されます。

## ライセンス

Python modules are released under the GNU General Public License v2.0

Copyright (c) 2018-2026 Yasunori Kirimoto
