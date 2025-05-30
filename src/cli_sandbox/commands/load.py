import typer
import json
from pathlib import Path

def register(app: typer.Typer):
    @app.command(help="保存した挨拶メッセージを表示します")
    def load(
        file: str = typer.Option("greetings.txt", "--file", "-f", help="読み込みファイル名")
    ):
        try:
            with open(file, "r", encoding="utf-8") as f:
                content = f.read().strip()
                if content:
                    typer.secho("📄 ログ内容:", fg="green", bold=True)
                    typer.secho(content, fg="white")
                else:
                    typer.secho("⚠️ ファイルは空です。", fg="yellow")
        except FileNotFoundError:
            typer.secho(f"❌ ファイルが見つかりません: {file}", fg="red")
        except Exception as e:
            typer.echo(f"エラーが発生しました: {e}")
            
def load_greetings(file: str = "greetings.json") -> list[str] | None:
    path = Path(file)
    if not path.exists():
        return None

    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
            
    return data.get("messages", [])