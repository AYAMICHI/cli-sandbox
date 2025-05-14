import typer
import json
from pathlib import Path
from datetime import datetime


def register(app: typer.Typer):
    @app.command(help="挨拶メッセージをファイルに保存します")
    def save(
        name: str = typer.Option(..., "--name", "-n", help="あなたの名前"),
        message: str = typer.Option(..., "--message", "-m", help="保存したいメッセージ"),
        file: str = typer.Option("greetings.txt", "--file", "-f", help="保存先ファイル名")
    ):
        now = datetime.now().strftime("%Y-%m-%d %H:%M")
        lof_line = f"{now} {name}: {message}"
        with open(file, "a", encoding="utf-8") as f:
            f.write(lof_line + "\n")
        typer.echo(f"✅ 保存完了: {file}")
        
def save_greetings(name: str, messages: list[str], file: str = "greetings.json"):
    data = {
        "name": name,
        "messages": messages
    }
    with open(file, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)