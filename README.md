# 🚀 CLI Sandbox

Python + Typer + FastAPI で構築した、学習兼ツール開発用の CLI & Web API プロジェクトです。

---

## 🔧 機能一覧

### CLIコマンド

| コマンド | 説明 |
|---------|------|
| `greet` | 名前を指定して挨拶 |
| `greet-env` | .envから読み込んで挨拶 |
| `save` | メッセージをJSONに保存 |
| `load` | 保存したログを読み込んで表示 |

### Web API（FastAPI）

| エンドポイント | 説明 |
|----------------|------|
| `GET /greet` | クエリで挨拶（例: `/greet?name=太郎&repeat=2`） |
| `GET /version` | バージョン表示 |

---

## 💻 実行方法

### 1. リポジトリのクローン

```bash
git clone https://github.com/あなたのユーザー名/cli-sandbox.git
cd cli-sandbox
```

### 2. Poetry環境の構築

```bash
poetry install
```

### 3. CLI実行例

```bash
poetry run cli greet --name 太郎 --repeat 2
```

### 4. Web APIの起動

```bash
poetry run uvicorn cli_sandbox.main_api:app --reload
```

### 5. API確認（ブラウザアクセス）

- Swagger UI: http://localhost:8000/docs  
- 実行例: http://localhost:8000/greet?name=太郎&repeat=2

---

## 🧪 テスト（pytest）

```bash
poetry run pytest
```

---

## 🔒 環境変数（.env）

`.env` ファイルに以下のような変数を定義可能です：

```env
DEFAULT_NAME=太郎
GREETING_REPEAT=2
```

※ `.env` は `.gitignore` により GitHub には含まれません。

---

## 🧠 技術スタック

- [Python 3.12](https://www.python.org/)
- [Typer](https://typer.tiangolo.com/) - CLI構築
- [FastAPI](https://fastapi.tiangolo.com/) - Web API
- [PyYAML](https://pyyaml.org/) - YAML読み込み
- [python-dotenv](https://github.com/theskumar/python-dotenv) - .env管理
- [PyInstaller](https://pyinstaller.org/) - .exeビルド
- [pytest](https://docs.pytest.org/) - 自動テスト
- [httpx](https://www.python-httpx.org/) - HTTPクライアント

---

## 📁 ディレクトリ構成

```text
cli-sandbox/
├── .gitignore
├── .env               # 環境変数ファイル（Git管理外）
├── README.md
├── pyproject.toml     # Poetry設定
├── poetry.lock
├── dist/              # PyInstallerで出力されたexeファイル
├── tests/             # pytestによる自動テスト
│   ├── test_cli.py
│   └── test_api.py
├── src/
│   └── cli_sandbox/
│       ├── main.py         # CLIエントリポイント
│       ├── main_api.py     # FastAPIエントリポイント
│       └── commands/       # コマンドごとに分離
│           ├── greet.py
│           ├── save.py
│           ├── load.py
│           └── goodbye.py
```

---

## 📝 ライセンス

MIT
