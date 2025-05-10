import json
import typer
from pathlib import Path

def register(app: typer.Typer):
    @app.command("load-json", help="JSON形式の挨拶ログを表示します")
    def load_json(
        file: str = typer.Option("greetings.json", "--file", "-f", help="読み込むファイル名")
    ):
        file_path = Path(file)
        if not file_path.exists():
            typer.secho(f"❌ ファイルが見つかりません: {file}")
            return

        with open(file, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                typer.secho("⚠️ エラー: JSONファイルの読み込みに失敗しました", fg="yellow")
                return
        
        if not data:
            typer.secho("⚠️ データは空です。", fg="yellow")
            return
        
        typer.secho("📄 ログ内容:", fg="green", bold=True)
        for entry in data:
            print(f"[{entry['timestamp']}] {entry['name']}: {entry['message']}")