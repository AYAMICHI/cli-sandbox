import json
from datetime import datetime
import typer
from pathlib import Path

def register(app: typer.Typer):
    @app.command("save-json", help="挨拶メッセージをJSON形式でファイルに保存します")
    def save_json(
        name: str = typer.Option(..., "--name", "-n", help="あなたの名前"),
        message: str = typer.Option(..., "--message", "-m", help="メッセージ内容"),
        file: str = typer.Option("greetings.json", "--file", "-f", help="保存先ファイル名")
    ):
        now = datetime.now().strftime("%Y-%m-%d %H:%M")
        log = {
            "timestamp": now,
            "name": name,
            "message": message
        }
        
        # JSONファイルに追記するために、既存の内容を読み込む
        file_path = Path(file)
        if file_path.exists():
            with open(file, "r", encoding="utf-8") as f:
                try:
                    data = json.load(f)
                except json.JSONDecodeError:
                    # JSONが壊れている場合は新しいリストを作成
                    data = []
        else:
            data = []
        
        data.append(log)
        
        with open(file, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        
        typer.echo(f"✅ 保存完了: {file}")